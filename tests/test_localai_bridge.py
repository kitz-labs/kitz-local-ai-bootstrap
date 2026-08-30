import tempfile
import unittest
from pathlib import Path

from release_overrides.install_localai_bridge import (
    discover_models_dir,
    install_bridge_config,
    localai_has_model,
    parse_chat_content,
    render_bridge_config,
)


class LocalAIBridgeTests(unittest.TestCase):
    def test_render_bridge_config_points_localai_to_agent_core(self):
        text = render_bridge_config()
        self.assertIn('name: kitz-agent', text)
        self.assertIn('known_usecases:\n  - chat\n', text)
        self.assertIn('backend: cloud-proxy', text)
        self.assertIn('mode: passthrough', text)
        self.assertIn('provider: openai', text)
        self.assertIn('upstream_url: http://127.0.0.1:8787/v1/chat/completions', text)
        self.assertIn('upstream_model: kitz-agent', text)
        self.assertIn('request_timeout_seconds: 600', text)
        self.assertIn('enabled: false', text)

    def test_install_bridge_config_preserves_existing_config_with_backup(self):
        with tempfile.TemporaryDirectory() as td:
            model_dir = Path(td)
            target = model_dir / 'kitz-agent.yaml'
            target.write_text('old config\n', encoding='utf-8')
            result = install_bridge_config(model_dir)
            self.assertTrue(result.changed)
            self.assertEqual(result.path, target)
            self.assertIn('backend: cloud-proxy', target.read_text(encoding='utf-8'))
            backups = list(model_dir.glob('kitz-agent.yaml.pre-v1.0.4-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding='utf-8'), 'old config\n')

    def test_install_bridge_config_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            model_dir = Path(td)
            first = install_bridge_config(model_dir)
            second = install_bridge_config(model_dir)
            self.assertTrue(first.changed)
            self.assertFalse(second.changed)
            self.assertEqual(list(model_dir.glob('kitz-agent.yaml.pre-v1.0.4-*')), [])

    def test_discover_models_dir_finds_existing_localai_model_config(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            real_models = home / '.localai' / 'custom-models'
            real_models.mkdir(parents=True)
            (real_models / 'qwen3-fast.yaml').write_text('name: qwen3-fast\n', encoding='utf-8')
            self.assertEqual(discover_models_dir(home=home, env={}), real_models)

    def test_localai_has_model_reads_openai_model_list(self):
        payload = {'object': 'list', 'data': [{'id': 'qwen3-fast'}, {'id': 'kitz-agent'}]}
        self.assertTrue(localai_has_model(payload, 'kitz-agent'))
        self.assertFalse(localai_has_model(payload, 'missing'))

    def test_parse_chat_content_reads_openai_chat_completion(self):
        payload = {'choices': [{'message': {'role': 'assistant', 'content': 'KITZ BRIDGE OK'}}]}
        self.assertEqual(parse_chat_content(payload), 'KITZ BRIDGE OK')


if __name__ == '__main__':
    unittest.main()
