# Signal — free community release, 0.2.1 companion kit

**Your words. Your voice. Better writing.** Signal helps people edit, compose, and examine their own writing while protecting meaning and voice. It remains free, MIT licensed, and independent community software.

This kit preserves both original **0.2.0 Claude packages byte for byte** and adds a **0.2.1 ChatGPT companion**. The added edition follows the same editorial contract, optional Voice DNA method, and evidence-based audit. It is a platform adaptation, not a Temper rebrand.

| File | Use |
| --- | --- |
| `Signal-Claude-Skill.zip` | Original Claude chat skill, version 0.2.0. |
| `Signal-Claude-Code-Plugin.zip` | Original Claude Code plugin, version 0.2.0, with slash commands and local inspector. |
| `Signal-ChatGPT-Plugin-v0.2.1.zip` | New ChatGPT desktop plugin companion with the same core workflows. |
| `Signal-Product-Preview.html` | Offline overview with all three paths. |
| `SHARE-WITH-COMMUNITY.md` | Editable sharing copy and release checklist. |
| `SOURCE.md` | Source provenance and original-file hashes. |

## Start with a draft

Paste writing and ask: **“Use Signal to tighten this without changing my point or making it sound generic.”** A Voice DNA profile is optional. The ChatGPT ZIP includes a worked example in `examples/first-use.md`.

For Voice DNA, use your own non-sensitive original samples, review Signal's evidence-backed observations, and decide whether to save a profile privately. Signal does not save one by default.

## Install

- **Claude chat:** Upload `Signal-Claude-Skill.zip` through Claude's skill upload flow, as described in the original package.
- **Claude Code:** Extract `Signal-Claude-Code-Plugin.zip`, then use `claude --plugin-dir /absolute/path/to/my-editor`.
- **ChatGPT desktop:** Extract `Signal-ChatGPT-Plugin-v0.2.1.zip` into a workspace root, add a local marketplace entry, restart ChatGPT desktop, and install Signal. The ChatGPT ZIP's `README.md` gives the exact steps. A developer can also upload the ZIP as a draft through OpenAI's plugin portal; draft upload is not publication.

The local inspector runs only where Python and local files are available. No Signal account, telemetry, external API, or subscription is included. Text submitted to Claude or ChatGPT remains subject to that provider's account settings and policies. Signal does not detect authorship or promise detector evasion.

## Validation status

The preparation environment ran the original Claude package tests, the ChatGPT companion tests, and ZIP integrity checks. A live install and prompt smoke test in Claude and ChatGPT accounts remains to be done before wide release. See `SOURCE.md` for what was preserved.
