from pathlib import Path
import importlib.util

MODULE = Path(__file__).resolve().parents[1] / 'release-overrides' / 'patch_start_ollama.py'


def load_module():
    spec = importlib.util.spec_from_file_location('patch_start_ollama', MODULE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def old_start_text() -> str:
    return '''import shutil\nimport subprocess\n\ndef main():\n    failed = False\n    for app in ("LocalAI", "Ollama"):\n        failed = subprocess.run(["open", "-a", app], check=False).returncode != 0 or failed\n    return 1 if failed else 0\n'''


def test_patch_replaces_app_only_ollama_start_with_cli_aware_start(tmp_path):
    start = tmp_path / 'start.py'
    start.write_text(old_start_text(), encoding='utf-8')

    module = load_module()
    assert module.patch_file(start) is True
    text = start.read_text(encoding='utf-8')
    assert 'for app in ("LocalAI", "Ollama")' not in text
    assert 'shutil.which("ollama")' in text
    assert '[ollama, "ps"]' in text
    assert '[ollama, "serve"]' in text
    assert 'open", "-Ra", "Ollama"' in text
    assert 'import time' in text


def test_patch_is_idempotent(tmp_path):
    start = tmp_path / 'start.py'
    start.write_text(old_start_text(), encoding='utf-8')

    module = load_module()
    assert module.patch_file(start) is True
    once = start.read_text(encoding='utf-8')
    assert module.patch_file(start) is False
    assert start.read_text(encoding='utf-8') == once
