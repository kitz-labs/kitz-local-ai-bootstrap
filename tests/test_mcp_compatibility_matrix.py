from pathlib import Path
import tomllib


def test_pydantic_ai_harness_compatible_mcp_matrix():
    data = tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))
    dependencies = data['project']['dependencies']

    slim = next(dep for dep in dependencies if dep.startswith('pydantic-ai-slim[openai]'))
    mcp = next(dep for dep in dependencies if dep.startswith('mcp[cli]'))

    assert '>=2.33.0' in slim and '<3' in slim
    assert '>=1.24' in mcp and '<2' in mcp
    assert not any(dep.startswith('pydantic-ai>=') for dep in dependencies)
    assert not any(dep.startswith('browser-use') for dep in dependencies)
