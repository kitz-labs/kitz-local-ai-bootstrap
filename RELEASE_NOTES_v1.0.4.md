# KITZ Local AI v1.0.4

LocalAI integration release:

- Adds `kitz-agent` as a LocalAI `cloud-proxy` model.
- Routes LocalAI chat requests to the local KITZ Agent Core at `http://127.0.0.1:8787/v1/chat/completions`.
- Keeps the direct Qwen model aliases available in LocalAI.
- Detects the active LocalAI models directory instead of assuming a hard-coded path.
- Backs up any previous `kitz-agent.yaml` before replacing it.
- Restarts LocalAI only when the new model is not yet visible.
- Verifies Agent Core health, LocalAI model visibility and an end-to-end chat request through LocalAI.
- Disables LocalAI cloud-proxy PII middleware for this strictly local loopback upstream to avoid unnecessary detector overhead.

This update is designed for an existing KITZ v1.0.3 installation and does not reinstall the full media/model stack.
