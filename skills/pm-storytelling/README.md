# pm-storytelling

A skill for Claude Code and Codex that turns raw PM source material — discovery transcripts, evidence dossiers, briefs, AI-generated drafts, scattered notes, assignments — into audience-ready narrative artefacts.

## What it does

Extracts a story spine (tension → insight → change → takeaway) from messy source material, picks the right narrative framework for the audience, and produces a draft in the format the user asked for. Supports PM-native formats (one-pager opener, PRD problem statement, exec / decision memo, release notes, discovery synthesis, slide / QBR storyline, customer case study, pitch deck) plus generic prose (essay, article, video script, lesson, social sequence).

## Where it sits in the stack

| Stage | Skill | Role |
|---|---|---|
| Generation | **`pm-storytelling`** *(this)* | Build the story — spine, beats, format |
| Voice polish | [`humanizer`](../humanizer/SKILL.md) | Strip AI-writing patterns, run the "what still makes this AI?" pass |
| Outbound gate | [`humanize-deliverables`](../humanize-deliverables/SKILL.md) | Hard-enforced sentinel before Confluence / Slack / customer / exec |

Default chain for outbound work:

```
draft with pm-storytelling
        ↓
polish with humanizer
        ↓
mark with humanize-deliverables  (hook hard-blocks publish/send without this)
        ↓
ship via Confluence / Slack / Jira / customer email
```

For internal scratchpads or `.ai/memory/` updates, the chain stops at step 1.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Workflow, phases, integration with humanizer/humanize-deliverables |
| `frameworks/STORY_FRAMEWORKS.md` | 13 narrative frameworks (9 general + 4 PM-specific) and a selection heuristic |
| `templates/OUTPUT_TEMPLATES.md` | Fillable templates per format (8 general + 5 PM-specific) |
| `rubrics/QUALITY_RUBRIC.md` | 1–5 scorecard across 7 dimensions, plus a binary outbound voice gate |
| `references/format-editorial-rules.md` | Per-format editorial rules (what to say once the template is in front of you) |
| `references/deck-storyline.md` | Per-slide assertion-evidence contract, QBR slide budget, optional harness-dependent `.pptx` render handoff |
| `references/progressive-loading.md` | Loading map: which support file to read for which task |
| `examples/sample_one_pager_opener.md` | Worked example: scattered interview notes → one-pager opener |

## Lineage

Forked from the standalone `assignment-storytelling` skill (zip distribution, 2026-04). Adaptations for this repo:

- Renamed `assignment-storytelling` → `pm-storytelling` to match the repo's `pm-*` / `humanize-*` / `eng-*` convention
- Description rewritten to be pushy (per skill-creator guidance) and bilingual PT/EN
- Added an explicit **"Working with humanizer and humanize-deliverables"** section in `SKILL.md` defining the split of labour
- Reduced the in-line "Anti-Generic Filter" from a duplicate mini-catalogue to a light first-pass; full coverage delegated to `humanizer`'s pattern catalogue
- Added 4 PM-specific frameworks (Discovery Synthesis Arc, PRD Opener, Decision Memo Narrative, Release Notes Narrative) and 5 PM-specific templates (one-pager opener, PRD problem statement, decision memo, release notes, discovery synthesis story)
- Added a binary **voice-gate pre-requisite** to the rubric for any artefact that ships outbound
- Replaced the original "feedback reflection" example with a one-pager opener example using PM evidence
- Removed the upstream `install.sh` script — this repo *is* the install location
- Added `references/deck-storyline.md`: an assertion-evidence per-slide contract and a QBR slide budget for decks. Rendering to `.pptx` is an optional handoff to the Anthropic `pptx` skill where the harness offers it, never a bundled renderer — the storyline markdown is the deliverable on both harnesses

## Suggested user prompt

```text
Use pm-storytelling.

Input type: discovery notes / generated content / brief / assignment / raw notes
Target format: one-pager opener / PRD problem statement / exec memo / release notes / discovery synthesis / case study / slide storyline / article / essay / video script / social sequence / lesson
Audience:
Tone:
Length:
Must include:
Must avoid:

Source:
<<<
[paste assignment, evidence, generated content, or notes]
>>>
```

## Notes

Zero-dependency. No scripts, no npm packages, no external services. The skill is pure markdown, loaded on demand by either harness. The optional `.pptx` render described in `references/deck-storyline.md` adds no dependency here: it points at a skill the harness may or may not offer.
