# Signal Community Edition

This project adapts the user-supplied Signal 0.2.0 community release and adds a faithful ChatGPT companion. Signal's product promise remains **“Your words. Your voice. Better writing.”** Its scope is editorial: meaning-preserving edits and composition, optional evidence-backed Voice DNA, passage-level audits, accurate snapshots, and literal artifact inspection when a local runtime is available.

## Contents

- [`source/`](source/) — reviewable Claude skill and plugin source, with the internal sharing draft removed.
- [`chatgpt/`](chatgpt/) — Signal ChatGPT plugin 0.2.1, adapted from the original chat skill.
- [`community-release/`](community-release/) — updated three-path release notes and product preview.
- [`downloads/`](downloads/) — downloadable ZIPs for the complete kit and each platform.
- [GitHub Releases](https://github.com/cliffwmay-wq/signal-community/releases) — version notes and download links.
- [`SOURCE.md`](SOURCE.md) — hashes and preservation record.

The original supplied ZIPs are retained only in the local preservation copy. Public Claude packages are rebuilt from the source without the internal sharing draft. The ChatGPT edition adapts platform wording and packaging while retaining the editorial method and inspector. It is an addition to Signal, not a Temper rebrand.

## Validate and build

From this project's parent directory:

```bash
python3 -m unittest discover -s signal-community/source/claude-code/my-editor/tests -v
python3 -m unittest discover -s signal-community/chatgpt/tests -v
python3 signal-community/scripts/build_release.py
python3 -m zipfile -t signal-community/releases/Signal-ChatGPT-Plugin-v0.2.1.zip
python3 -m zipfile -t signal-community/releases/Signal-Community-Edition-v0.2.2.zip
```

The [ChatGPT README](chatgpt/README.md) gives local installation steps and a first prompt. The [first-use example](chatgpt/examples/first-use.md) demonstrates a cold edit and optional Voice DNA path. Tests validate the scanner, package shape, and archive integrity. Live host behavior still needs a smoke test after installation.
