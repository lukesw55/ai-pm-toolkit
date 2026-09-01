# Prioritisation frameworks

## What it is

Applying an explicit method to compare options and rank work according to impact, effort, confidence, timing, and strategic alignment. Prioritisation is one of the clearest hard-skill differentiators in senior PM work.

## Why it matters

Prioritisation forces trade-offs under scarcity. A PM who cannot defend "why this over that" does not have a prioritisation system — they have opinions.

## Frameworks — when each fits

| Framework | Best for | Limitation |
|---|---|---|
| **RICE** (Reach × Impact × Confidence / Effort) | Quantitative-ish comparison across diverse initiatives | Reach/Impact estimates are often guesswork; confidence multiplier is the real honesty |
| **Value vs Effort** (2×2) | Small teams, short horizon, visual alignment | No strategic-fit dimension; oversimplifies |
| **Cost of Delay / WSJF** | Known release windows, multiple teams sharing capacity | Requires honest CoD estimation (users tend to over-claim) |
| **Kano** | Understanding user-satisfaction thresholds (basic vs performance vs delighter) | Needs customer survey data; not for ranking initiatives directly |
| **MoSCoW** | Fixed-scope releases (contract / regulatory deadlines) | Too binary for steady-state prioritisation; M becomes "everyone thinks theirs is M" |
| **Opportunity scoring** | Where the bet is the segment/problem, not the feature | Needs discovery evidence; use with `pm-phase-discover/opportunity-hypothesis.md` |
| **Weighted scorecard** | Regulated / cross-functional / executive-visible bets | Slow; scores can hide judgement; needs governance |

## RICE — template

```markdown
## RICE scoring — [scope + date]

| Initiative | Reach | Impact | Confidence | Effort | RICE | Notes |
|---|---|---|---|---|---|---|
| A | 10k users/qtr | 3 (high) | 80% | 3 wk | 800 | evidence: ... |
| B | 500 users/qtr | 1 (low) | 50% | 1 wk | 250 | ... |

### Scoring rules (pin these)
- Reach: users affected per time period (be specific about period + segment)
- Impact: 0.25 (minimal), 0.5, 1, 2, 3 (massive) — anchored to primary metric movement
- Confidence: 0–100% — penalises hand-wavy estimates
- Effort: person-weeks total (eng + design + PM + analytics)
- RICE = (Reach × Impact × Confidence) / Effort
```

**Pitfall:** RICE treats a 3-week effort and a 3-week-calendar-but-needs-4-teams effort the same. Honest effort = sum of all team-weeks, not a single engineer's.

## Value vs Effort (2×2)

Simple. Plot each initiative on effort (x) × value (y). Quadrants:
- High value / low effort → **do now**
- High value / high effort → **plan carefully** (slice!)
- Low value / low effort → **maybe** (or drop)
- Low value / high effort → **drop**

Use for visual alignment in a planning session. Don't use as the only ranking method for cross-area work.

## Cost of Delay / WSJF

**Cost of Delay** = what we lose (revenue, risk increase, opportunity cost) for each unit of time this is delayed.

**WSJF (Weighted Shortest Job First)** = Cost of Delay / Job Size.

Best when:
- multiple teams share a backlog or release train
- some initiatives are genuinely time-sensitive (regulatory, partnership, seasonal)

Worst when:
- all CoD estimates are "high" (nobody is forcing honest discrimination)

## Kano

Categorises features by satisfaction impact:
- **Basic / must-have** — absence causes dissatisfaction; presence doesn't delight (login works, data doesn't disappear)
- **Performance** — satisfaction scales linearly with quality (speed, accuracy, depth)
- **Delighter** — unexpected; high satisfaction; but becomes "basic" over time

Use Kano to decide **which features to invest quality in**, not to rank across initiatives.

## Opportunity scoring (for discovery-anchored bets)

When the bet is the problem (not the feature), score opportunities directly:

| Opportunity | Pain severity | Frequency | Segment reach | Strategic fit | Evidence strength | Reachability | Total |
|---|---|---|---|---|---|---|---|
| ... | 5 | 4 | 3 | 5 | 4 | 4 | 25 |

Then commit to the top 2–3 as funded opportunities; solutions come from `pm-phase-develop`.

## Adapting the framework to context

The expert move is not picking a framework — it's **adapting it**:

- Add a **strategic-fit penalty** to RICE for initiatives that drift from pillars
- Add a **confidence floor** — drop anything below 30% without more discovery
- Add a **dependency cost** — initiatives that unblock others get a bonus
- Add a **learning value** — small tests that de-risk bigger bets get weighted up

Pin the adaptation in writing. Un-documented adjustments = gaming.

## Anti-patterns

- **Score as truth.** Treating the arithmetic as the decision rather than as a forcing function for discussion.
- **Judgement hiding.** Using the framework to avoid stating "I think X because Y".
- **Weak evidence.** Scoring Reach/Impact without any data — confidence should drop to 20–30%.
- **Never recalibrating.** The framework was right 2 years ago; evidence has changed; nobody updated the rules.
- **Framework tourism.** Switching frameworks every quarter. Pick one, adapt it, and stick with it for long enough to trust it.
- **Score gaming.** Stakeholders learn how to inflate Reach/Impact to game the score. Counter by pinning definitions and requiring evidence links.

## Output format

```markdown
## Prioritisation — [scope, horizon]

### Framework + adaptations
[Name] with [adjustments, pinned]

### Inputs + evidence links
Each initiative's scoring references a data source or assumption.

### Ranked initiatives
1. ...
2. ...
3. ...

### What we are NOT funding this horizon
Explicit, with 1-line rationale each.

### Recalibration trigger
What would change the ranking (new data, shifted strategy, competitor move).
```

## Files

`.ai/memory/projects/<slug>/priorities.md` + `prioritisation-rubric.md` (the pinned rules). Linked from strategy memo and roadmap.
