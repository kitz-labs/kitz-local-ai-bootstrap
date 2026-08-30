#!/usr/bin/env bash
set -euo pipefail

printf '\n==============================================\n'
printf ' KITZ Local AI v1.0.5 - Chat Selector Fix\n'
printf '==============================================\n\n'

command -v curl >/dev/null 2>&1 || { echo 'ERROR: curl missing' >&2; exit 1; }
command -v uv >/dev/null 2>&1 || { echo 'ERROR: uv missing' >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo 'ERROR: python3 missing' >&2; exit 1; }

if ! curl -fsS --max-time 5 http://127.0.0.1:8787/health >/dev/null 2>&1; then
  echo '[v1.0.5] Agent Core is offline; starting KITZ services...'
  kitz-start || true
fi

tmp="$(mktemp "${TMPDIR:-/tmp}/kitz-localai-chat-fix.XXXXXX.py")"
capfile="$(mktemp "${TMPDIR:-/tmp}/kitz-localai-capabilities.XXXXXX.json")"
trap 'rm -f "$tmp" "$capfile"' EXIT

bridge_url='https://raw.githubusercontent.com/kitz-labs/kitz-local-ai-bootstrap/v1.0.5/release-overrides/install_localai_bridge.py'
echo '[v1.0.5] Installing LocalAI chat capability for kitz-agent...'
curl -fsSL "$bridge_url" -o "$tmp"
uv run --no-project --python 3.12 python "$tmp" --no-restart --no-chat-test

echo '[v1.0.5] Restarting LocalAI so capabilities are reloaded...'
osascript -e 'tell application "LocalAI" to quit' >/dev/null 2>&1 || true
sleep 2
pkill -x local-ai >/dev/null 2>&1 || true
open -a LocalAI

echo '[v1.0.5] Waiting for LocalAI...'
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
    raise SystemExit(f"ERROR: kitz-agent still has no FLAG_CHAT capability: {capabilities}")
print('[v1.0.5] VERIFIED: kitz-agent has FLAG_CHAT')
PY

printf '\n==============================================\n'
printf ' kitz-agent is now eligible for LocalAI Chat\n'
printf ' Open: http://localhost:8080/app/chat\n'
printf ' Search/select: kitz-agent\n'
printf '==============================================\n'
