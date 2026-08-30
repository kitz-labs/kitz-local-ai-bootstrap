#!/usr/bin/env bash
set -euo pipefail

printf '\n==============================================\n'
printf ' KITZ Local AI v1.0.6 - Streaming Chat Fix\n'
printf '==============================================\n\n'

for cmd in curl python3 open launchctl; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: $cmd missing" >&2; exit 1; }
done
command -v uv >/dev/null 2>&1 || { echo 'ERROR: uv missing' >&2; exit 1; }

ROOT="$HOME/KITZLABS-AI/agent-core"
RUNTIME_DIR="$ROOT/runtime"
LOG_DIR="$HOME/KITZLABS-AI/logs"
LAUNCH_DIR="$HOME/Library/LaunchAgents"
LABEL="ai.kitz.localai-stream-bridge"
PLIST="$LAUNCH_DIR/$LABEL.plist"
BRIDGE_PY="$RUNTIME_DIR/localai_stream_bridge.py"
PYTHON="$ROOT/.venv/bin/python"
DOMAIN="gui/$(id -u)"

mkdir -p "$RUNTIME_DIR" "$LOG_DIR" "$LAUNCH_DIR"
if [ ! -x "$PYTHON" ]; then
  PYTHON="$(command -v python3)"
fi

if ! curl -fsS --max-time 5 http://127.0.0.1:8787/health >/dev/null 2>&1; then
  echo '[v1.0.6] Agent Core is offline; starting KITZ services...'
  kitz-start || true
fi
curl -fsS --max-time 10 http://127.0.0.1:8787/health >/dev/null 2>&1 || {
  echo 'ERROR: Agent Core is not reachable on 127.0.0.1:8787.' >&2
  exit 1
}
echo '[v1.0.6] Agent Core: ONLINE'

echo '[v1.0.6] Installing streaming compatibility bridge...'
tmp_bridge="$(mktemp "${TMPDIR:-/tmp}/kitz-stream-bridge.XXXXXX.py")"
tmp_installer="$(mktemp "${TMPDIR:-/tmp}/kitz-localai-installer.XXXXXX.py")"
capfile="$(mktemp "${TMPDIR:-/tmp}/kitz-localai-capabilities.XXXXXX.json")"
stream_body="$(mktemp "${TMPDIR:-/tmp}/kitz-localai-stream.XXXXXX.txt")"
trap 'rm -f "$tmp_bridge" "$tmp_installer" "$capfile" "$stream_body"' EXIT

curl -fsSL https://raw.githubusercontent.com/kitz-labs/kitz-local-ai-bootstrap/v1.0.6/release-overrides/localai_stream_bridge.py -o "$tmp_bridge"
"$PYTHON" -m py_compile "$tmp_bridge"
install -m 0644 "$tmp_bridge" "$BRIDGE_PY"

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$BRIDGE_PY</string>
    <string>--host</string><string>127.0.0.1</string>
    <string>--port</string><string>8788</string>
  </array>
  <key>WorkingDirectory</key><string>$ROOT</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$LOG_DIR/localai-stream-bridge.log</string>
  <key>StandardErrorPath</key><string>$LOG_DIR/localai-stream-bridge.err.log</string>
  <key>EnvironmentVariables</key>
  <dict><key>PYTHONUNBUFFERED</key><string>1</string></dict>
</dict>
</plist>
PLIST

launchctl bootout "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "$DOMAIN" "$PLIST"
launchctl kickstart -k "$DOMAIN/$LABEL" >/dev/null 2>&1 || true

echo '[v1.0.6] Waiting for streaming bridge on :8788...'
i=0
while [ "$i" -lt 30 ]; do
  if curl -fsS --max-time 2 http://127.0.0.1:8788/health >/dev/null 2>&1; then
    break
  fi
  i=$((i + 1))
  sleep 1
done
curl -fsS --max-time 3 http://127.0.0.1:8788/health >/dev/null
echo '[v1.0.6] Streaming bridge: ONLINE'

echo '[v1.0.6] Pointing LocalAI kitz-agent to streaming bridge...'
curl -fsSL https://raw.githubusercontent.com/kitz-labs/kitz-local-ai-bootstrap/v1.0.6/release-overrides/install_localai_bridge.py -o "$tmp_installer"
uv run --no-project --python 3.12 python "$tmp_installer" --no-restart --no-chat-test

echo '[v1.0.6] Restarting LocalAI safely...'
osascript -e 'tell application "LocalAI" to quit' >/dev/null 2>&1 || true
sleep 2
pkill -x local-ai >/dev/null 2>&1 || true
open -a LocalAI

echo '[v1.0.6] Waiting for LocalAI on :8080...'
i=0
while [ "$i" -lt 90 ]; do
  if curl -fsS --max-time 3 http://127.0.0.1:8080/v1/models >/dev/null 2>&1; then
    break
  fi
  i=$((i + 1))
  sleep 1
done
curl -fsS --max-time 5 http://127.0.0.1:8080/v1/models >/dev/null 2>&1 || {
  echo 'ERROR: LocalAI did not come back online.' >&2
  exit 1
}
echo '[v1.0.6] LocalAI: ONLINE'

curl -fsS --max-time 10 http://127.0.0.1:8080/api/models/capabilities -o "$capfile"
python3 - "$capfile" <<'PY'
import json
import sys
from pathlib import Path
payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
items = payload.get('data', []) if isinstance(payload, dict) else []
model = next((m for m in items if isinstance(m, dict) and m.get('id') == 'kitz-agent'), None)
if model is None:
    raise SystemExit('ERROR: kitz-agent missing from /api/models/capabilities')
capabilities = model.get('capabilities') or []
if 'FLAG_CHAT' not in capabilities:
    raise SystemExit(f'ERROR: kitz-agent has no FLAG_CHAT capability: {capabilities}')
print('[v1.0.6] kitz-agent capability: FLAG_CHAT')
PY

echo '[v1.0.6] Running real LocalAI streaming chat test...'
http_code="$(curl -sS -N --max-time 240 -o "$stream_body" -w '%{http_code}' \
  http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"kitz-agent","messages":[{"role":"user","content":"Antworte kurz mit KITZ_STREAM_OK"}],"stream":true,"stream_options":{"include_usage":true}}')"

if [ "$http_code" != "200" ]; then
  echo "ERROR: streaming chat returned HTTP $http_code" >&2
  cat "$stream_body" >&2
  exit 1
fi

grep -q '^data: ' "$stream_body" || { echo 'ERROR: response was not SSE.' >&2; cat "$stream_body" >&2; exit 1; }
grep -q 'data: \[DONE\]' "$stream_body" || { echo 'ERROR: SSE stream had no [DONE] frame.' >&2; cat "$stream_body" >&2; exit 1; }

echo '[v1.0.6] VERIFIED: LocalAI -> kitz-agent -> streaming bridge -> Agent Core returned HTTP 200 + SSE'
printf '\n==============================================\n'
printf ' KITZ LocalAI streaming chat is ready\n'
printf ' Open: http://localhost:8080/app/chat\n'
printf ' Select: kitz-agent\n'
printf '==============================================\n'
