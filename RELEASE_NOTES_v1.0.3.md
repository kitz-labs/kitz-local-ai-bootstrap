# KITZ Local AI v1.0.3

Ollama start compatibility hotfix:

- Detect an existing Homebrew/CLI Ollama installation before trying `Ollama.app`.
- Treat a running `ollama serve` process/API as ready instead of failing on a missing macOS app bundle.
- Start `ollama serve` in the background when the CLI exists but the server is not ready, then wait up to 30 seconds.
- Fall back to `Ollama.app` only when no CLI is available.
- Add an idempotent runtime patch plus regression tests.
