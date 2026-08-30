# KITZ Local AI v1.0.1

Fixes the installer dependency conflict between MCP v2 in the KITZ core and Browser Use, which pins MCP 1.x.

- Keeps `mcp[cli]>=2.0,<3` in the KITZ core.
- Removes `browser-use` from the core dependency set.
- Installs `browser-use[core]==0.13.8` in an isolated `uv tool` environment.
- Keeps Playwright in the core runtime.
- Adds a regression test for the dependency boundary.
