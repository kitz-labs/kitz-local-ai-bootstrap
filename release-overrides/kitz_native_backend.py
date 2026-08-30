#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from concurrent import futures

import grpc
import backend_pb2
import backend_pb2_grpc

AGENT_CORE_CHAT_URL = os.environ.get(
    'KITZ_AGENT_CORE_CHAT_URL',
    'http://127.0.0.1:8787/v1/chat/completions',
)
AGENT_CORE_HEALTH_URL = os.environ.get(
    'KITZ_AGENT_CORE_HEALTH_URL',
    'http://127.0.0.1:8787/health',
)
UPSTREAM_MODEL = 'kitz-agent'
MAX_WORKERS = int(os.environ.get('PYTHON_GRPC_MAX_WORKERS', '4'))


def _messages_from_request(request):
    messages = []
    for msg in getattr(request, 'Messages', []) or []:
        role = getattr(msg, 'role', '') or 'user'
        content = getattr(msg, 'content', '') or ''
        item = {'role': role, 'content': content}
        name = getattr(msg, 'name', '')
        if name:
            item['name'] = name
        tool_call_id = getattr(msg, 'tool_call_id', '')
        if tool_call_id:
            item['tool_call_id'] = tool_call_id
        raw_tool_calls = getattr(msg, 'tool_calls', '')
        if raw_tool_calls:
            try:
                item['tool_calls'] = json.loads(raw_tool_calls)
            except json.JSONDecodeError:
                pass
        messages.append(item)
    if not messages:
        prompt = getattr(request, 'Prompt', '') or ''
        messages = [{'role': 'user', 'content': prompt}]
    return messages


def _payload_from_request(request, *, stream: bool):
    payload = {
        'model': UPSTREAM_MODEL,
        'messages': _messages_from_request(request),
        'stream': stream,
    }
    tokens = int(getattr(request, 'Tokens', 0) or 0)
    if tokens > 0:
        payload['max_tokens'] = tokens
    temperature = float(getattr(request, 'Temperature', 0.0) or 0.0)
    if temperature > 0:
        payload['temperature'] = temperature
    top_p = float(getattr(request, 'TopP', 0.0) or 0.0)
    if top_p > 0:
        payload['top_p'] = top_p
    stop = list(getattr(request, 'StopPrompts', []) or [])
    if stop:
        payload['stop'] = stop
    tools = getattr(request, 'Tools', '') or ''
    if tools:
        try:
            payload['tools'] = json.loads(tools)
        except json.JSONDecodeError:
            pass
    tool_choice = getattr(request, 'ToolChoice', '') or ''
    if tool_choice:
        try:
            payload['tool_choice'] = json.loads(tool_choice)
        except json.JSONDecodeError:
            payload['tool_choice'] = tool_choice
    return payload


def _json_request(url: str, payload=None, timeout: float = 600.0):
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')
        headers['Content-Type'] = 'application/json'
        method = 'POST'
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode('utf-8')
    return json.loads(raw)


def _chat_content(payload):
    return str(payload['choices'][0]['message'].get('content') or '')


def _usage(payload):
    usage = payload.get('usage') or {}
    return int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)


def _iter_sse(payload):
    req = urllib.request.Request(
        AGENT_CORE_CHAT_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'text/event-stream'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=600.0) as resp:
        for raw_line in resp:
            line = raw_line.decode('utf-8', errors='replace').strip()
            if not line.startswith('data:'):
                continue
            data = line[5:].strip()
            if not data or data == '[DONE]':
                if data == '[DONE]':
                    break
                continue
            try:
                yield json.loads(data)
            except json.JSONDecodeError:
                continue


class BackendServicer(backend_pb2_grpc.BackendServicer):
    def Health(self, request, context):
        return backend_pb2.Reply(message=b'OK')

    def LoadModel(self, request, context):
        try:
            _json_request(AGENT_CORE_HEALTH_URL, timeout=5.0)
            return backend_pb2.Result(success=True, message='KITZ Agent Core online')
        except Exception as exc:
            return backend_pb2.Result(success=False, message=f'Agent Core unavailable: {exc}')

    def Free(self, request, context):
        return backend_pb2.Result(success=True, message='KITZ native backend freed')

    def Predict(self, request, context):
        try:
            payload = _payload_from_request(request, stream=False)
            data = _json_request(AGENT_CORE_CHAT_URL, payload=payload)
            content = _chat_content(data)
            prompt_tokens, completion_tokens = _usage(data)
            return backend_pb2.Reply(
                message=content.encode('utf-8'),
                prompt_tokens=prompt_tokens,
                tokens=completion_tokens,
                chat_deltas=[backend_pb2.ChatDelta(content=content)],
            )
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            return backend_pb2.Reply(message=b'')

    def PredictStream(self, request, context):
        try:
            payload = _payload_from_request(request, stream=True)
            for event in _iter_sse(payload):
                choices = event.get('choices') or []
                if choices:
                    delta = choices[0].get('delta') or {}
                    content = delta.get('content') or ''
                    reasoning = delta.get('reasoning_content') or ''
                    if content or reasoning:
                        yield backend_pb2.Reply(
                            message=content.encode('utf-8'),
                            chat_deltas=[backend_pb2.ChatDelta(content=content, reasoning_content=reasoning)],
                        )
                usage = event.get('usage') or {}
                if usage:
                    yield backend_pb2.Reply(
                        message=b'',
                        prompt_tokens=int(usage.get('prompt_tokens') or 0),
                        tokens=int(usage.get('completion_tokens') or 0),
                    )
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            yield backend_pb2.Reply(message=b'')


def serve(address: str):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=MAX_WORKERS),
        options=[
            ('grpc.max_message_length', 50 * 1024 * 1024),
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024),
        ],
    )
    backend_pb2_grpc.add_BackendServicer_to_server(BackendServicer(), server)
    server.add_insecure_port(address)
    server.start()
    print(f'KITZ native backend listening on {address}', file=sys.stderr, flush=True)
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', default='127.0.0.1:50051')
    args = parser.parse_args()
    serve(args.addr)
