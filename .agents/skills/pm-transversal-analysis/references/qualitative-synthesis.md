# Qualitative synthesis

## What it is

Turning raw qualitative data (interview transcripts, user-test recordings, support tickets, survey free-text, session replays, sales call notes) into **themes with evidence**. Two-pass coding (open → axial → thematic), then translate into product implications.

## Why it matters

Quotes alone are colour. Synthesis is what changes team behaviour. PMs who can turn 8 messy interviews into 3 ranked, evidenced themes within a week are disproportionately effective.

## Sampling discipline (before you start)

- **Minimum for a theme:** 3+ users out of 5-7 per segment. N=1 is anecdote.
- **Saturation check:** if the last 2 interviews are not revealing new themes, you've probably saturated for this question.
- **Segment coverage:** don't synthesise across mixed segments unless the theme truly spans all. Cross-segment themes require cross-segment presence.
- **Recency:** prefer recent data (behaviour shifts). 2-year-old interviews are archaeology, not research.

## Two-pass coding — step by step

### Pass 1 — Open coding

Read / listen to each source in full. For each interesting excerpt, attach a short tag (a phrase, not a theme).

```
Excerpt: "I usually open the dashboard, scan the top numbers, then go into the team view if something looks off."
Open codes: #dashboard-top-scan  #drill-into-team-on-anomaly  #reactive-review-pattern
```

Do NOT try to group into themes yet. The goal is to stay close to the source.

### Pass 2 — Axial coding

Group related open codes into emerging themes. Ask per theme:
- how many sources mention this?
- what segment do they share?
- how painful / important is it relative to other themes they mentioned?

Promote codes to themes only when they recur across sources.

### Pass 3 — Synthesis into implications

For each theme, translate into what it means for the product:

```
Theme: "reactive dashboard use"
- frequency: 6 of 8 interviews
- segment: B2B admins, 5-15 user accounts
- evidence strength: high
- implication: current dashboard design is correct for reactive pattern; investment in proactive alerting/notifications might shift this to proactive use (hypothesis, not conclusion)
```

## Ready-to-use template — Theme with evidence

```markdown
## Theme: [short name]

**Frequency:** X / Y sources (out of N potential)
**Segment(s):** [who]
**Evidence strength:** low / medium / high
**Confidence:** low / medium / high (and why)

### Definition
[1-2 sentences — what the theme is, in users' terms]

### Representative quotes (3-5)
> "[verbatim quote]"
> — [User ID or pseudonym], [segment], [date/timestamp in source]

> "..."
> — ...

### Supporting observations (non-quote)
- [behavioural pattern observed]
- [common phrasing across sources]

### Counter-evidence (users who did NOT express this)
- [N users] — [why they differ]

### Product implication
- [what this suggests we should investigate, change, or prioritise]
- [what it does NOT tell us]

### Triangulation with quant
- what quant signal should we look at? (see `triangulation.md`)
- quant result: [supports / contradicts / not yet checked]

### Next question
- [what we'd want to answer next to sharpen this theme]
```

## Ready-to-use template — Synthesis memo

```markdown
# Research synthesis — [Topic] — YYYY-MM-DD

**PM:** @name   **Contributors:** [research partner / others]
**Source data:** [N interviews / N transcripts / survey N / tickets N]
**Sample:** [segment + recruit criteria + date range]

## TL;DR
Three sentences. Top finding + confidence + implication.

## Research questions (from the plan)
1. Q1: [answered? partially? not?]
2. Q2:
3. Q3:

## Themes (ranked by evidence strength × implication)
### Theme 1: [name]
[template from above]

### Theme 2: [name]
...

## Surprising findings
- [unexpected observations]

## What the data did NOT answer
- [limitations of this round]

## Triangulation summary
[high-level view — which themes are quant-supported, which are quant-silent, which are quant-contradicted]

## Recommended next actions
- update problem brief / segments / one-pager
- design an experiment to test implication of theme X
- deepen research on Theme Y (more interviews, survey at scale)
- archive Theme Z as not load-bearing

## Raw data location
Links to interview transcripts, recordings, tickets folder. Keep originals accessible.
```

## Coding practical tips

- **Code in the source.** Use margin comments in transcripts (Confluence, Google Docs, Notion). Or a spreadsheet with quote + code columns.
- **Colour-code live.** Highlighting works well for surfacing theme overlap visually.
- **Quote sparingly but verbatim.** Paraphrased quotes lose evidentiary weight.
- **Preserve timestamps.** For videos/audio, note time. For transcripts, note line number. Makes reviewers' lives easy.
- **Separate raw from synthesis.** Don't edit raw transcripts; produce a separate synthesis doc that references them.

## Common anti-patterns

- **Cherry-picking quotes.** Picking 3 quotes that fit the preferred conclusion, ignoring 5 that don't. The synthesis memo should include counter-evidence.
- **N=1 generalisation.** "A customer said X, so users want X." One customer = one data point, not a theme.
- **Confusing request with pain.** "Users asked for a CSV export" is a request. "Users can't share data with non-users easily" is the pain. The request might or might not be the best solution.
- **Solution-disguised-as-theme.** "Users want a Kanban view" is a solution. "Users struggle to see blocked work" is a theme; Kanban is one possible response.
- **Over-synthesis.** Collapsing 8 themes into 2 "meta-themes" that lose all specificity.
- **Under-synthesis.** 30 themes, all 1-line. No hierarchy; decision-making impossible.
- **Anecdote-driven.** "User X told me Y" becomes "users want Y" within 48h. Not how this works.
- **Silent dropping of themes.** Themes that appear early then disappear from the memo without rationale.

## Integration

- Source of raw data: `.ai/memory/projects/<slug>/research/<topic>/` — transcripts, recordings, tickets, raw survey data.
- Synthesis memo: `.ai/memory/projects/<slug>/insights.md` — the ranked-themes repository.
- Triangulation: follow up with `triangulation.md` before committing to a bet.
- Discovery artefacts downstream: Impact Brief (stage 2), One Pager (stage 4) cite synthesis.

## Seniority signals

- **Beginner:** participates in researcher-led synthesis.
- **Intermediate:** runs coding + synthesis independently for small rounds.
- **Advanced:** synthesises across mixed-method data; translates into crisp product implications; challenges team's interpretation when data contradicts assumption.
- **Expert:** defines how the team synthesises (tools, templates, quality bar); improves institutional memory of user understanding.

## Files

Synthesis memos → `.ai/memory/projects/<slug>/insights/<topic>-<date>.md`. Raw data preserved alongside. Publish to Confluence insight repository via `pm-transversal-docs`.
