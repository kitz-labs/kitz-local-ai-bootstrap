from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCHER = ROOT / 'release-overrides' / 'patch_agent_timeout.py'
UPDATE = ROOT / 'update-localai-v1.1.1.sh'
INSTALL = ROOT / 'install.sh'
VERSION = ROOT / 'VERSION'


def test_timeout_patcher_exists_and_targets_240_seconds():
    text = PATCHER.read_text(encoding='utf-8')
    assert 'timeout: float = 30.0,' in text
    assert 'timeout: float = 240.0,' in text
    assert 'already patched' in text


def test_v111_updater_applies_timeout_patch_and_verifies_it():
    text = UPDATE.read_text(encoding='utf-8')
    assert 'KITZ_RELEASE_REF:-v1.1.1' in text
    assert 'patch_agent_timeout.py' in text
    assert 'timeout == 240.0' in text
    assert 'KITZ_TIMEOUT_FIXED' in text


def test_fresh_install_applies_timeout_patch_before_tool_install():
    text = INSTALL.read_text(encoding='utf-8')
    assert 'KITZ Local AI v1.1.1 Bootstrap' in text
    assert 'KITZ_REPO_REF:-v1.1.1' in text
    assert 'patch_agent_timeout.py' in text
    assert text.index('patch_agent_timeout.py') < text.index('uv tool install --force')


def test_release_version_is_v111():
    assert VERSION.read_text(encoding='utf-8').strip() == '1.1.1'
