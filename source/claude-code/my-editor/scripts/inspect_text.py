#!/usr/bin/env python3
"""Signal: local read-only UTF-8 textual artifact and editorial lint inspection.

No network, no editing, no model-origin prediction, and no statistical watermarks.
Requires Python 3.9+ standard library only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata

SPECIAL = {
    "\u00ad": ("soft-hyphen", "review", "Discretionary line-break character; can be intentional in typography."),
    "\u034f": ("combining-grapheme-joiner", "review", "Invisible combining control; can be valid for some scripts."),
    "\u061c": ("bidi-control", "caution", "Arabic letter mark; often legitimate in right-to-left text."),
    "\u180e": ("invisible-format", "review", "Mongolian vowel separator; context matters."),
    "\u200b": ("zero-width", "review", "Zero-width space; may be intentional line-breaking."),
    "\u200c": ("zero-width", "review", "Zero-width non-joiner; essential in some languages."),
    "\u200d": ("zero-width", "review", "Zero-width joiner; essential in emoji and many scripts."),
    "\u200e": ("bidi-control", "caution", "Left-to-right mark; can be intentional."),
    "\u200f": ("bidi-control", "caution", "Right-to-left mark; can be intentional."),
    "\u2060": ("invisible-format", "review", "Word joiner; may prevent line breaks intentionally."),
    "\ufeff": ("bom-or-zero-width", "review", "BOM at file start is common; elsewhere warrants review."),
    "\u00a0": ("unusual-space", "info", "Non-breaking space; ordinary in typography and pastes."),
    "\u202f": ("unusual-space", "info", "Narrow no-break space; legitimate in multiple languages."),
    "\u2007": ("unusual-space", "info", "Figure space; used for numeric alignment."),
    "\ufe0e": ("variation-selector", "info", "Text-style variation selector; may be legitimate."),
    "\ufe0f": ("variation-selector", "info", "Emoji-style variation selector; generally legitimate."),
}
BIDI = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A))
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
FRONTMATTER = re.compile(r"\A(?:\ufeff)?---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
MARKER_KEYS = re.compile(r"^\s*(?:generator|generated_by|created_by|ai_model|model_id|assistant_model|ai_tool)\s*:", re.I | re.M)
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)

STYLE_PATTERNS = (
    ("generic-era-opening", r"\bin today'?s (?:rapidly )?(?:evolving|changing|fast-paced) landscape\b", "Opening announces an era instead of a specific change."),
    ("empty-preamble", r"\bit(?:'s| is) important to note(?: that)?\b", "Preamble delays the point."),
    ("formulaic-transition", r"\b(?:moreover|furthermore|additionally)\s*,", "Check whether this transition actually advances an argument."),
    ("hype-vocabulary", r"\b(?:unlock|supercharge|game.changer|cutting.edge|revolutioniz\w*|synerg\w*)\b", "Check if this word substitutes for a precise mechanism."),
    ("unearned-certainty", r"\b(?:will ensure|guaranteed to|the truth is)\b", "Check whether the evidence supports this certainty."),
    ("formulaic-contrast", r"\bit(?:'s| is) not just\b|\bnot only\b.{0,90}\bbut also\b", "An authentic distinction may still be useful; assess this instance."),
    ("generic-close", r"\b(?:in conclusion|ultimately,? it comes down to)\b", "Conclusion may be restating rather than advancing the point."),
    ("generic-authority", r"\b(?:experts agree|research shows|studies show)\b", "Verify specific evidence or attribution."),
    ("performance-voice", r"\b(?:let'?s (?:dive in|delve into)|here'?s the (?:real )?(?:secret|twist))\b", "Check whether this performance framing matches the author."),
    ("inflated-claims", r"\b(?:seamless success|transformative outcomes|best.in.class)\b", "Replace with observables, if available."),
)


def _where(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    previous_newline = text.rfind("\n", 0, offset)
    return line, offset - previous_newline


def _excerpt(text: str, begin: int, end: int, radius: int = 36) -> str:
    return text[max(0, begin - radius):min(len(text), end + radius)].replace("\n", "\\n")


def _script(ch: str) -> str | None:
    if not unicodedata.category(ch).startswith("L"):
        return None
    name = unicodedata.name(ch, "")
    for script in ("LATIN", "CYRILLIC", "GREEK"):
        if name.startswith(script + " "):
            return script
    return None


def scan_text(text: str, max_examples: int = 10, include_style: bool = True) -> dict:
    findings: dict[str, list] = {}
    totals = Counter()

    def record(category: str, item: dict) -> None:
        totals[category] += 1
        findings.setdefault(category, [])
        if len(findings[category]) < max_examples:
            findings[category].append(item)

    for offset, ch in enumerate(text):
        code = ord(ch)
        setting = SPECIAL.get(ch)
        if setting is None and code in BIDI:
            setting = ("bidi-control", "caution", "Bidirectional formatting control; legitimate sometimes, but can reorder text displays.")
        if setting is None and 0xE0000 <= code <= 0xE007F:
            setting = ("unicode-tag", "review", "Unicode tag character; generally invisible; context should be examined.")
        if setting is None and 0x2061 <= code <= 0x2064:
            setting = ("invisible-format", "info", "Invisible mathematical or formatting separator; context matters.")
        if setting is None and unicodedata.category(ch) == "Cf":
            setting = ("other-format-control", "review", "Unicode format character; evaluate in linguistic context.")
        if setting is None:
            continue
        category, severity, note = setting
        if ch == "\ufeff" and offset == 0:
            note = "Byte order mark at file start; common encoding marker, not proof of provenance."
        line, column = _where(text, offset)
        record(category, {
            "line": line, "column": column, "offset": offset,
            "codepoint": f"U+{code:04X}", "unicode_name": unicodedata.name(ch, "UNNAMED"),
            "severity": severity, "excerpt": _excerpt(text, offset, offset + 1), "note": note,
        })

    for match in WORD.finditer(text):
        scripts = {s for ch in match.group(0) if (s := _script(ch))}
        if "LATIN" in scripts and ("CYRILLIC" in scripts or "GREEK" in scripts):
            line, column = _where(text, match.start())
            record("mixed-script-word", {"line": line, "column": column, "value": match.group(0),
                "scripts": sorted(scripts), "severity": "caution", "note": "Mixed scripts can be legitimate but can also visually mask lookalike letters."})

    for match in HTML_COMMENT.finditer(text):
        line, column = _where(text, match.start())
        record("html-comment", {"line": line, "column": column, "severity": "info", "excerpt": _excerpt(text, match.start(), match.end()),
            "note": "Markdown HTML comment; not necessarily hidden provenance. Review before altering."})

    fm = FRONTMATTER.search(text)
    if fm:
        for match in MARKER_KEYS.finditer(fm.group(1)):
            offset = fm.start(1) + match.start()
            line, column = _where(text, offset)
            record("frontmatter-provenance-field", {"line": line, "column": column, "severity": "info",
                "field": match.group().strip().rstrip(":"), "note": "Possible authoring metadata; preserve if it documents provenance."})

    if include_style:
        for category, pattern, note in STYLE_PATTERNS:
            for match in re.finditer(pattern, text, re.I | re.M):
                line, column = _where(text, match.start())
                record("style:" + category, {"line": line, "column": column, "severity": "editorial",
                    "matched_text": match.group(0), "note": note})

    return {
        "tool": "Signal / myEditor textual artifact inspector",
        "scope": "literal UTF-8/Markdown characters and heuristic editorial patterns",
        "limitations": [
            "NOT a statistical token-choice watermark detector.",
            "NOT an AI-authorship classifier or proof of origin.",
            "Legitimate multilingual, emoji and typographic usage can produce findings.",
            "This scan never changes the input or contacts external services."
        ],
        "statistics": {"characters": len(text), "lines": text.count("\n") + 1, "word_tokens_approx": len(re.findall(r"\b\w+\b", text))},
        "total_findings": sum(totals.values()),
        "totals_by_category": dict(sorted(totals.items())),
        "examples_by_category": dict(sorted(findings.items())),
    }


def render_markdown(report: dict) -> str:
    lines = ["# Signal: text inspection", "", f"**Characters:** {report['statistics']['characters']:,} · "
             f"**Lines:** {report['statistics']['lines']:,} · **Findings:** {report['total_findings']:,}", ""]
    lines += ["**Important:** This is **not** a provider statistical watermark test or an AI-authorship detector.", ""]
    if not report["total_findings"]:
        lines.append("No matching artifacts or editorial patterns found. This does not verify human authorship.")
    for category, count in report["totals_by_category"].items():
        lines += [f"## {category} ({count})", ""]
        for finding in report["examples_by_category"].get(category, []):
            where = f"line {finding['line']}, col {finding['column']}"
            identifier = finding.get("codepoint", finding.get("field", finding.get("matched_text", finding.get("value", "HTML comment"))))
            lines.append(f"- **{where}** · `{identifier}` — {finding['note']}")
        if count > len(report["examples_by_category"].get(category, [])):
            lines.append(f"- ... and {count - len(report['examples_by_category'][category])} more finding(s).")
        lines.append("")
    lines += ["## Interpretation", "", "A finding identifies a character, markup item, or editorial candidate for review—not an author, origin, or hidden statistical watermark."]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Unicode, Markdown metadata, and editorial pattern scan; not an AI watermark detector.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("path", nargs="?", help="UTF-8 text/Markdown file")
    source.add_argument("--stdin", action="store_true", help="Read UTF-8 text from standard input")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--no-style", action="store_true", help="Only inspect literal characters and markup")
    parser.add_argument("--max-examples", type=int, default=10, help="Max shown findings per category (default 10)")
    args = parser.parse_args(argv)
    if args.max_examples < 1 or args.max_examples > 1000:
        parser.error("--max-examples must be 1..1000")
    if args.stdin:
        text = sys.stdin.read()
    else:
        source_path = Path(args.path)
        if not source_path.is_file():
            parser.error(f"Not a file: {source_path}")
        if source_path.stat().st_size > 10 * 1024 * 1024:
            parser.error("File too large (10 MiB maximum)")
        try:
            text = source_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            parser.error("File is not valid UTF-8; convert a copy before scanning")
    report = scan_text(text, args.max_examples, include_style=not args.no_style)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
