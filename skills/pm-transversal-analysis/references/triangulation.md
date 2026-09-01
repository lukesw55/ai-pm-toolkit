# Triangulation (quali + quant)

## What it is

**Cross-referencing qualitative themes with quantitative signals** to strengthen or challenge a conclusion. When both say the same thing, confidence is high. When they disagree, the disagreement itself is the insight — investigate it.

## Why it matters

Quali without quant = anecdote risk. Quant without quali = confident guessing about cause. The expert move is to never commit to a bet based on only one type of evidence — triangulate by default, not on request.

## The triangulation protocol

For each important claim:

1. **State the claim.** One sentence, falsifiable.
2. **Find qualitative evidence.** Themes, quotes, observations. How strong?
3. **Find quantitative evidence.** Metric direction, magnitude, segment pattern, CI. How strong?
4. **Compare.** Do they support each other? Contradict? One is silent?
5. **State combined confidence.** low / medium / high, with reasoning.
6. **Name what would change the answer.**

If you cannot find BOTH quali and quant for a claim, the claim is at-risk. Not wrong — just under-supported.

## Ready-to-use template — Triangulation memo

```markdown
# Triangulation — [Claim] — YYYY-MM-DD

## Claim
[One sentence. Specific. Falsifiable.]
Example: "B2B admins in 5-15 seat accounts disengage from the product in weeks 3-4 after activation because the dashboard becomes visually overwhelming as more teams are added."

## Qualitative evidence
**Source:** [N interviews / tickets / sales calls / ...]
**Sample:** [segment + recruit criteria + date range]

**Themes supporting this claim:**
- Theme 1 (N sources): [quote + implication]
- Theme 2 (N sources): [quote + implication]

**Themes contradicting this claim:**
- [any counter-evidence]

**Quali strength:** low / medium / high (and why)

## Quantitative evidence
**Sources:** [dashboards / queries / experiments]

**Signals supporting:**
- metric X for segment Y: [magnitude + CI]
- funnel drop in step Z: [evidence]
- retention curve shape for cohort W: [evidence]

**Signals contradicting:**
- [any counter-signal]

**Signals that are silent (data gap):**
- [what we'd want to measure but cannot]

**Quant strength:** low / medium / high

## Comparison

| Aspect | Quali says | Quant says | Aligned? |
|---|---|---|---|
| Existence of problem | ... | ... | ✅ / ⚠️ / ❌ |
| Segment pattern | ... | ... | ... |
| Timing / trigger | ... | ... | ... |
| Magnitude | ... | ... | ... |

## Combined confidence
low / medium / high — based on [strength of both sides + alignment + counter-evidence]

## Implications
- for product: [what to do differently]
- for metrics / tracking: [what to measure we aren't yet]
- for further research: [what to investigate]

## What would change this conclusion
- [observation that would reduce confidence or flip the claim]

## Decision impact
- [what we'd prioritise or defund based on this]
```

## The four patterns

### Pattern 1 — Aligned (quali + quant both support)
Highest confidence. Act on it.

```
Quali: 6 of 8 interviewees describe dashboard overwhelm in weeks 3-4
Quant: retention drops 35% between weeks 2 and 4 for 5-15 seat accounts specifically
→ HIGH confidence; investment in dashboard simplification for this segment is warranted
```

### Pattern 2 — Quali strong, quant silent
Medium confidence. Worth acting on but consider instrumenting to measure.

```
Quali: users describe confusion during upgrade flow
Quant: no tracking currently on upgrade flow micro-steps
→ MEDIUM confidence; add instrumentation first, then re-evaluate; but the quali is strong enough to consider a low-risk fix in parallel
```

### Pattern 3 — Quant strong, quali silent
Medium confidence. Easy to over-interpret — find the *why* before acting.

```
Quali: no interviews on this topic yet
Quant: 40% drop in primary metric for enterprise cohort, sustained for 3 weeks
→ MEDIUM confidence something is wrong; immediately launch qualitative investigation before shipping a fix — the "why" matters
```

### Pattern 4 — Disagreement
Most interesting case. The gap is the insight.

```
Quali: "users love the new feature"
Quant: adoption is 4% after 6 weeks; engagement flat
→ LOW confidence in "love"; investigate sampling bias (were interviewees already enthusiasts? recency effect?); re-assess
```

### Bonus pattern — Both weak
Don't commit. More research before bet.

## Anti-patterns

- **Quali rubber-stamping quant.** Running 2 interviews to confirm a quant finding, then calling it triangulated. N=2 doesn't validate.
- **Quant rubber-stamping quali.** Running a quick query that matches the quali narrative, without checking segment / baseline / seasonality.
- **Dismissing quali as "soft".** "That's just anecdote" dismisses evidence the quant instrumentation can't capture.
- **Over-weighting quant because it feels objective.** Numbers can be as biased as quotes — instrumentation gaps, sample issues, seasonality.
- **Cherry-picking.** Choosing the one quant cut that supports quali, or the one quote that supports quant.
- **Ignoring silent signals.** "We have quant but no quali on this" is a limitation, not an oversight to paper over.
- **Single-source confidence.** Shipping based on only one type of evidence when both were possible to collect.

## When NOT to triangulate (or when it's genuinely not possible)

- **Very new products / features** with no quant baseline — lean on quali until there's data to triangulate with.
- **Very common problems with overwhelming quant** (e.g. a crash that affects 20% of users) — don't delay fixing.
- **Speed-sensitive decisions** where the cost of being wrong is small and reversible — quali-only is fine for directional calls.
- **Discovery phase** specifically designed to generate hypotheses, not validate them — quant comes later.

The rule is **aim for triangulation on material bets**, not every micro-decision.

## Using MCP for triangulation

- Quali side: read transcripts, tickets, survey free-text via `Read`; publish synthesis via `pm-transversal-docs`.
- Quant side: query via PostHog MCP (see `quantitative-analysis.md` for patterns).
- Cross-reference in a triangulation memo that links both.

## Seniority signals

- **Beginner:** uses quali OR quant; rarely both for the same claim.
- **Intermediate:** remembers to check both sides for major bets.
- **Advanced:** triangulates by default; notices disagreement; investigates gaps.
- **Expert:** designs the team's triangulation practice (tools, cadence, quality bar); triangulation becomes cultural.

## Integration

- Upstream inputs: `qualitative-synthesis.md` (themes) + `quantitative-analysis.md` (signals).
- Triangulation memos cite both. They are the artefact that closes the evidence loop.
- Feed into Impact Briefs, One Pagers, PRDs, experiment decisions.

## Files

`.ai/memory/projects/<slug>/triangulation/<claim>-<date>.md`. Linked from the discovery synthesis and the decision memos that depend on the claim.
