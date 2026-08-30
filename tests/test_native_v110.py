import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / 'release-overrides' / 'install_kitz_native.py'
UPDATE = ROOT / 'update-localai-v1.1.0.sh'
BACKEND = ROOT / 'release-overrides' / 'kitz_native_backend.py'


class NativeV110Tests(unittest.TestCase):
    def load_installer(self):
        spec = importlib.util.spec_from_file_location('install_kitz_native', INSTALLER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_native_model_config_uses_kitz_native_not_cloud_proxy(self):
        mod = self.load_installer()
        text = mod.render_model_config()
        self.assertIn('backend: kitz-native', text)
        self.assertIn('parameters:\n  model: kitz-agent', text)
        self.assertIn('known_usecases:\n  - chat', text)
        self.assertNotIn('cloud-proxy', text)
        self.assertNotIn('proxy:', text)

    def test_dynamic_external_backend_json_preserves_other_backends(self):
        mod = self.load_installer()
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'external_backends.json'
            path.write_text('{"other":"/tmp/other/run.sh"}\n', encoding='utf-8')
            mod.upsert_external_backend_json(path, Path('/tmp/kitz-native/run.sh'))
            data = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(data['other'], '/tmp/other/run.sh')
            self.assertEqual(data['kitz-native'], '/tmp/kitz-native/run.sh')

    def test_backend_source_implements_grpc_chat_methods(self):
        text = BACKEND.read_text(encoding='utf-8')
        self.assertIn('class BackendServicer', text)
        self.assertIn('def LoadModel(', text)
        self.assertIn('def Predict(', text)
        self.assertIn('def PredictStream(', text)
        self.assertIn('http://127.0.0.1:8787/v1/chat/completions', text)

    def test_predict_stream_uses_non_streaming_agent_core(self):
        text = BACKEND.read_text(encoding='utf-8')
        marker = 'def PredictStream(self, request, context):'
        block = text[text.index(marker):]
        self.assertIn('payload = _payload_from_request(request, stream=False)', block)
        self.assertNotIn('payload = _payload_from_request(request, stream=True)', block)

    def test_update_script_is_pinned_and_removes_legacy_bridge(self):
        text = UPDATE.read_text(encoding='utf-8')
        self.assertIn('v1.1.0 - KITZ Native Backend', text)
        self.assertIn('KITZ_RELEASE_REF:-v1.1.0', text)
        self.assertIn('install_kitz_native.py', text)
        self.assertIn('ai.kitz.localai-stream-bridge', text)
        self.assertNotIn('/main/release-overrides/', text)


if __name__ == '__main__':
    unittest.main()
