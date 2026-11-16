from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def test_manifest_has_stable_plugin_name_and_license(self):
        data = json.loads((ROOT / '.claude-plugin' / 'plugin.json').read_text())
        self.assertEqual(data['name'], 'my-editor')
        self.assertEqual(data['license'], 'MIT')
        self.assertEqual(data['version'], '0.2.0')

    def test_marketplace_entry_resolves_to_plugin(self):
        data = json.loads((ROOT / '.claude-plugin' / 'marketplace.json').read_text())
        self.assertEqual(data['plugins'][0]['name'], 'my-editor')
        self.assertEqual(data['plugins'][0]['source'], './')

    def test_editor_commands_and_voice_profile_exist(self):
        for name in ['editor', 'audit', 'inspect', 'voice', 'compress-to-signal']:
            text = (ROOT / 'skills' / name / 'SKILL.md').read_text()
            self.assertIn('name:', text[:200])
            self.assertIn('description:', text[:400])
        self.assertTrue((ROOT / 'references' / 'voice-dna-template.md').exists())

    def test_privacy_and_license_distributed(self):
        privacy = (ROOT / 'PRIVACY.md').read_text().lower()
        self.assertIn('claude', privacy)
        self.assertIn('no telemetry', privacy)
        self.assertIn('mit license', (ROOT / 'LICENSE').read_text().lower())
        self.assertIn('profiles/', (ROOT / '.gitignore').read_text())

    def test_all_linked_reference_files_exist(self):
        for skill in (ROOT / 'skills').glob('*/SKILL.md'):
            import re
            for name in re.findall(r'\.\./\.\./references/([\w-]+\.md)', skill.read_text()):
                self.assertTrue((ROOT / 'references' / name).exists(), str(skill) + ': ' + name)

if __name__ == '__main__':
    unittest.main()
