# Deck storyline (QBR / exec review / kickoff / pitch)

Load when the deliverable is a slide deck: a QBR, an executive review, the stage-7 tech-team-kickoff deck, or a pitch. This file produces the **storyline** — the numbered slide sequence with titles, evidence, and speaker notes — not the `.pptx` file. It is not a slides skill; see "Render" below for what happens when a file is actually needed.

## Per-slide contract

Every slide in the storyline uses this exact shape:

```markdown
## Slide N — <title stated as a complete-sentence claim>
Evidence (proves the title):
Visual:
Speaker note:
```

- **Title is a claim, not a label.** "Activation is down in the SMB segment" is a title. "Activation metrics" is a label — reject it.
- **Evidence proves exactly the title, nothing more.** If the evidence supports a narrower or different claim than the title states, narrow the title until it matches what the evidence actually shows.
- **One idea per slide.** A slide that needs "and" in its title to stay accurate is two slides.
- **Speaker note carries the density.** Numbers, caveats, and the second-order explanation belong in the speaker note, not crammed onto the slide.

## Deck-level rules

- **Opening (slide 1) is SCQA.** Situation, Complication, Question, Answer — see `pm-transversal-comms/references/exec-email-scqa.md` for the full structure. Don't copy the S/C/Q/A labels onto the slide; the opening slide's title is the Answer, stated as a claim, with the Situation/Complication compressed into the speaker note.
- **QBR budget: 6–10 slides for 45 minutes.** See `pm-transversal-stakeholder/references/exec-reporting.md:155` for the cadence table this budget comes from, and `:54-91` for the operating-review template whose sections map onto slides: TL;DR → slide 1 (the SCQA answer), Against the plan → 1–2 slides, KPI tree movement → 1–2 slides, What we learned / What we're changing → 1 slide each, Risks for next period → 1 slide, Asks of leadership → closing slide. Collapse sections with nothing new to report rather than padding to a slide count.
- **Kickoff and pitch decks use the same per-slide contract.** A stage-7 tech-team-kickoff deck swaps the QBR section mapping for the kickoff's own beats (context → scope → sequencing → dependencies → asks); a pitch swaps in the Pitch framework from `frameworks/STORY_FRAMEWORKS.md`. The contract — claim title, evidence, visual, speaker note — does not change.
- **A visible `[NEEDS METRIC]` never becomes an invented chart.** If the source material doesn't have the number a slide wants, the slide says `[NEEDS METRIC: <what's missing>]` in the Evidence field and the Visual field stays a placeholder description, not a fabricated graph.
- **Titles and speaker notes pass through `humanizer` and, before delivery, `humanize-deliverables`** — same as any other outbound artefact this skill produces. A deck going to an exec or a customer is outbound prose; slide titles read as flat and AI-generic as easily as paragraph prose does.

## Render (optional, harness-dependent)

The storyline markdown above is the deliverable on every harness. Rendering it to an actual `.pptx` file is an optional next step that depends on what the current harness offers:

- **Claude Code with the Anthropic `pptx` skill available**: hand off to that skill with the storyline already in the per-slide contract shape — it maps directly to the skill's three verbs (create: build via its `pptxgenjs` script; edit: unzip/modify XML/rezip; read: extract via `markitdown`). Map fields as `Slide title` → slide title, `Evidence` → body content, `Visual` → the visual element or chart the skill creates, `Speaker note` → the slide's notes field. Hand off by pointing at the skill — never vendor or copy its content into this repo; it is Anthropic proprietary ("All rights reserved") and not distributed on Codex.
- **Codex, or any Claude Code session without the `pptx` skill**: no `.pptx` is produced. The storyline markdown is the final artefact — hand it to the user as-is, ready to paste into whatever deck tool they use.

This skill adds zero new dependency for either path — no bundled renderer, no new entry in `scripts/check_requirements.sh`.

## Anti-patterns

- **Label titles.** "Q3 Metrics", "Roadmap Update" — a label, not a claim. Every title must be falsifiable.
- **Evidence that doesn't match the title.** The body proves a different, usually broader, claim than the title states.
- **Slide-count padding.** Restating the same finding across two slides to hit a target count, or splitting one idea to look thorough.
- **Chart invention.** Building a plausible-looking chart for a `[NEEDS METRIC]` gap instead of leaving it visibly marked.
- **Dense slides, empty notes.** Cramming the speaker note's content onto the slide itself, leaving nothing for the presenter to add live.
- **Skipping the humanize pass because "it's just bullet points."** Slide titles and notes are prose an exec or customer will read; they need the same voice pass as a memo.
