from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

MODEL_NAME = "kitz-agent"
AGENT_CORE_CHAT_URL = "http://127.0.0.1:8787/v1/chat/completions"
AGENT_CORE_HEALTH_URL = "http://127.0.0.1:8787/health"
LOCALAI_MODELS_URL = "http://127.0.0.1:8080/v1/models"
LOCALAI_CHAT_URL = "http://127.0.0.1:8080/v1/chat/completions"


@dataclass(frozen=True)
class InstallResult:
    path: Path
    changed: bool
    backup: Path | None = None


def render_bridge_config(*, model_name: str = MODEL_NAME, upstream_url: str = AGENT_CORE_CHAT_URL) -> str:
    return (
        f"name: {model_name}\n"
        "description: KITZ Agent Core - local orchestrator for models, knowledge and tools\n"
        "known_usecases:\n"
        "  - chat\n"
        "backend: cloud-proxy\n"
        "proxy:\n"
        "  mode: passthrough\n"
        "  provider: openai\n"
        f"  upstream_url: {upstream_url}\n"
        f"  upstream_model: {model_name}\n"
        "  request_timeout_seconds: 600\n"
        "pii:\n"
        "  enabled: false\n"
    )


def install_bridge_config(model_dir: Path, *, now: datetime | None = None) -> InstallResult:
    model_dir = Path(model_dir).expanduser()
    model_dir.mkdir(parents=True, exist_ok=True)
    target = model_dir / f"{MODEL_NAME}.yaml"
    desired = render_bridge_config()
    if target.exists() and target.read_text(encoding="utf-8") == desired:
        return InstallResult(path=target, changed=False)
    backup: Path | None = None
    if target.exists():
        stamp = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
        backup = model_dir / f"{target.name}.pre-v1.0.4-{stamp}"
        shutil.copy2(target, backup)
    fd, tmp_name = tempfile.mkstemp(prefix=".kitz-agent-", suffix=".yaml", dir=model_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(desired)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp_name, 0o644)
        os.replace(tmp_name, target)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
    return InstallResult(path=target, changed=True, backup=backup)


def localai_has_model(payload: dict[str, Any], model_name: str = MODEL_NAME) -> bool:
    data = payload.get("data")
    if not isinstance(data, list):
        return False
    return any(isinstance(item, dict) and item.get("id") == model_name for item in data)


def parse_chat_content(payload: dict[str, Any]) -> str:
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("OpenAI-compatible chat response did not contain choices[0].message.content") from exc
    if not isinstance(content, str):
        raise ValueError("OpenAI-compatible chat response content was not text")
    return content


def _json_request(url: str, *, payload: dict[str, Any] | None = None, timeout: float = 5.0) -> dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    method = "GET"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
        method = "POST"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    decoded = json.loads(raw)
    if not isinstance(decoded, dict):
        raise ValueError(f"Expected JSON object from {url}")
    return decoded


def _wait_json(url: str, *, timeout_seconds: int = 60) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            return _json_request(url, timeout=3.0)
        except (OSError, ValueError, urllib.error.URLError) as exc:
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"Timed out waiting for {url}: {last_error}")


def _restart_localai() -> None:
    subprocess.run(["osascript", "-e", 'tell application "LocalAI" to quit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    time.sleep(2)
    subprocess.run(["pkill", "-f", "local-ai"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    result = subprocess.run(["open", "-a", "LocalAI"], check=False)
    if result.returncode != 0:
        raise RuntimeError("Could not start LocalAI.app")


def verify_agent_core() -> None:
    payload = _wait_json(AGENT_CORE_HEALTH_URL, timeout_seconds=20)
    status = payload.get("status")
    if status not in (None, "ok", "healthy", "ONLINE", "online"):
        raise RuntimeError(f"Agent Core health returned unexpected status: {status!r}")


def verify_localai_model(*, restart_if_missing: bool = True) -> None:
    models = _wait_json(LOCALAI_MODELS_URL, timeout_seconds=30)
    if localai_has_model(models):
        return
    if not restart_if_missing:
        raise RuntimeError(f"{MODEL_NAME} is not visible in LocalAI")
    _restart_localai()
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        try:
            models = _json_request(LOCALAI_MODELS_URL, timeout=5)
            if localai_has_model(models):
                return
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError(f"{MODEL_NAME} did not appear in LocalAI after restart")


def verify_chat_bridge() -> str:
    payload = _json_request(
        LOCALAI_CHAT_URL,
        payload={"model": MODEL_NAME, "messages": [{"role": "user", "content": "Antworte exakt mit: KITZ BRIDGE OK"}], "temperature": 0, "max_tokens": 64},
        timeout=180,
    )
    return parse_chat_content(payload)


def discover_models_dir(*, home: Path | None = None, env: dict[str, str] | None = None) -> Path:
    home = (home or Path.home()).expanduser()
    env = dict(os.environ if env is None else env)
    configured = env.get("LOCALAI_MODELS_PATH") or env.get("MODELS_PATH")
    if configured:
        return Path(configured).expanduser()
    default = home / ".localai" / "models"
    if default.exists():
        return default
    localai_root = home / ".localai"
    if localai_root.exists():
        for marker in ("qwen3-fast.yaml", "qwen3-reasoning.yaml", "nomic-embed-text.yaml"):
            matches = sorted(localai_root.rglob(marker))
            if matches:
                return matches[0].parent
    return default


def default_models_dir() -> Path:
    return discover_models_dir()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install the KITZ Agent Core bridge into LocalAI")
    parser.add_argument("--models-dir", type=Path, default=default_models_dir())
    parser.add_argument("--no-restart", action="store_true")
    parser.add_argument("--no-chat-test", action="store_true")
    args = parser.parse_args(argv)
    result = install_bridge_config(args.models_dir)
    print(f"[localai] bridge config: {result.path}")
    print(f"[localai] config {'updated' if result.changed else 'already current'}")
    if result.backup:
        print(f"[localai] previous config backup: {result.backup}")
    verify_agent_core()
    print("[localai] Agent Core: ONLINE")
    verify_localai_model(restart_if_missing=not args.no_restart)
    print(f"[localai] LocalAI model: {MODEL_NAME} VISIBLE")
    if not args.no_chat_test:
        response = verify_chat_bridge().strip()
        print(f"[localai] bridge response: {response}")
    print("[localai] KITZ Agent Core integration ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
