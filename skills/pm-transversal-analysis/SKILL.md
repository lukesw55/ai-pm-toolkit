---
name: pm-transversal-analysis
description: >-
  Cross-phase skill for **qualitative synthesis, quantitative analysis, triangulation
  of quali+quant evidence, and parsing of videos/audio/transcripts** into product
  insight. Invoke whenever the user hands over interview transcripts, user-test
  recordings, call notes, survey free-text, support tickets, session replays,
  analytics queries, or funnel/cohort data — and expects insight, not just a summary.
  Trigger on "sintetize essas entrevistas", "triangule quali e quant", "analyse these
  transcripts", "cohort analysis", "funnel interpretation". Produces thematic
  syntheses with evidence quotes, cohort/funnel interpretations, and triangulated
  findings that make the team act differently. For interviews at the very start of a
  discovery (problem still soft, JTBD undefined), use `pm-phase-discover` first to
  scope the research, then chain to this skill for synthesis — this skill assumes the
  upstream framing is set.
---

# PM Transversal — Qualitative + Quantitative + Media analysis

> Transversal skill. The analytical layer that sits under every phase. Discovery without synthesis is anecdote; analytics without qualitative grounding is confident guessing.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## When to use this skill

Invoke when:

- interview transcripts, user-test recordings, or session replays need to be turned into insight
- survey free-text, support tickets, NPS comments, or in-product feedback must be coded and synthesised
- a funnel, retention, cohort, or segmentation analysis needs interpretation (not just numbers)
- quali and quant evidence conflict and must be reconciled (triangulation)
- a video/audio recording or its transcript is the main input (user test, sales call, exec interview)
- an "analysis" is needed but nobody has said whether it's quali, quant, or both

Skip for pure dashboard consumption (no synthesis needed) — that stays in `pm-phase-deliver/references/product-analytics.md`.

Trigger phrases: "sintetize essas entrevistas", "analyse these transcripts", "assista esse vídeo", "extraia insights", "coding temático", "triangule quali e quant", "cohort analysis", "funnel interpretation", "qualitative themes", "review session replays".

For interviews at the very start of a discovery (problem still soft, JTBD undefined, segments still in flux), use `pm-phase-discover` first to scope the research and only then chain to this skill for synthesis — this skill assumes the upstream framing is set and the work is "what does the evidence mean for product?".

## Prime directive

**Evidence → insight → decision.** Quotes alone are colour. Numbers alone are noise. The expert move is synthesis that changes behaviour: "because of X (quali evidence) and Y (quant evidence), we should Z."

## Core sub-skills

### 1. Qualitative synthesis (interviews, transcripts, feedback)

Turn raw text/audio/video data into themes with evidence. Open coding → axial coding → thematic synthesis. Distinguish user pain from user request.

Outputs: theme map, coded excerpts with timestamps/locators, insight repository entry (problem, evidence, segment, implication), opportunity list ranked by evidence strength + frequency.

Anti-patterns: cherry-picking quotes, no sampling discipline, confusing request with pain, "analysis paralysis" vs acting on clear themes, n=1 generalisation.

→ Deep-dive: `references/qualitative-synthesis.md`

### 2. Quantitative analysis (funnels, cohorts, retention, segments)

Interpret behavioural data structurally — not just "it went up". Understand what the funnel/cohort *means* for the hypothesis.

Outputs: funnel breakdown, cohort retention narrative, segment comparison, statistical framing of the claim (CI, practical significance, guardrails), decision implication.

Anti-patterns: dashboard worship, no segments, correlation-as-cause, p-hacking, reporting averages that hide segment harm.

→ Deep-dive: `references/quantitative-analysis.md`

### 3. Triangulation (quali + quant)

Cross-reference qualitative themes with quantitative signals to strengthen or challenge a conclusion. If quali says "checkout is confusing" and quant says "drop-off at step 3 is 40% higher than benchmark", the insight is stronger and the fix is targeted. If they conflict, investigate the gap.

Outputs: triangulation memo (claim → quali evidence → quant evidence → confidence → action), conflict log (where they disagree and why), sharpened hypothesis for next experiment.

Anti-patterns: using one type to validate the other without checking assumptions, over-weighting quant because it feels objective, ignoring quali because it feels soft.

→ Deep-dive: `references/triangulation.md`

### 4. Media and transcript parsing (video, audio, transcripts)

Process videos/audio files/transcripts (interviews, user tests, sales calls, session replays with narration) to extract insight. Use timestamps as locators; preserve raw signal; synthesise in a second pass. If a transcript is not available, request one or use available tooling to generate one before analysis.

Outputs: timestamped highlights, coded excerpts, thematic synthesis (§1), key-quote list, follow-up-question list for next research session.

Anti-patterns: "I watched the video and vibed with it", summarising before coding, losing the raw reference, treating transcripts as ground truth without checking against audio on load-bearing quotes.

→ Deep-dive: `references/media-transcript-parsing.md`

## Workflow

1. **Load the raw data** — transcripts, recordings, dashboards, exports. If media is provided, confirm transcript is available or request one; use Read on provided text files.
2. **Classify the ask** — quali, quant, triangulation, or media-first?
3. **Sampling discipline** — for quali, check sample size and segment coverage. For quant, check cohort definitions and exclusion rules.
4. **Code then synthesise** — for quali, resist the urge to summarise before coding. For quant, define the hypothesis before slicing.
5. **Triangulate** — always ask "what does the *other* type of evidence say about this claim?"
6. **State confidence and implication** — every insight ends with "confidence: low/med/high; implication: X".
7. **Persist** — insight repo → `.ai/memory/projects/<slug>/insights.md`; experiment plan if needed → `experiments.md`; raw signal preserved (links or copies) — don't lose originals.

## Output contract

```text
## [Synthesis / analysis title]

### Inputs
- raw sources + sample size + time range

### Method
- how analysis was done (coding scheme, cohort logic, triangulation protocol)

### Findings (ranked by evidence strength)
1. [Claim]
   - Qualitative evidence: [theme, N quotes, timestamps/locators]
   - Quantitative evidence: [metric, cohort, magnitude, CI if available]
   - Confidence: low/med/high
   - Implication: [what to do differently]
2. ...

### Conflicts or gaps
### Recommended next action
### Files / raw artefacts preserved
```

## Integration

- `pm-phase-discover` — feeds research synthesis, segment models, opportunity ranking.
- `pm-phase-deliver` — interprets post-launch metrics, A/B results with quali context.
- Transversais: `pm-transversal-docs` (synthesis published in Confluence insight repo), `pm-transversal-stakeholder` (exec memo citing triangulated evidence).
- MCP tools: when PostHog MCP is available (product analytics), this skill can query directly (`query-run`, `insights-list`, etc.; the `mcp__<server>__` prefix varies by environment) for quantitative inputs. When the team uses Zoom/Gong/Otter, transcript files come in via Read.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is ranked findings + implications + confidence; Standard is the full synthesis memo with method + findings + quotes; Caveman is the top 3 findings in 2 lines each.

## Success criteria

- insights change team behaviour (new experiment, scope change, deprecation)
- raw signal is preserved and retrievable
- quali and quant are triangulated by default, not on request
- video/transcript analysis produces timestamped evidence, not vibes
- the team stops confusing "I talked to a customer" with "I have evidence"
