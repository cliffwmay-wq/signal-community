# First use: improve the writing without changing the decision

You do not need to create a Voice DNA profile first. Paste a draft and give Signal a simple instruction:

> Use Signal to compress this note. Keep every qualification and do not make it sound like a corporate announcement.

**Fictional source note**

> We may pilot the new intake process in January. The 14-day target is aspirational, and finance hasn't approved the budget. We think the change could reduce duplicate handoffs, but we haven't measured that yet.

**Signal edit**

> January is a possible start for the intake pilot. The 14-day target remains aspirational, finance has not approved the budget, and any reduction in duplicate handoffs is still unmeasured.

**Why this passes the meaning check:** The pilot is still tentative; the target is not a promise; finance approval is absent; and the expected benefit remains unmeasured. The edit shortens the note without supplying a false decision, result, or source.

If the author's direct phrasing matters more than compression, a lighter Polish pass could keep the original sentence structure. Signal should follow that preference rather than forcing its own house voice.

## Optional next steps

**Audit before rewriting:** Ask, “Audit this passage, show exactly what is weak and what already works, and do not rewrite until I ask.” Signal should cite excerpts and explain their effect; it should not produce an AI-origin score.

**Voice DNA:** Provide two or more non-sensitive samples you wrote yourself, ideally in the same kind of writing. Ask, “Build a provisional Voice DNA profile. Show short evidence for each observation. Let me correct it; do not save it yet.” A short or mixed-authorship sample should yield a clearly provisional profile. The profile belongs to the author and can be edited or discarded.

**Inspect literal artifacts:** If you have a local `.md` or `.txt` file and a Python-capable host, run the packaged inspector. It can report exact hidden characters, bidirectional controls, HTML comments, and related artifacts. It cannot identify who wrote the text or detect a statistical watermark. Do not remove provenance or ambiguous characters automatically.
