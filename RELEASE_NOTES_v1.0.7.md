# KITZ Local AI v1.0.7

## macOS mktemp compatibility fix

Fixes the v1.0.6 updater failure on macOS where BSD `mktemp` rejected templates such as `XXXXXX.py` with `File exists`.

Changes:
- all temporary-file templates now end directly in `XXXXXX`
- keeps the v1.0.6 streaming bridge architecture
- keeps `kitz-agent` chat capability and LocalAI integration
- keeps the real LocalAI streaming end-to-end verification

No model downloads or full reinstall are required.
