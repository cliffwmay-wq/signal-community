---
name: inspect
description: "Inspect a local plain-text or Markdown file for invisible Unicode, directional controls, soft hyphens, unusual spaces, mixed-script lookalikes, HTML comments, and provenance-related frontmatter. A factual, read-only textual artifact scan—not a statistical AI watermark detector."
---

# Signal — provenance and hidden-text inspection

## Boundaries

Do not confuse visual/Unicode artifacts with provider **statistical token-choice watermarks**. The latter cannot be established by a character scan and generally need a provider-compatible keyed detector. No finding proves AI authorship. No clean report proves human authorship. Do not claim to remove a watermark or erase the text's origin.

Read `../../references/watermarks-provenance.md` for mechanisms and caveats.

## Local scan

When a local shell is available, inspect an explicitly supplied local UTF-8 `.md` or `.txt` file using the packaged **read-only** program:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect_text.py" path/to/document.md
```

For machine-readable output:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect_text.py" path/to/document.md --format json
```

Or paste text over standard input with `--stdin`. The tool neither modifies files nor uses a network connection. If execution is unavailable, inspect pasted source text where possible, describe the limitation, and offer the local command; do not pretend to have run the scan.

## Interpretation

- **Character evidence:** give exact code points, line/column and context. Explain possible legitimate usage (emoji, Persian/Arabic shaping, Indic script, technical notation, copy/paste).
- **Markup/metadata evidence:** find HTML comments and authoring/frontmatter metadata. Do not automatically remove disclosure or copyright/provenance content.
- **Editorial heuristics:** give candidate style issues as suggestions, not source attribution.
- **Privacy:** keep all content local unless the user explicitly asks for a particular external analysis. Never upload text to third-party detectors by default.

Return a concise finding summary and the location of any reviewed artifacts. If the user wants cleanup, propose explicit changes and get agreement before destructive removal of ambiguous characters or metadata.
