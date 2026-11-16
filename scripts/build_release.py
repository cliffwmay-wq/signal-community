"""Build deterministic Signal platform and community release ZIPs."""

from __future__ import annotations

import hashlib
from pathlib import Path
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
CHATGPT = PROJECT / "chatgpt"
CLAUDE_SKILL = PROJECT / "source" / "claude-skill"
CLAUDE_CODE = PROJECT / "source" / "claude-code"
RELEASES = PROJECT / "releases"
CHATGPT_ZIP = RELEASES / "Signal-ChatGPT-Plugin-v0.2.1.zip"
CLAUDE_SKILL_ZIP = RELEASES / "Signal-Claude-Skill.zip"
CLAUDE_CODE_ZIP = RELEASES / "Signal-Claude-Code-Plugin.zip"
KIT_ZIP = RELEASES / "Signal-Community-Edition-v0.2.2.zip"
FIXED_TIME = (2026, 11, 15, 0, 0, 0)


def _add(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    entry = zipfile.ZipInfo(name, date_time=FIXED_TIME)
    entry.compress_type = zipfile.ZIP_DEFLATED
    entry.external_attr = 0o644 << 16
    archive.writestr(entry, data)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_tree(source: Path, destination: Path, root: str) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        for path in sorted(source.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc" or path.name == ".DS_Store":
                continue
            _add(archive, root + "/" + path.relative_to(source).as_posix(), path.read_bytes())
    return _digest(destination)


def build_chatgpt(destination: Path = CHATGPT_ZIP) -> str:
    return _build_tree(CHATGPT, destination, "signal-community")


def build_claude_skill(destination: Path = CLAUDE_SKILL_ZIP) -> str:
    return _build_tree(CLAUDE_SKILL, destination, "signal")


def build_claude_code(destination: Path = CLAUDE_CODE_ZIP) -> str:
    return _build_tree(CLAUDE_CODE, destination, "my-editor")


def build_kit(destination: Path = KIT_ZIP, chatgpt_zip: Path = CHATGPT_ZIP, claude_skill_zip: Path = CLAUDE_SKILL_ZIP, claude_code_zip: Path = CLAUDE_CODE_ZIP) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        names = (
            (claude_skill_zip, CLAUDE_SKILL_ZIP.name),
            (claude_code_zip, CLAUDE_CODE_ZIP.name),
            (PROJECT / "community-release" / "Signal-Product-Preview.html", "Signal-Product-Preview.html"),
            (PROJECT / "community-release" / "RELEASE-README.md", "RELEASE-README.md"),
            (PROJECT / "SOURCE.md", "SOURCE.md"),
            (chatgpt_zip, CHATGPT_ZIP.name),
        )
        for source, name in sorted(names, key=lambda pair: pair[1]):
            _add(archive, "Signal-Community-Edition/" + name, source.read_bytes())
    return _digest(destination)


if __name__ == "__main__":
    chat_digest = build_chatgpt()
    claude_skill_digest = build_claude_skill()
    claude_code_digest = build_claude_code()
    kit_digest = build_kit()
    (RELEASES / "SHA256SUMS.txt").write_text(
        f"{chat_digest}  {CHATGPT_ZIP.name}\n"
        f"{claude_skill_digest}  {CLAUDE_SKILL_ZIP.name}\n"
        f"{claude_code_digest}  {CLAUDE_CODE_ZIP.name}\n"
        f"{kit_digest}  {KIT_ZIP.name}\n", encoding="utf-8"
    )
    print(CHATGPT_ZIP)
    print(f"SHA-256: {chat_digest}")
    print(CLAUDE_SKILL_ZIP)
    print(f"SHA-256: {claude_skill_digest}")
    print(CLAUDE_CODE_ZIP)
    print(f"SHA-256: {claude_code_digest}")
    print(KIT_ZIP)
    print(f"SHA-256: {kit_digest}")
