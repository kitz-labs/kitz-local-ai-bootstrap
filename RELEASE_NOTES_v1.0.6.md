# KITZ Local AI v1.0.6

LocalAI streaming chat compatibility release.

- Adds a local streaming compatibility bridge on `127.0.0.1:8788`.
- Converts LocalAI's `stream: true` requests into the Agent Core's current non-streaming request format and converts the response back to OpenAI-compatible SSE.
- Keeps `kitz-agent` exposed as a `FLAG_CHAT` LocalAI model.
- Moves legacy `kitz-agent.yaml.pre-*` backups out of the LocalAI models directory so they are not detected as fake models.
- Uses exact-process `pkill -x local-ai` during controlled LocalAI restarts.
- Adds unit tests for SSE conversion, bridge routing, backup migration, and chat model configuration.
