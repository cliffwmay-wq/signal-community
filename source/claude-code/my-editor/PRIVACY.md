# Signal privacy & provenance

Signal's bundled tools perform **no telemetry, analytics, upload, account creation, networking, or automatic document modification**. The optional Python inspector reads local UTF-8 text and reports findings; it does not rewrite source files.

**Important distinction:** Text that you paste into Claude, or provide through Claude Code, is processed by that platform according to its own terms, settings, and retention policies. Signal cannot independently guarantee privacy within the Claude service. Use only writing samples you are allowed to share; remove sensitive identifying details, client information, internal communications, names, and credentials before submission.

Voice DNA profiles are **opt-in**, human-readable, editable, and controlled by the author. There is no account or shared database for profiles. The plugin does not save them unless the user requests saving. Files named `VOICE_PROFILE.md` and folders named `profiles/` are git-ignored by default as a safeguard, not an access-control guarantee.

Signal does not determine AI authorship, prove human origin, remove statistical text watermarks, or guarantee that an institutional AI detector will classify a document in any particular way. It identifies exact Unicode/markup artifacts where present and makes editorial quality suggestions. Do not remove or falsify required AI-use disclosures or other provenance records.

This is community software independent of Anthropic, Claude, Ruben Hassid and the How to AI community. No endorsement is implied.
