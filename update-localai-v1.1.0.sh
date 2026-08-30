#!/usr/bin/env bash
set -euo pipefail

printf '\n==============================================\n'
printf ' KITZ Local AI v1.1.0 - KITZ Native Backend\n'
printf '==============================================\n\n'

for cmd in curl python3 open launchctl osascript; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: $cmd missing" >&2; exit 1; }
done
command -v uv >/dev/null 2>&1 || { echo 'ERROR: uv missing' >&2; exit 1; }

REF="${KITZ_RELEASE_REF:-v1.1.0}"
RAW="https://raw.githubusercontent.com/kitz-labs/kitz-local-ai-bootstrap/$REF"
TMP_BASE="${TMPDIR:-/tmp}"
BACKEND_TMP="$(mktemp "$TMP_BASE/kitz-native-backend.XXXXXX")"
INSTALLER_TMP="$(mktemp "$TMP_BASE/kitz-native-installer.XXXXXX")"
CHAT_BODY="$(mktemp "$TMP_BASE/kitz-native-chat.XXXXXX")"
trap 'rm -f "$BACKEND_TMP" "$INSTALLER_TMP" "$CHAT_BODY"' EXIT

if ! curl -fsS --max-time 5 http://127.0.0.1:8787/health >/dev/null 2>&1; then
  echo '[v1.1.0] Agent Core offline -> starting KITZ...'
  kitz-start || true
fi
curl -fsS --max-time 15 http://127.0.0.1:8787/health >/dev/null
printf '[v1.1.0] Agent Core: ONLINE\n'

printf '[v1.1.0] Installing native gRPC backend...\n'
curl -fsSL "$RAW/release-overrides/kitz_native_backend.py" -o "$BACKEND_TMP"
curl -fsSL "$RAW/release-overrides/install_kitz_native.py" -o "$INSTALLER_TMP"
python3 -m py_compile "$BACKEND_TMP" "$INSTALLER_TMP"
python3 "$INSTALLER_TMP" --backend-source "$BACKEND_TMP"

LABEL='ai.kitz.localai-stream-bridge'
DOMAIN="gui/$(id -u)"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
launchctl bootout "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
rm -f "$PLIST"
pkill -f 'localai_stream_bridge.py' >/dev/null 2>&1 || true
printf '[v1.1.0] Legacy port-8788 bridge: REMOVED\n'

printf '[v1.1.0] Restarting LocalAI...\n'
osascript -e 'tell application "LocalAI" to quit' >/dev/null 2>&1 || true
sleep 3
pkill -x local-ai >/dev/null 2>&1 || true
open -a LocalAI

printf '[v1.1.0] Waiting for LocalAI :8080...\n'
i=0
while [ "$i" -lt 120 ]; do
  if curl -fsS --max-time 3 http://127.0.0.1:8080/v1/models >/dev/null 2>&1; then
    break
  fi
  i=$((i + 1))
  sleep 1
done
curl -fsS --max-time 5 http://127.0.0.1:8080/v1/models >/dev/null || { echo 'ERROR: LocalAI did not come online.' >&2; exit 1; }
printf '[v1.1.0] LocalAI: ONLINE\n'

curl -fsS http://127.0.0.1:8080/v1/models | python3 -c 'import json,sys; d=json.load(sys.stdin); ids={x.get("id") for x in d.get("data",[])}; assert "kitz-agent" in ids, ids; print("[v1.1.0] kitz-agent: VISIBLE")'

python3 - <<'PY'
import json
from pathlib import Path
p=Path.home()/'.localai'/'configuration'/'external_backends.json'
d=json.loads(p.read_text())
assert 'kitz-native' in d, d
assert d['kitz-native'].endswith('/.localai/backends/kitz-native/run.sh'), d
print('[v1.1.0] kitz-native registration: OK')
PY

printf '[v1.1.0] Testing LocalAI -> native gRPC -> Agent Core...\n'
code="$(curl -sS -N --max-time 240 -o "$CHAT_BODY" -w '%{http_code}' \
  http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"kitz-agent","messages":[{"role":"user","content":"Antworte nur mit KITZ_NATIVE_OK"}],"stream":true,"max_tokens":32}')"
if [ "$code" != '200' ]; then
  echo "ERROR: native kitz-agent returned HTTP $code" >&2
  cat "$CHAT_BODY" >&2
  exit 1
fi
grep -q '^data:' "$CHAT_BODY" || { echo 'ERROR: no SSE response from native backend' >&2; cat "$CHAT_BODY" >&2; exit 1; }
grep -q 'KITZ_NATIVE_OK' "$CHAT_BODY" || { echo 'ERROR: native backend answered but expected KITZ_NATIVE_OK was not found' >&2; cat "$CHAT_BODY" >&2; exit 1; }

printf '\n==============================================\n'
printf ' KITZ NATIVE BACKEND READY\n'
printf ' LocalAI -> gRPC kitz-native -> Agent Core\n'
printf ' kitz-agent no longer uses cloud-proxy/8788\n'
printf ' Open: http://localhost:8080/app/chat\n'
printf '==============================================\n'
