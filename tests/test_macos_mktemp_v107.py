from pathlib import Path
import re
import unittest


class MacOSMktempV107Tests(unittest.TestCase):
    def test_v107_mktemp_templates_end_with_xs(self):
        script = Path('update-localai-v1.0.7.sh')
        self.assertTrue(script.exists(), 'v1.0.7 updater must exist')
        text = script.read_text(encoding='utf-8')
        templates = re.findall(r'mktemp\s+"\$\{TMPDIR:-/tmp\}/([^"]+)"', text)
        self.assertGreaterEqual(len(templates), 4)
        for template in templates:
            self.assertTrue(
                template.endswith('XXXXXX'),
                f'macOS mktemp template must end in XXXXXX, got: {template}',
            )
            self.assertNotRegex(template, r'XXXXXX\.[A-Za-z0-9]+$')


if __name__ == '__main__':
    unittest.main()
