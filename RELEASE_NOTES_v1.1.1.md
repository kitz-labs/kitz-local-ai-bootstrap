# KITZ Local AI v1.1.1

Reliability release for cold-start inference through the KITZ Agent Core.

## Root cause fixed

The Agent Core `LocalAIClient` previously used a 30 second HTTP timeout. On Apple Silicon, a cold Ollama load of `qwen3:8b` can take well over two minutes. LocalAI would eventually complete successfully, but Agent Core aborted first and returned HTTP 500.

## Changes

- Raises the Agent Core LocalAI client timeout from 30 seconds to 240 seconds.
- Adds an idempotent `release-overrides/patch_agent_timeout.py` patcher.
- Applies the timeout patch during fresh bootstrap before `uv tool install`.
- Adds `update-localai-v1.1.1.sh` for existing installations.
- The updater patches both the source tree and the active `uv tool` installation.
- Creates timestamped backups before modifying an existing installation.
- Restarts Agent Core and verifies the active timeout value.
- Performs an end-to-end `LocalAI -> kitz-agent -> Agent Core -> qwen3-fast -> Ollama` verification.
- Rolls back modified files if the patch, restart, or end-to-end verification fails.
- Adds regression tests locking the v1.1.1 release behavior.

## One-command update

```bash
curl -fsSL https://raw.githubusercontent.com/kitz-labs/kitz-local-ai-bootstrap/v1.1.1/update-localai-v1.1.1.sh | bash
```
