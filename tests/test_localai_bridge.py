import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'release-overrides' / 'install_localai_bridge.py'
spec = importlib.util.spec_from_file_location('install_localai_bridge', MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class LocalAIBridgeTests(unittest.TestCase):
    def test_render_bridge_config_is_chat_model_and_points_to_stream_bridge(self):
        text = mod.render_bridge_config()
        self.assertIn('name: kitz-agent', text)
        self.assertIn('known_usecases:\n  - chat', text)
        self.assertIn('backend: cloud-proxy', text)
        self.assertIn('upstream_url: http://127.0.0.1:8788/v1/chat/completions', text)
        self.assertIn('upstream_model: kitz-agent', text)

    def test_backup_is_outside_models_directory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / '.localai'
            models = root / 'models'
            models.mkdir(parents=True)
            target = models / 'kitz-agent.yaml'
            target.write_text('old config\n', encoding='utf-8')
            result = mod.install_bridge_config(models, now=datetime(2026, 8, 30, 8, 50, 0))
            self.assertTrue(result.changed)
            self.assertIsNotNone(result.backup)
            self.assertEqual(result.backup.parent, root / 'backups' / 'kitz-agent')
            self.assertFalse(any(models.glob('kitz-agent.yaml.pre-*')))

    def test_migrate_legacy_backups_removes_fake_model_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / '.localai'
            models = root / 'models'
            models.mkdir(parents=True)
            legacy = models / 'kitz-agent.yaml.pre-v1.0.4-20260830-082758'
            legacy.write_text('old config', encoding='utf-8')
            moved = mod.migrate_legacy_backups(models)
            self.assertEqual(len(moved), 1)
            self.assertFalse(legacy.exists())
            self.assertTrue(moved[0].exists())
            self.assertEqual(moved[0].parent, root / 'backups' / 'kitz-agent')

    def test_install_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            models = Path(td) / '.localai' / 'models'
            first = mod.install_bridge_config(models)
            second = mod.install_bridge_config(models)
            self.assertTrue(first.changed)
            self.assertFalse(second.changed)


if __name__ == '__main__':
    unittest.main()
