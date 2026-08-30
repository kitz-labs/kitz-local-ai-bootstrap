from pathlib import Path
import tomllib


def test_browser_use_is_not_in_core_dependency_set():
    data = tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))
    dependencies = data['project']['dependencies']
    assert any(dep.startswith('mcp[cli]>=2.0') for dep in dependencies)
    assert not any(dep.startswith('browser-use') for dep in dependencies)
