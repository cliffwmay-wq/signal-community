<div align="center">

# SIGNAL

### Your words. Your voice. Better writing.

**A free, open-source personal editorial studio for Claude.**

_Edit without losing yourself._

**Claude chat skill • Claude Code plugin • No paywall • MIT licensed**

</div>

---

## Your writing should still sound like you

AI can help with a draft. It can also sand every rough edge into the same generic paragraph. Signal is an editorial workflow designed to improve clarity **without rewriting the author's thinking or personality out of the page**.

Signal can edit cold, with no setup. Or you can give it examples of your own *original* writing—handwritten notes, essays, emails, or journal pages—and build a **Voice DNA** profile that you can review, change, and keep private.

This is **not** a tool for proving a text is human-authored or evading detector systems.

### What you get

| Experience | What it does | Claude Code command |
|---|---|---|
| **Edit** | Compress, Compose, Polish and Snapshot text without losing meaning | `/my-editor:editor` |
| **Voice DNA** | Learn your writing habits from *your own* examples; create an optional private profile | `/my-editor:voice` |
| **Audit** | Show passage-level writing problems, not fake AI-detection percentages | `/my-editor:audit` |
| **Inspect** | Identify exact hidden Unicode, mixed-script confusables, and Markdown metadata | `/my-editor:inspect` |
| **Legacy** | Keep the earlier Signal invocation | `/my-editor:compress-to-signal` |

## Two ways to get started

### A. New to Claude Code? Use the Claude Skill ZIP

Get **`Signal-Claude-Skill.zip`** from the release package (it is a separate ZIP, not this entire repository).

1. Open [Claude → Customize → Skills](https://claude.ai/customize/skills). Turn on code execution/file creation if prompted.
2. Choose **+ → Create skill → Upload a skill**, then choose `Signal-Claude-Skill.zip`.
3. Enable Signal. In chat, try: **“Use Signal to make this sound like me while keeping every fact and qualification: [paste draft].”**

You do **not** need to supply a voice profile to start. For Voice DNA, upload a couple of your original writing passages and say: **“Use Signal to make a provisional Voice DNA profile from these. Show me what you inferred; don't save it yet.”**

The chat skill provides prompt-based editing and audit. The Python file inspector is only available if the Claude environment can execute the bundled script.

### B. Claude Code users? Load the plugin ZIP

Get **`Signal-Claude-Code-Plugin.zip`** and extract it. The plugin root is the `my-editor/` folder.

```bash
claude --plugin-dir /absolute/path/to/my-editor
```

Then in Claude Code:

```text
/my-editor:editor Compress this note without altering decisions or evidence: ...
/my-editor:voice Learn my voice from these three original passages: ...
/my-editor:audit Find the formulaic parts and show specific fixes: ...
/my-editor:inspect Inspect this UTF-8 Markdown file for hidden characters: notes.md
```

Validate in your own Claude Code installation:

```bash
claude plugin validate --strict /absolute/path/to/my-editor
```

A GitHub marketplace can provide a reusable install/update command after the repository is made public. A GitHub repository **has not yet been published as part of this package**.

## The Signal principles

- **Keep the thinking. Lose the noise.** Facts, decisions, qualifiers, uncertainty, cause-and-effect and authorial intent are protected.
- **Your voice is the baseline.** If you naturally use a rhetorical pattern, it isn't automatically wrong because AI also uses it.
- **No manufactured personality.** Never add fake stories, typos, dialect, professions, emotions, or first-hand claims to feel more human.
- **Show your work.** Audits cite specific passages and reasons; Voice DNA has evidence and uncertainty.
- **No black-box detector scores.** Style is not proof of origin; Unicode artifacts are not a statistical model watermark.
- **Private by design.** No Signal analytics, subscription, server, external API, or network-enabled scripts. Claude's own service data handling still applies.

## Voice DNA: optional, portable, personal

1. Share 2–5 short passages that are actually yours. Confirm whether they are handwritten, typed, or AI-assisted. Remove sensitive details first.
2. Signal describes observed vocabulary, cadence, thought structure, qualifiers, humor, emphasis and differences among writing contexts. Every meaningful trait should have supporting sample evidence.
3. Review and correct its first interpretation. If **you request a file**, Signal can produce `VOICE_PROFILE.md` to save privately, outside the shared plugin.
4. Provide that profile whenever you want a new draft edited in your voice. You can suspend, adjust or discard it at any time.

See [`references/voice-dna-template.md`](references/voice-dna-template.md).

## Word-choice watermarks and character inspection

```bash
python3 scripts/inspect_text.py examples/sample-draft.md
python3 scripts/inspect_text.py examples/sample-draft.md --format json
```

The local inspector requires only Python 3.9+ and the standard library; it does not change the file. It can spot invisible characters, bidi controls, HTML comments, and other literal artifacts. **It cannot identify a provider's statistical text watermark**, or determine whether AI wrote the text. See [`references/watermarks-provenance.md`](references/watermarks-provenance.md).

## For community makers

- **Price:** free, no signup with Signal, no paid license. Your Claude account may have its own usage limits.
- **License:** MIT. Fork, adapt, share and contribute with attribution under the license terms.
- **Privacy:** read [`PRIVACY.md`](PRIVACY.md). Never publish samples or profiles from real people without their explicit permission.
- **Contributing:** see [`CONTRIBUTING.md`](CONTRIBUTING.md).
- **Releases:** see [`CHANGELOG.md`](CHANGELOG.md).

Independent community software; not affiliated with or endorsed by Anthropic, Ruben Hassid, or How to AI. Signal refers to this editorial tool, not the Signal messaging service.

## Technical status

The scanner has automated unit tests; run them with `python3 -m unittest discover -s tests -v`. Plugin and skill source packages are prepared for local installation and Claude upload respectively. They were not smoke-tested inside the user's logged-in Claude Code/Claude chat account during creation. Feedback from first-time installs is welcome.
