# Opportunity assessment and hypothesis design

## What it is

Turning evidence into explicit hypotheses about where value exists, how to test it, and what the smallest useful learning step should be.

## Why it matters

Discovery becomes actionable only when a PM can **rank opportunities** and **design low-cost ways to reduce uncertainty**. Without this, discovery becomes a library of observations that never turns into bets.

## The distinction: idea vs opportunity vs hypothesis

- **Idea** — "We could add AI to the dashboard."
- **Opportunity** — "New users miss the high-value feature in session 1; a first-session activation intervention could move primary metric by X."
- **Hypothesis** — "If we surface the high-value feature via contextual tooltip on empty state, session-1 activation will increase from 38% to ≥50% within 2 weeks in the test group."

Expert PMs do not fund ideas. They rank opportunities, translate the top ones into falsifiable hypotheses, and then design tests.

## Opportunity scorecard

For each candidate opportunity:

| Dimension | Score (1–5) | Note |
|---|---|---|
| **User pain severity** (how bad when it happens) | | quoted evidence / data |
| **Frequency** (how often it happens) | | data source |
| **Segment reach** (how much of our target user base) | | size + definition |
| **Strategic alignment** (fits our strategy pillars) | | which pillar |
| **Evidence strength** (how confident we are) | | quali + quant |
| **Reachability** (can we actually address it?) | | tech + GTM feasibility |

Ranking by sum is a starting point. The real move is using the table to force comparison and expose weak spots.

## Hypothesis template

```markdown
# Hypothesis: [short name]

## Belief
We believe that [user/segment] has [problem/pain] in [context], and that [intervention approach] will [expected effect], because [evidence / reasoning].

## Primary metric
Which metric moves if this is true? Baseline value. Target magnitude that would be practically meaningful.

## Guardrails
Metrics that must NOT move negatively (reliability, retention, support load, trust).

## Smallest test
The cheapest way to learn if the belief is false. Options in order of cost:
1. Desk research / existing data pull
2. Fake-door / concept test (paint, no code)
3. Prototype usability test (click-through)
4. Limited MVP (gated cohort)
5. A/B at scale

## Invalidation condition
"This hypothesis is false if [specific observation]."

## Decision rule
If primary metric [moves ≥ X / does not move ≥ Y] and guardrails [hold / break], we will [ship / iterate / drop].

## Cost + timeline
Days of which roles.
```

## Cost-of-learning hierarchy

Rough order of cost and speed to evidence. Start low.

1. **Desk check** — look at existing data before designing anything. Often ends the hypothesis.
2. **Fake-door** — a button or link that measures intent without building the feature. Use carefully and ethically (be transparent post-click).
3. **Concept test** — 3–5 users reacting to a concept description or mock.
4. **Prototype** — clickable, no backend. Usability + desirability signal.
5. **Painted-door MVP** — looks like a real feature, minimal backend. For rare-path features.
6. **Gated MVP** — real feature, one segment, feature flag. For measurable impact.
7. **A/B at scale** — expensive but definitive.

Don't skip to 7 when 1 would have done.

## Anti-patterns

- **"We'll know it when we see it."** No invalidation condition = belief, not hypothesis.
- **Build-then-validate.** Polished prototypes before risks are resolved.
- **Too many risks per test.** One test, one risk; otherwise results are uninterpretable.
- **Vanity baselines.** Comparing against "before any measurement" instead of a real cohort.
- **Opportunity sprawl.** 15 "top opportunities". Without forced ranking, priorities blur.

## Decision after the test

- **Green** (primary moved, guardrails held) → scale or ship.
- **Yellow** (partial signal) → iterate the hypothesis, not the framework. What specifically needs to change?
- **Red** (no signal or guardrails broken) → drop. Log what was learned so nobody re-proposes the same bet in 6 months.

## Files

Persist hypotheses to `.ai/memory/projects/<slug>/experiments.md` using the template in `.ai/memory/_templates/experiment-log.md`. Results go back in as the experiment closes.
