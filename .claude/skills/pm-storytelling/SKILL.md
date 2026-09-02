---
name: pm-storytelling
description: >-
  Turn raw PM source material — discovery transcripts, evidence dossiers,
  briefs, AI-generated drafts, scattered notes, assignments — into
  audience-ready narrative artefacts. Use whenever the output needs a spine
  (tension → insight → change → takeaway) rather than a flat summary. Covers
  PM-native formats (one-pager opener, PRD problem statement, exec / decision
  memo, release notes, discovery synthesis, QBR / slide-deck storyline with an
  optional .pptx render, customer case study, pitch deck) and generic prose
  (essay, article, video script,
  lesson, social sequence). Trigger on "rascunha a narrativa", "monta a
  história", "esse texto está sem alma", "give this a spine", "make this
  memorable" — the full trigger list lives in the skill body. Pushy by design
  — when source material has a real tension/insight/change to surface, prefer
  this over plain summarisation. If the request is to tighten prose without
  changing its shape, use humanizer instead.
---

# pm-storytelling: turn source material into narrative without losing the assignment

Forked from the standalone `assignment-storytelling` skill and adapted for the PM skills repo. The job is the same: take an assignment, brief, evidence pile, or rough draft and produce a clear, compelling narrative that preserves the original intent. The change is the lane: this skill **generates** narrative; voice polish and outbound delivery are someone else's job in this repo (see next section).

## Trigger phrases

The frontmatter description carries a subset; this is the full list. Invoke on: "rascunha a narrativa", "monta a história", "transforma essas notas em narrativa", "story for the exec memo", "PRD opener", "one-pager narrative", "release notes story", "discovery synthesis story", "case study from this customer", "pitch storyline", "slide narrative", "monta o deck", "QBR deck", "gera o pptx", "make this less generic", "give this a spine", "esse texto está sem alma", "make this memorable".

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## Why this exists

A lot of PM output reads like an assembled report — facts stacked on facts, no spine, no point of view. Storytelling adds a spine. But "more story" is not the goal — clarity is. Every scene, hook, metaphor, and example must serve the assignment, not decorate weak content. When source material is thin, the right move is to mark gaps explicitly (`[NEEDS SOURCE]`), not invent.

## When to use / when not

Use this skill when the user gives or references:

- a discovery synthesis, evidence dossier, or interview transcript pile that needs a narrative spine
- a one-pager / PRD / decision memo that needs a problem-statement opener with tension
- AI-generated content that reads flat, generic, or disconnected
- raw notes, brainstorms, transcripts, product notes, or lesson material
- a request to make content more narrative, persuasive, educational, memorable, or presentation-ready
- an assignment, exercise, brief, prompt, or rubric (the legacy use case)

Skip this skill for:

- pure copy-editing where the user wants the same shape, just cleaner
- structured ticket fields (Jira labels, components, fixVersion)
- raw machine output — JSON, logs, CSVs, terminal commands
- code, config, schemas
- internal scratchpads or `.ai/memory/` updates that nobody outside the team will read

If the request is "tighten this prose" without "give it a spine" — use `humanizer` directly, not this skill.

## Working with humanizer and humanize-deliverables

This skill always pairs with `humanizer` for voice polish, and with `humanize-deliverables` when the artefact ships outbound (Confluence, Slack, customer, leadership). Storytelling and humanizing are distinct jobs in this repo. Don't merge them.

| Skill | Role | When |
|---|---|---|
| `pm-storytelling` (this) | **Generate** narrative — spine, beats, format | Source needs structure or arc |
| `humanizer` | **Polish** voice — strip AI-writing patterns | Voice quality matters (long-form, exec-facing, customer-facing) |
| `humanize-deliverables` | **Gate** outbound prose — hard-enforced sentinel | Before Confluence / Slack / customer / exec / release notes |

Default chain when the artefact ships outside the immediate team:

1. **Draft here** — produce the story (Phases 0–6 below).
2. **Polish with `humanizer`** — read `../humanizer/SKILL.md`, apply its pattern catalogue, and run its mandatory final pass ("what still makes this AI-generated?"). Don't reimplement that catalogue inside this skill — the inline anti-generic filter (Phase 5) is a tiny first sweep, not a substitute.
3. **Run `humanize-deliverables` before delivery** — read `../humanize-deliverables/SKILL.md`. The gate is hard-enforced for `createConfluencePage`, `updateConfluencePage`, `slack_send_message`, `slack_send_message_draft`, Slack canvases, and Jira comments. Forgetting it blocks the call.

Skip the humanizer/gate pass for: internal scratchpads, `.ai/memory/` updates, tickets you're triaging, raw analytical output, or anything you'll rewrite anyway. When unsure, run them — the cost of one extra pass is seconds; the cost of AI-tinted prose hitting a customer or a director is reputational drag.

## Core principles

1. **Assignment first.** Preserve the task objective, constraints, audience, and required deliverable before adding narrative polish.
2. **No empty drama.** Every scene, hook, metaphor, and example must support the goal. PM storytelling is dragged forward by evidence, not by emotional arc.
3. **Evidence anchored.** Do not invent facts, data, citations, claims, company results, customer quotes, or personal experiences. Mark gaps with `[NEEDS SOURCE: …]`.
4. **Audience fit.** Adapt tone, structure, depth, and examples to the actual reader (evaluator, customer, eng director, GPM, learner). When in doubt, default to a lean house style: direct, evidence-first, occasionally bilingual PT/EN.
5. **One strong spine.** Every output needs a single sentence that survives the test below.
6. **Reusable formats.** The same source can become an essay, an article, a video script, a slide storyline, a case study, a one-pager, a memo, or a social sequence. Pick one primary format; flag others as adjacent assets if useful.
7. **Iterate visibly when source is messy.** First extract ingredients, then propose the route, then write. Don't pretend a thin pile of notes is ready to ship.

### The narrative-spine test

Every generated output must have one sentence that fits this template:

> *This is a story about [protagonist] who faces [friction], discovers [turning point], and ends with [takeaway].*

If the spine is weak, refine it before drafting. PM-flavoured example:

> *This is a story about active customers who plateau after 90 days, the team that mistook adoption for stickiness, the discovery that drove churn was account-management drift, and the bet that closes that gap.*

---

## Phase 0 — detect mode

| Mode | When the user gives you… | Goal |
|---|---|---|
| A — Assignment-to-Story | An assignment, prompt, rubric, brief, or task | Satisfy the task while making the answer narrative |
| B — Generated-to-Story | AI-generated or drafted content | Preserve substance, strip generic phrasing, add spine |
| C — Raw-Notes-to-Story | Notes, bullets, transcripts, fragments | Extract spine, organise material |
| D — Story Adaptation | An existing story that needs a different format / channel / audience / length | Preserve story core, change delivery |
| E — Multi-Asset System | Source + a request for several outputs (article + slide storyline, script + social posts, case study + exec summary, lesson + activity) | Consistent story world across assets |

## Phase 1 — intake

If the user already provided enough information, proceed without asking. Ask **at most three** objective questions, only when critical info is missing:

1. **Target format** — essay, article, script, slide storyline, one-pager, PRD opener, exec memo, release notes, case study, lesson, social sequence
2. **Audience and tone** — who reads it, what register
3. **Constraints** — word count, language (PT / EN / both), rubric, citations, deadline, brand voice, forbidden claims, required sections

Defaults when nothing is specified:

- Format: narrative article or structured story draft
- Language: match the user's language; if the user mixes PT/EN in the source, mirror that
- Tone: clear, professional, direct
- Length: concise but complete
- Claims: only what's in the provided material; mark unknowns as `[NEEDS SOURCE]`

## Phase 2 — source deconstruction

Before writing, extract three layers (briefly, in scratchpad form is fine — the user does not need to see them unless asked):

### Assignment map

- Objective — what the task actually asks for
- Deliverable — required format and scope
- Audience / evaluator — who judges success
- Required criteria — rubric, learning outcomes, business goals, constraints
- Non-negotiables — topics, sources, terms, frameworks, citations, length
- Risk — where storytelling could accidentally violate the assignment

### Story ingredients

- Protagonist — person, team, company, customer, learner, idea, problem, community
- Desire — what the protagonist wants
- Friction — obstacle, misconception, constraint, tension, unanswered question
- Stakes — why it matters now
- Turning point — insight, discovery, decision, experiment, conflict, shift
- Resolution — result, lesson, recommendation, next step
- Takeaway — what the audience should remember or do

### Content quality check

| State | What it means | What to do |
|---|---|---|
| Ready | Enough detail to write a final story | Draft the final output |
| Thin | Usable but lacks examples, proof, stakes | Draft with placeholders; flag what's missing |
| Conflicted | Unclear claims, inconsistent structure, mixed objectives | Surface the conflict to the user; ask to resolve before drafting |
| Unsupported | Requires facts, citations, or data not provided | Refuse to invent; return a gap list |

When source is Thin / Conflicted / Unsupported, proceed with placeholders or push back. Inventing facts to round out the arc is the exact failure mode this skill exists to prevent.

## Phase 3 — choose narrative architecture

Pick one primary framework. See `frameworks/STORY_FRAMEWORKS.md` for the full catalogue (13 frameworks).

Default choices:

| Situation | Framework |
|---|---|
| Discovery synthesis | Question → Method → Finding → Pattern → Implication → Open |
| One-pager opener | Why now → What we found → What we'll do → Sizing → Risk |
| PRD problem statement | Customer + JTBD → Friction observed → What we tried → Why now → Bet |
| Exec / decision memo (DACI) | Decision → Why now → Context → Options weighed → Choice + reasoning → Acknowledged risk |
| Release notes | What changed for the user → Why it matters → How to use → What's next |
| Persuasive recommendation | Problem → Stakes → Evidence → Recommendation |
| Customer case study | Context → Challenge → Approach → Evidence → Learning → Next |
| Slide / QBR storyline | Promise → Problem → Stakes → Insight → Solution → Proof → Implications → Action; per-slide contract and deck rules in `references/deck-storyline.md` |
| Pitch | Why now → Pain → Shift → Solution → Proof → Ask |
| Academic / business analysis | SCQA + Insight Arc |
| Personal reflection | Moment → Conflict → Realisation → Change |
| Educational | Curiosity Gap → Explanation → Example → Application |
| Short-form video / social | Hook → Tension → Reveal → Payoff → CTA |

## Phase 4 — output planning

Before final writing, produce a compact plan when useful (skip only if the user said "just the final text"):

```markdown
## Story strategy
- Objective:
- Audience:
- Format:
- Narrative spine:
- Chosen framework:
- Key beats:
  1.
  2.
  3.
- Evidence available:
- Gaps / placeholders:
```

This makes assumptions visible and lets the user redirect cheaply before bigger writing happens.

## Phase 5 — generate the story

Use the most relevant template from `templates/OUTPUT_TEMPLATES.md`.

### Universal output rules

- Open with a concrete hook, not a generic introduction
- Use specific nouns, verbs, examples, and constraints from the source
- One idea per paragraph
- Show tension early
- Avoid moralising, clichés, and vague transformation language
- Preserve assignment requirements even when improving style
- Use headings only when they aid readability or match requested format
- Do not invent metrics, testimonials, citations, names, events, dates, or outcomes
- Mark missing facts as `[NEEDS SOURCE: …]`
- End with a clear takeaway, recommendation, reflection, or call to action

### Inline anti-generic check (light)

While drafting, watch for the most flagrant generic openings: *"in today's fast-paced world"*, *"this essay will discuss"*, *"throughout history"*, *"in the rapidly evolving landscape of"*, *"at its core"*, *"it is crucial to note that"*, *"a game-changer"*, *"unlock the potential"*. If one slips in, replace with concrete context, tension, or a direct claim.

This is a first sweep, not a complete check. The full pattern catalogue lives in `humanizer/SKILL.md` and its `references/`; run that skill on the draft when voice quality matters, and always before outbound delivery.

## Phase 6 — format-specific rules

Pick the deliverable format and load two files: `templates/OUTPUT_TEMPLATES.md` for the fillable structure, and `references/format-editorial-rules.md` for the per-format editorial rules (what to say once the template is in front of you — covers essay, one-pager, exec memo, release notes, article, video script, slide storyline, case study, lesson, social sequence). When the deliverable is a deck (QBR, exec review, stage-7 kickoff, pitch), also load `references/deck-storyline.md` for the per-slide contract, the slide budget, and the optional render handoff.

## Phase 7 — quality review

Before final response, check the following. If any check fails, revise — don't ship.

1. **Assignment alignment** — does it answer the original task and respect non-negotiables?
2. **Narrative spine** — is the protagonist / friction / turning point / takeaway sentence clear?
3. **Specificity** — are there concrete details from the source, not generic statements?
4. **Evidence integrity** — are unsupported facts marked, not invented?
5. **Audience fit** — does tone match the intended reader?
6. **Format fit** — does it follow requested structure and length?
7. **Memorability** — at least one strong image, contrast, example, or sentence?
8. **Voice gate (outbound only)** — has the draft been through `humanizer` and, if it ships externally, marked via `humanize-deliverables`?

The voice gate item is binary, not a score. If the artefact is outbound prose and hasn't been humanised, the work is not done.

See `rubrics/QUALITY_RUBRIC.md` for the 1–5 scoring scorecard with minimum bars.

---

## Default response shape

Use this default unless the user requests otherwise:

```markdown
## Story strategy
- Objective:
- Audience:
- Format:
- Narrative spine:
- Gaps / assumptions:

## Final story
[Generated output]

## Why this works
[2–4 bullets explaining alignment with assignment, narrative structure, and audience]
```

For quick requests, drop "Why this works" and return only the final story. For outbound artefacts, append a one-line note: *"Run `humanizer` on this draft before delivery; if it ships to Confluence / Slack / customer / exec, run `humanize-deliverables` first."*

---

## Support files

Load these only when needed; they're referenced from this SKILL.md:

- `frameworks/STORY_FRAMEWORKS.md` — 13 narrative frameworks + selection heuristic (PM-specific frameworks added: Discovery Synthesis, PRD Opener, Decision Memo, Release Notes)
- `templates/OUTPUT_TEMPLATES.md` — fillable templates per format (PM-specific templates added)
- `rubrics/QUALITY_RUBRIC.md` — 1–5 scorecard across 7 dimensions plus a voice-gate pre-requisite for outbound
- `examples/sample_one_pager_opener.md` — worked example showing assignment → strategy → final story → why-this-works
- `references/deck-storyline.md` — per-slide assertion-evidence contract, QBR slide budget, and the optional harness-dependent `.pptx` render handoff
