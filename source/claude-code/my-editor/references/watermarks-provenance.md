# Text provenance and watermark inspection — limitations

## Four distinct mechanisms

1. **Unicode/formatting artifacts (inspectable):** zero-width characters, soft hyphens, bidirectional controls, unusual spaces, tag characters, BOMs and cross-script confusables. These can be intentional and often have legitimate writing or typography uses. Their presence does **not** show the text came from AI.
2. **Markup and metadata (inspectable when present):** Markdown HTML comments, YAML frontmatter `generator`/`model` fields, tracked document properties. A Markdown text scanner cannot inspect all DOCX, PDF, HTML or C2PA metadata; use a format-specific inspection tool and keep the original file when provenance is important.
3. **Statistical token-choice watermark (not inspectable with this tool):** a generative model can shift token probabilities according to a secret scheme. Detection generally requires a compatible detector/key, enough text and appropriate conditions. It is not produced by zero-width characters and may not survive rewriting. **Do not represent a local Unicode scan as this test.**
4. **Post-hoc AI text classifiers (fallible, external):** can produce false positives, including human prose, and false negatives, including edited model prose. They are not watermarks and should not be treated as evidence of authorship.

## Interpretation principles

- **Positive character finding** = specific code point present, no attribution.
- **No character finding** = no matching character found in inspected input, not a declaration of human authorship.
- **Positive vendor-compatible watermark** = limited provenance signal according to that detector, not proof of who authored, owned, or edited the text.
- **No vendor-compatible watermark** = no supported signal found, not proof that AI wasn't involved.
- A source can be partially human, partially AI-assisted, heavily edited, or copied. No single quality label captures authorship.
- Don't strip disclosure statements or licensing data to misrepresent provenance or evade institutional requirements.

## Scanning limitations

- `scripts/inspect_text.py` operates on UTF-8 text/Markdown only and **does not open network connections, contact providers, or alter the input**.
- Emoji ZWJ sequences, variation selectors, joiners in Persian/Arabic/Indic scripts, narrow non-breaking spaces and soft hyphens can be ordinary and essential. Flag for contextual review, not blanket deletion.
- Mixed Latin + Cyrillic/Greek lookalikes *within a word* may indicate copy/paste or spoofing, but a word containing characters from multiple scripts is not necessarily malicious.
- Scan results are literal observations; editorial pattern matches are subjective heuristics. Never combine them into an AI-authorship probability.
