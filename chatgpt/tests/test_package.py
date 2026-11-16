"""Validate the ChatGPT companion and preserved Signal 0.2.0 source."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_HASHES = {
    "Signal-Claude-Skill.zip": "fd81bf622dc54c4316d385a9196a09d1b339d3b5f3f177eef7f159d17165f15f",
    "Signal-Claude-Code-Plugin.zip": "e4f322b69d52201210f6ceefbd41e2c0c84d65d6dd5ee9f71b05d4570ba78d51",
}


class PackageTests(unittest.TestCase):
    def test_original_releases_are_unchanged(self) -> None:
        for name, expected in SOURCE_HASHES.items():
            with self.subTest(name=name):
                actual = hashlib.sha256((PROJECT / "original-release" / name).read_bytes()).hexdigest()
                self.assertEqual(actual, expected)

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

    def test_community_kit_retains_originals_and_adds_chatgpt(self) -> None:
        spec = importlib.util.spec_from_file_location("signal_release", PROJECT / "scripts/build_release.py")
        assert spec and spec.loader
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as temp:
            chatgpt = Path(temp) / "chatgpt.zip"
            kit = Path(temp) / "kit.zip"
            builder.build_chatgpt(chatgpt)
            builder.build_kit(kit, chatgpt)
            with zipfile.ZipFile(kit) as archive:
                self.assertEqual(archive.testzip(), None)
                names = archive.namelist()
                self.assertTrue(all(name.startswith("Signal-Community-Edition/") for name in names))
                self.assertIn("Signal-Community-Edition/Signal-Product-Preview.html", names)
                self.assertIn("Signal-Community-Edition/Signal-ChatGPT-Plugin-v0.2.1.zip", names)
                for name, expected in SOURCE_HASHES.items():
                    member = archive.read("Signal-Community-Edition/" + name)
                    self.assertEqual(hashlib.sha256(member).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
