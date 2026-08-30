import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'release-overrides' / 'localai_stream_bridge.py'
spec = importlib.util.spec_from_file_location('localai_stream_bridge', MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class StreamBridgeTests(unittest.TestCase):
    def test_stream_request_is_converted_to_nonstream_agent_request(self):
        incoming = {
            'model': 'kitz-agent',
            'messages': [{'role': 'user', 'content': 'Hallo'}],
            'stream': True,
            'stream_options': {'include_usage': True},
        }
        result = mod.normalize_request_for_agent_core(incoming)
        self.assertEqual(result['model'], 'kitz-agent')
        self.assertFalse(result['stream'])
        self.assertNotIn('stream_options', result)
        self.assertEqual(result['messages'], incoming['messages'])

    def test_nonstream_completion_is_encoded_as_openai_sse(self):
        completion = {
            'id': 'chatcmpl-test',
            'object': 'chat.completion',
            'created': 123,
            'model': 'kitz-agent',
            'choices': [{
                'index': 0,
                'message': {'role': 'assistant', 'content': 'KITZ_OK'},
                'finish_reason': 'stop',
            }],
            'usage': {'prompt_tokens': 3, 'completion_tokens': 2, 'total_tokens': 5},
        }
        body = mod.encode_sse_completion(completion, include_usage=True).decode('utf-8')
        self.assertIn('data: ', body)
        self.assertIn('KITZ_OK', body)
        self.assertIn('"finish_reason":"stop"', body)
        self.assertIn('"usage":{"prompt_tokens":3,"completion_tokens":2,"total_tokens":5}', body)
        self.assertTrue(body.endswith('data: [DONE]\n\n'))

    def test_stream_error_body_is_not_faked_as_success(self):
        with self.assertRaises(ValueError):
            mod.encode_sse_completion({'detail': 'upstream failed'}, include_usage=False)


if __name__ == '__main__':
    unittest.main()
