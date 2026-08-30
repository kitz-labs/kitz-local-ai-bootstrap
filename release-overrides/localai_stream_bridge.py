from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

DEFAULT_AGENT_CORE_URL = 'http://127.0.0.1:8787/v1/chat/completions'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8788
MODEL_NAME = 'kitz-agent'
MAX_REQUEST_BODY_BYTES = 64 * 1024 * 1024


def normalize_request_for_agent_core(payload: dict[str, Any]) -> dict[str, Any]:
    result = dict(payload)
    result['model'] = MODEL_NAME
    result['stream'] = False
    result.pop('stream_options', None)
    return result


def _completion_parts(completion: dict[str, Any]) -> tuple[str, str, str, dict[str, Any] | None, list[dict[str, Any]] | None]:
    try:
        choice = completion['choices'][0]
        message = choice['message']
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError('Agent Core response is not an OpenAI chat completion') from exc
    if not isinstance(choice, dict) or not isinstance(message, dict):
        raise ValueError('Agent Core response is not an OpenAI chat completion')
    content = message.get('content') or ''
    if not isinstance(content, str):
        raise ValueError('Agent Core response content is not text')
    finish_reason = choice.get('finish_reason') or 'stop'
    response_id = completion.get('id') or f'chatcmpl-kitz-{uuid.uuid4().hex}'
    model = completion.get('model') or MODEL_NAME
    usage = completion.get('usage') if isinstance(completion.get('usage'), dict) else None
    tool_calls = message.get('tool_calls') if isinstance(message.get('tool_calls'), list) else None
    return str(response_id), str(model), str(finish_reason), usage, tool_calls


def _sse_line(payload: dict[str, Any]) -> bytes:
    return ('data: ' + json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n\n').encode('utf-8')


def encode_sse_completion(completion: dict[str, Any], *, include_usage: bool = False) -> bytes:
    response_id, model, finish_reason, usage, tool_calls = _completion_parts(completion)
    created = completion.get('created')
    if not isinstance(created, int):
        created = int(time.time())

    frames: list[bytes] = []
    frames.append(_sse_line({
        'id': response_id,
        'object': 'chat.completion.chunk',
        'created': created,
        'model': model,
        'choices': [{'index': 0, 'delta': {'role': 'assistant'}, 'finish_reason': None}],
    }))

    delta: dict[str, Any] = {}
    content = completion['choices'][0]['message'].get('content') or ''
    if content:
        delta['content'] = content
    if tool_calls:
        delta['tool_calls'] = tool_calls
    if delta:
        frames.append(_sse_line({
            'id': response_id,
            'object': 'chat.completion.chunk',
            'created': created,
            'model': model,
            'choices': [{'index': 0, 'delta': delta, 'finish_reason': None}],
        }))

    frames.append(_sse_line({
        'id': response_id,
        'object': 'chat.completion.chunk',
        'created': created,
        'model': model,
        'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
    }))

    if include_usage and usage is not None:
        frames.append(_sse_line({
            'id': response_id,
            'object': 'chat.completion.chunk',
            'created': created,
            'model': model,
            'choices': [],
            'usage': usage,
        }))

    frames.append(b'data: [DONE]\n\n')
    return b''.join(frames)


def _read_chunked_body(rfile: Any, *, max_bytes: int = MAX_REQUEST_BODY_BYTES) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        line = rfile.readline()
        if not line:
            raise ValueError('Unexpected EOF while reading chunk size')
        token = line.strip().split(b';', 1)[0]
        if not token:
            raise ValueError('Empty chunk size')
        try:
            size = int(token, 16)
        except ValueError as exc:
            raise ValueError(f'Invalid chunk size: {token!r}') from exc
        if size == 0:
            while True:
                trailer = rfile.readline()
                if trailer in (b'\r\n', b'\n', b''):
                    break
            return b''.join(chunks)
        total += size
        if total > max_bytes:
            raise ValueError('Request body too large')
        data = rfile.read(size)
        if len(data) != size:
            raise ValueError('Unexpected EOF inside chunk body')
        terminator = rfile.read(2)
        if terminator != b'\r\n':
            raise ValueError('Invalid chunk terminator')
        chunks.append(data)


def read_request_body(headers: Any, rfile: Any, *, max_bytes: int = MAX_REQUEST_BODY_BYTES) -> bytes:
    transfer_encoding = headers.get('Transfer-Encoding', '') or ''
    encodings = [part.strip().lower() for part in transfer_encoding.split(',')]
    if 'chunked' in encodings:
        return _read_chunked_body(rfile, max_bytes=max_bytes)

    raw_length = headers.get('Content-Length')
    if raw_length in (None, ''):
        return b''
    try:
        length = int(raw_length)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'Invalid Content-Length: {raw_length!r}') from exc
    if length < 0:
        raise ValueError('Negative Content-Length')
    if length > max_bytes:
        raise ValueError('Request body too large')
    data = rfile.read(length)
    if len(data) != length:
        raise ValueError('Unexpected EOF while reading request body')
    return data


def call_agent_core(payload: dict[str, Any], *, url: str = DEFAULT_AGENT_CORE_URL, timeout: float = 600.0) -> tuple[int, bytes, str]:
    body = json.dumps(normalize_request_for_agent_core(payload), ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=body,
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), resp.headers.get('Content-Type', 'application/json')
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), exc.headers.get('Content-Type', 'application/json')


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = 'KITZLocalAIStreamBridge/1.0.8'

    def log_message(self, fmt: str, *args: Any) -> None:
        print('[stream-bridge] ' + (fmt % args), flush=True)

    @property
    def agent_core_url(self) -> str:
        return getattr(self.server, 'agent_core_url', DEFAULT_AGENT_CORE_URL)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == '/health':
            self._send_json(200, {'ok': True, 'service': 'kitz-localai-stream-bridge', 'agent_core_url': self.agent_core_url})
            return
        self._send_json(404, {'detail': 'Not found'})

    def do_POST(self) -> None:
        if self.path != '/v1/chat/completions':
            self._send_json(404, {'detail': 'Not found'})
            return
        try:
            raw_body = read_request_body(self.headers, self.rfile)
            if not raw_body:
                raise ValueError('Empty request body')
            payload = json.loads(raw_body.decode('utf-8'))
            if not isinstance(payload, dict):
                raise ValueError('JSON body must be an object')
        except Exception as exc:
            self._send_json(400, {'detail': f'Invalid JSON request: {exc}'})
            return

        wants_stream = payload.get('stream') is True
        include_usage = bool((payload.get('stream_options') or {}).get('include_usage')) if isinstance(payload.get('stream_options'), dict) else False
        status, raw, content_type = call_agent_core(payload, url=self.agent_core_url)
        if status >= 400:
            self.send_response(status)
            self.send_header('Content-Type', content_type or 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return

        if not wants_stream:
            self.send_response(status)
            self.send_header('Content-Type', content_type or 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return

        try:
            completion = json.loads(raw.decode('utf-8'))
            if not isinstance(completion, dict):
                raise ValueError('Agent Core response must be a JSON object')
            sse = encode_sse_completion(completion, include_usage=include_usage)
        except Exception as exc:
            self._send_json(502, {'detail': f'Could not convert Agent Core response to SSE: {exc}'})
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'close')
        self.send_header('X-Accel-Buffering', 'no')
        self.end_headers()
        self.wfile.write(sse)
        self.wfile.flush()
        self.close_connection = True


def run_server(*, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, agent_core_url: str = DEFAULT_AGENT_CORE_URL) -> None:
    server = ThreadingHTTPServer((host, port), BridgeHandler)
    server.agent_core_url = agent_core_url
    print(f'[stream-bridge] listening on http://{host}:{port} -> {agent_core_url}', flush=True)
    server.serve_forever()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='KITZ LocalAI streaming compatibility bridge')
    parser.add_argument('--host', default=DEFAULT_HOST)
    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('--agent-core-url', default=DEFAULT_AGENT_CORE_URL)
    args = parser.parse_args(argv)
    run_server(host=args.host, port=args.port, agent_core_url=args.agent_core_url)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
