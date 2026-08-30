from pathlib import Path
import tomllib


def test_core_uses_slim_pydantic_ai_and_mcp1_boundary():
    data = tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))
    dependencies = data['project']['dependencies']

    assert any(dep.startswith('pydantic-ai-slim[openai]>=2.33') for dep in dependencies)
    assert not any(dep.startswith('pydantic-ai>=') for dep in dependencies)

    assert any(dep.startswith('mcp[cli]>=1.24') and '<2' in dep for dep in dependencies)
    assert not any(dep.startswith('mcp[cli]>=2') for dep in dependencies)

    assert not any(dep.startswith('browser-use') for dep in dependencies)
