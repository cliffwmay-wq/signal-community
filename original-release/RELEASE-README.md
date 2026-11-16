# Signal — free community release kit

**Your words. Your voice. Better writing.**

Start with the edition that fits you:

| File | Who it's for |
|---|---|
| `Signal-Claude-Skill.zip` | Anyone who uses Claude in chat. Upload under Customize → Skills. No terminal required. |
| `Signal-Claude-Code-Plugin.zip` | Claude Code users who want slash commands, optional local file inspection, and repository source. |
| `Signal-Product-Preview.html` | An offline product-page preview. Download buttons work when both ZIP files are kept in this same folder. |
| `SHARE-WITH-COMMUNITY.md` | A ready-to-edit group post and publishing checklist. |

**Claude skill installation:** In Claude → Customize → Skills, enable code execution/file creation if needed. Use **+ → Create skill → Upload a skill** and select `Signal-Claude-Skill.zip`. Then ask Claude to use Signal on your draft.

**Claude Code installation:** Extract `Signal-Claude-Code-Plugin.zip` and run `claude --plugin-dir /absolute/path/to/my-editor`. Then try `/my-editor:editor` or `/my-editor:voice`.

**Voice DNA:** Upload your own original writing samples. Ask for an editable profile, review its observations, and opt in to any saving. Never distribute your real writing examples or profile with the public plugin.

**Privacy:** Signal's local scripts don't transmit data; using Claude still subjects provided text to Claude's own account policies and settings. Don't share sensitive writing samples.

**License:** MIT. No Signal signup, subscription or telemetry. No AI-detector-evasion promises. Provider watermark detection and authorship identification are not provided. Independent community software with no implied endorsement from Anthropic, Ruben Hassid, or How to AI.

**Verification:** 16 Python tests pass in the preparation environment, and packaged files can be inspected freely. Live Claude install/upload testing remains to be performed on a supported account before an official public release.
