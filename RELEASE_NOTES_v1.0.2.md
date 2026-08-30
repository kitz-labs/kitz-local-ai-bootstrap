# KITZ Local AI v1.0.2

Dependency-boundary hotfix:

- Use `pydantic-ai-slim[openai]` instead of the full `pydantic-ai` meta-package.
- Keep the KITZ core on the stable MCP 1.x line (`mcp[cli]>=1.24,<2`) required by the current Pydantic AI/FastMCP stack.
- Keep Browser Use isolated in its own `uv tool` environment.
- Preserve Playwright in the KITZ core.
- Add a regression test for these dependency boundaries.

MCP 2.x remains a planned separate-service / future-upgrade path once the surrounding agent stack is compatible.
