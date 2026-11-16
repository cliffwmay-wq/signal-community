"""Validate the ChatGPT companion and public Signal packages."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
class PackageTests(unittest.TestCase):
    def test_manifest_and_skill(self) -> None:
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertEqual(manifest["name"], "signal-community")
        self.assertEqual(manifest["version"], "0.2.1")
        self.assertEqual(manifest["license"], "MIT")
        self.assertFalse((ROOT / "mcp.json").exists())
        interface = manifest["extensions"]["com.openai"]["interface"]
        self.assertEqual(interface["displayName"], "Signal — Community Edition")
        for key in ("composerIcon", "logo"):
            self.assertTrue((ROOT / interface[key]).is_file())
        skill = (ROOT / "skills/signal/SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: signal\n"))
        for mode in ("Compress", "Compose", "Polish", "Snapshot", "Audit", "Voice DNA", "Inspect"):
            self.assertIn(mode, skill)
        self.assertIn("No false detection", skill)
        self.assertIn("No invented human-ness", skill)

    def test_skill_references_exist(self) -> None:
        skill_dir = ROOT / "skills/signal"
        for markdown in skill_dir.rglob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "#")):
                    continue
                with self.subTest(file=markdown.relative_to(ROOT), target=target):
                    self.assertTrue((markdown.parent / target.split("#", 1)[0]).is_file())
        for name in ("quality-gates.md", "anti-ai-patterns.md", "voice-dna-template.md", "voice-preservation.md", "watermarks-provenance.md"):
            self.assertTrue((skill_dir / "references" / name).is_file())

    def test_first_use_preserves_central_promise(self) -> None:
        example = (ROOT / "examples/first-use.md").read_text(encoding="utf-8")
        for phrase in ("possible start", "aspirational", "has not approved", "unmeasured", "do not save", "provisional"):
            self.assertIn(phrase, example)

    def test_release_archive_is_reproducible_and_single_root(self) -> None:
        spec = importlib.util.spec_from_file_location("signal_release", PROJECT / "scripts/build_release.py")
        assert spec and spec.loader
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as temp:
            a = Path(temp) / "a.zip"
            b = Path(temp) / "b.zip"
            self.assertEqual(builder.build_chatgpt(a), builder.build_chatgpt(b))
            with zipfile.ZipFile(a) as archive:
                names = archive.namelist()
                self.assertEqual(archive.testzip(), None)
                self.assertTrue(all(name.startswith("signal-community/") for name in names))
                self.assertIn("signal-community/plugin.json", names)
                self.assertIn("signal-community/skills/signal/SKILL.md", names)
                self.assertIn("signal-community/skills/signal/scripts/inspect_text.py", names)

    def test_community_kit_omits_internal_sharing_draft(self) -> None:
        spec = importlib.util.spec_from_file_location("signal_release", PROJECT / "scripts/build_release.py")
        assert spec and spec.loader
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as temp:
            chatgpt = Path(temp) / "chatgpt.zip"
            claude_skill = Path(temp) / "claude-skill.zip"
            claude_code = Path(temp) / "claude-code.zip"
            kit = Path(temp) / "kit.zip"
            builder.build_chatgpt(chatgpt)
            builder.build_claude_skill(claude_skill)
            builder.build_claude_code(claude_code)
            builder.build_kit(kit, chatgpt, claude_skill, claude_code)
            with zipfile.ZipFile(kit) as archive:
                self.assertEqual(archive.testzip(), None)
                names = archive.namelist()
                self.assertTrue(all(name.startswith("Signal-Community-Edition/") for name in names))
                self.assertIn("Signal-Community-Edition/Signal-Product-Preview.html", names)
                self.assertIn("Signal-Community-Edition/Signal-ChatGPT-Plugin-v0.2.1.zip", names)
                self.assertFalse(any("SHARE-WITH-COMMUNITY" in name for name in names))
            with zipfile.ZipFile(claude_code) as archive:
                self.assertFalse(any("SHARE-WITH-COMMUNITY" in name for name in archive.namelist()))


if __name__ == "__main__":
    unittest.main()
