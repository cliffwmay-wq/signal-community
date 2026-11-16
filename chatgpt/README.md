# Signal — Community Edition for ChatGPT

**Your words. Your voice. Better writing.**

This is a ChatGPT companion to the user-supplied Signal 0.2.0 community release. It keeps the original editorial purpose and workflows: Compress, Compose, Polish, Snapshot, Audit, optional Voice DNA, and literal text inspection where a local runtime is available. The companion is version **0.2.1** to distinguish this added platform package from the Claude source packages.

Signal works without a Voice DNA profile. Paste a draft and ask it to tighten the writing while preserving your meaning. A profile is optional, author-reviewed, and never saved by default.

## What Signal does

| Mode | Purpose |
| --- | --- |
| Compress | Remove repetition and formulaic prose without discarding consequential detail. |
| Compose | Turn supplied notes into prose without inventing facts or personal experience. |
| Polish | Make light changes to clarity, spelling, structure, and cadence. |
| Snapshot | Preserve decisions, alternatives, assumptions, evidence, and open questions for a handoff. |
| Audit | Locate and explain editorial problems without claiming to detect AI authorship. |
| Voice DNA | Build an optional, editable profile from the author's own writing. |
| Inspect | Report literal Unicode and markup artifacts using the bundled read-only script when execution is available. |

The [first-use example](examples/first-use.md) shows a cold edit with no profile, then optional voice and inspection paths. The [source note](PROVENANCE.md) explains what changed from the supplied release.

## Install

The ZIP contains one `signal-community/` plugin folder with a root `plugin.json` and `skills/signal/SKILL.md`. For a local ChatGPT desktop installation, extract it into a workspace root and add it to that workspace's `.agents/plugins/marketplace.json`:

```json
{
  "name": "local-signal",
  "interface": { "displayName": "Local Signal" },
  "plugins": [
    {
      "name": "signal-community",
      "source": { "source": "local", "path": "./signal-community" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
```

If a marketplace file already exists, add the entry to its `plugins` array. Restart ChatGPT desktop, find **Signal — Community Edition** under the local source in the Plugins Directory, install it, and start a new chat. This follows [OpenAI's local plugin packaging guide](https://developers.openai.com/plugins/build/plugins). Local marketplace support and installation permissions depend on the host and workspace.

For a developer draft, the [OpenAI plugin upload flow](https://developers.openai.com/plugins/deploy/submission) accepts a ZIP for validation and review. Uploading a draft does not publish it.

## First prompt

> Use Signal to tighten this without changing my point or making it sound generic: [paste draft]

For Voice DNA, supply your own authorized samples and ask for a **provisional profile** with evidence. Review and correct it before reuse. Do not put samples or private profiles in a public plugin package.

## Local text inspection

The optional scanner needs a local Python runtime and access to the installed plugin files. From the extracted plugin root:

```bash
python3 skills/signal/scripts/inspect_text.py /path/to/document.md
python3 skills/signal/scripts/inspect_text.py /path/to/document.md --format json
```

It reads only; it does not modify or upload the file. A ChatGPT session without local execution can discuss pasted text but must not claim to have run the scanner. The scanner cannot establish AI authorship or detect a provider's statistical watermark.

## Validate and rebuild

From the parent of the project folder:

```bash
python3 -m unittest discover -s signal-community/chatgpt/tests -v
python3 signal-community/scripts/build_release.py
python3 -m zipfile -t signal-community/releases/Signal-ChatGPT-Plugin-v0.2.1.zip
```

The tests cover the inherited inspector behavior, manifest and archive shape, reference links, original release hashes, and first-use promises. These checks do not replace a live installation smoke test.

## Privacy and limits

Signal has no account, telemetry, server, or subscription. The packaged script has no network calls. Text submitted to ChatGPT is still handled under the user's ChatGPT account and workspace settings. Signal does not send writing to third-party detectors or save Voice DNA without instruction. See [privacy](PRIVACY.md) and the [MIT license](LICENSE).

Signal is independent community software, with no implied endorsement by OpenAI, Anthropic, Ruben Hassid, How to AI, or Signal Messenger.
