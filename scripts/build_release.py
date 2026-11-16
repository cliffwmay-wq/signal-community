"""Build deterministic Signal ChatGPT and three-platform community release ZIPs."""

from __future__ import annotations

import hashlib
from pathlib import Path
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
CHATGPT = PROJECT / "chatgpt"
RELEASES = PROJECT / "releases"
CHATGPT_ZIP = RELEASES / "Signal-ChatGPT-Plugin-v0.2.1.zip"
KIT_ZIP = RELEASES / "Signal-Community-Edition-v0.2.1.zip"
FIXED_TIME = (2026, 11, 15, 0, 0, 0)


def _add(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    entry = zipfile.ZipInfo(name, date_time=FIXED_TIME)
    entry.compress_type = zipfile.ZIP_DEFLATED
    entry.external_attr = 0o644 << 16
    archive.writestr(entry, data)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_chatgpt(destination: Path = CHATGPT_ZIP) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        for path in sorted(CHATGPT.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc" or path.name == ".DS_Store":
                continue
            _add(archive, "signal-community/" + path.relative_to(CHATGPT).as_posix(), path.read_bytes())
    return _digest(destination)


def build_kit(destination: Path = KIT_ZIP, chatgpt_zip: Path = CHATGPT_ZIP) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        names = (
            (PROJECT / "original-release" / "Signal-Claude-Skill.zip", "Signal-Claude-Skill.zip"),
            (PROJECT / "original-release" / "Signal-Claude-Code-Plugin.zip", "Signal-Claude-Code-Plugin.zip"),
            (PROJECT / "community-release" / "Signal-Product-Preview.html", "Signal-Product-Preview.html"),
            (PROJECT / "community-release" / "RELEASE-README.md", "RELEASE-README.md"),
            (PROJECT / "community-release" / "SHARE-WITH-COMMUNITY.md", "SHARE-WITH-COMMUNITY.md"),
            (PROJECT / "SOURCE.md", "SOURCE.md"),
            (chatgpt_zip, CHATGPT_ZIP.name),
        )
        for source, name in sorted(names, key=lambda pair: pair[1]):
            _add(archive, "Signal-Community-Edition/" + name, source.read_bytes())
    return _digest(destination)


if __name__ == "__main__":
    chat_digest = build_chatgpt()
    kit_digest = build_kit()
    (RELEASES / "SHA256SUMS.txt").write_text(
        f"{chat_digest}  {CHATGPT_ZIP.name}\n{kit_digest}  {KIT_ZIP.name}\n", encoding="utf-8"
    )
    print(CHATGPT_ZIP)
    print(f"SHA-256: {chat_digest}")
    print(KIT_ZIP)
    print(f"SHA-256: {kit_digest}")
