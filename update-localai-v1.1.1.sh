#!/usr/bin/env bash
set -euo pipefail

printf '\n==============================================\n'
printf ' KITZ Local AI v1.1.1 - Agent Timeout Fix\n'
printf '==============================================\n\n'

for cmd in curl python3 lsof open; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: $cmd missing" >&2; exit 1; }
done

REF="${KITZ_RELEASE_REF:-v1.1.1}"
RAW="https://raw.githubusercontent.com/kitz-labs/kitz-local-ai-bootstrap/$REF"
PATCHER="$(mktemp "${TMPDIR:-/tmp}/kitz-agent-timeout.XXXXXX")"
CHAT_BODY="$(mktemp "${TMPDIR:-/tmp}/kitz-v111-chat.XXXXXX")"
trap 'rm -f "$PATCHER" "$CHAT_BODY"' EXIT

curl -fsSL "$RAW/release-overrides/patch_agent_timeout.py" -o "$PATCHER"
python3 -m py_compile "$PATCHER"

REPO_FILE="${KITZ_AGENT_CORE_SOURCE:-$HOME/KITZLABS-AI/agent-core/src/kitz_core/localai.py}"

KITZ_BIN="$(command -v kitz-agent-api 2>/dev/null || true)"
if [ -n "$KITZ_BIN" ]; then
  SHEBANG="$(head -n 1 "$KITZ_BIN" 2>/dev/null || true)"
  KITZ_PY="${SHEBANG#\#!}"
else
  KITZ_PY=""
fi
if [ -z "$KITZ_PY" ] || [ ! -x "$KITZ_PY" ]; then
  KITZ_PY="$HOME/.local/share/uv/tools/kitz-local-ai/bin/python"
fi
[ -x "$KITZ_PY" ] || { echo 'ERROR: KITZ Python runtime not found.' >&2; exit 1; }

ACTIVE_FILE="$($KITZ_PY - <<'PY'
import kitz_core.localai
print(kitz_core.localai.__file__)
PY
)"

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUPS=()
rollback() {
  local entry original backup
  for entry in "${BACKUPS[@]:-}"; do
    original="${entry%%|*}"
    backup="${entry#*|}"
    [ -f "$backup" ] && cp "$backup" "$original" || true
  done
}

for file in "$REPO_FILE" "$ACTIVE_FILE"; do
  [ -f "$file" ] || { echo "ERROR: expected Agent Core file missing: $file" >&2; exit 1; }
  duplicate=0
  for entry in "${BACKUPS[@]:-}"; do
    [ "${entry%%|*}" = "$file" ] && duplicate=1
  done
  if [ "$duplicate" -eq 0 ]; then
    backup="$file.backup-v1.1.1-$STAMP"
    cp "$file" "$backup"
    BACKUPS+=("$file|$backup")
  fi
done

if ! python3 "$PATCHER" "$REPO_FILE" "$ACTIVE_FILE"; then
  rollback
  echo 'ERROR: timeout patch failed; rollback completed.' >&2
  exit 1
fi

if ! "$KITZ_PY" - <<'PY'
import inspect
import importlib
import kitz_core.localai
importlib.reload(kitz_core.localai)
timeout = inspect.signature(kitz_core.localai.LocalAIClient.__init__).parameters['timeout'].default
print(f'[v1.1.1] Active Agent Core timeout: {timeout}s')
assert timeout == 240.0, timeout
PY
then
  rollback
  echo 'ERROR: active timeout verification failed; rollback completed.' >&2
  exit 1
fi

OLD_PID="$(lsof -tiTCP:8787 -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
if [ -n "$OLD_PID" ]; then
  kill -TERM "$OLD_PID" >/dev/null 2>&1 || true
  sleep 3
fi

if ! curl -fsS --max-time 2 http://127.0.0.1:8787/health >/dev/null 2>&1; then
  command -v kitz-start >/dev/null 2>&1 && kitz-start >/dev/null 2>&1 || true
fi

for _ in $(seq 1 30); do
  curl -fsS --max-time 2 http://127.0.0.1:8787/health >/dev/null 2>&1 && break
  sleep 1
done
curl -fsS --max-time 3 http://127.0.0.1:8787/health >/dev/null || {
  rollback
  echo 'ERROR: Agent Core did not return after restart; rollback completed.' >&2
  exit 1
}
printf '[v1.1.1] Agent Core: ONLINE\n'

if ! curl -fsS --max-time 3 http://127.0.0.1:8080/v1/models >/dev/null 2>&1; then
  printf '[v1.1.1] LocalAI offline -> starting LocalAI...\n'
  open -a LocalAI >/dev/null 2>&1 || true
fi

printf '[v1.1.1] Waiting for LocalAI :8080...\n'
i=0
while [ "$i" -lt 120 ]; do
  if curl -fsS --max-time 3 http://127.0.0.1:8080/v1/models >/dev/null 2>&1; then
    break
  fi
  i=$((i + 1))
  sleep 1
done
curl -fsS --max-time 5 http://127.0.0.1:8080/v1/models >/dev/null || {
  rollback
  echo 'ERROR: LocalAI did not come online; rollback completed.' >&2
  exit 1
}
printf '[v1.1.1] LocalAI: ONLINE\n'

code="$(curl -sS --max-time 240 -o "$CHAT_BODY" -w '%{http_code}' \
  http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"kitz-agent","messages":[{"role":"user","content":"Antworte nur mit KITZ_TIMEOUT_FIXED"}],"stream":false,"max_tokens":32}')"
if [ "$code" != '200' ]; then
  rollback
  echo "ERROR: kitz-agent returned HTTP $code; rollback completed." >&2
  cat "$CHAT_BODY" >&2
  exit 1
fi

grep -q 'KITZ_TIMEOUT_FIXED' "$CHAT_BODY" || {
  rollback
  echo 'ERROR: end-to-end response did not contain KITZ_TIMEOUT_FIXED; rollback completed.' >&2
  cat "$CHAT_BODY" >&2
  exit 1
}

printf '\n==============================================\n'
printf ' KITZ Local AI v1.1.1 READY\n'
printf ' Agent Core timeout: 240 seconds\n'
printf ' LocalAI -> kitz-agent -> Agent Core: OK\n'
printf '==============================================\n'
