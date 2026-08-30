#!/usr/bin/env bash
set -euo pipefail

printf '\n==============================================\n'
printf ' KITZ Local AI v1.0.4 - LocalAI Integration\n'
printf '==============================================\n\n'

command -v curl >/dev/null 2>&1 || { echo 'ERROR: curl missing' >&2; exit 1; }
command -v uv >/dev/null 2>&1 || { echo 'ERROR: uv missing' >&2; exit 1; }

if command -v kitz-start >/dev/null 2>&1; then
  echo '[v1.0.4] Ensuring KITZ services are running...'
  kitz-start
fi

tmp="$(mktemp "${TMPDIR:-/tmp}/kitz-localai-bridge.XXXXXX.py")"
trap 'rm -f "$tmp"' EXIT

bridge_url='https://raw.githubusercontent.com/kitz-labs/kitz-local-ai-bootstrap/v1.0.4/release-overrides/install_localai_bridge.py'
echo '[v1.0.4] Downloading LocalAI bridge...'
curl -fsSL "$bridge_url" -o "$tmp"

echo '[v1.0.4] Installing and verifying kitz-agent in LocalAI...'
uv run --no-project --python 3.12 python "$tmp"

printf '\n==============================================\n'
printf ' LocalAI integration finished\n'
printf ' Open: http://localhost:8080/app/chat\n'
printf ' Select model: kitz-agent\n'
printf '==============================================\n'
