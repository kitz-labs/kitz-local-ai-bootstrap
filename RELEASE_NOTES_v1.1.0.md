# KITZ Local AI v1.1.0 — Native LocalAI Backend

`kitz-agent` no longer uses the LocalAI `cloud-proxy` backend or the temporary HTTP streaming bridge on port 8788.

The new route is:

`LocalAI UI -> kitz-native gRPC backend -> KITZ Agent Core (:8787) -> model/tools`

Changes:
- native LocalAI gRPC backend for `kitz-agent`
- registration through LocalAI `configuration/external_backends.json`
- keeps existing Qwen `cloud-proxy` configurations unchanged
- removes the legacy port-8788 stream bridge
- adapts LocalAI `PredictStream` to the non-streaming Agent Core v1 endpoint
- preserves existing external gRPC backend registrations
- backs up the previous `kitz-agent.yaml`
- performs a real end-to-end streaming chat verification before reporting success
