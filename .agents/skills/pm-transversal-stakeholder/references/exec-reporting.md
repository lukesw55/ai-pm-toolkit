# Executive-ready reporting and operating reviews

## What it is

Translating product work into **concise reporting** that clarifies outcomes, trade-offs, risks, asks, and next decisions for senior stakeholders. The goal is to enable decisions — not to flood leaders with activity updates.

## Why it matters

Senior PMs secure alignment and resources by presenting the right signal, not by writing status novels. Bad exec reports are PM-career-limiting; good ones are career-defining.

## What exec reporting is NOT

- **Activity updates.** "This week we completed 23 tickets and had 4 meetings."
- **Traffic-light waffle.** All green every week, then surprise red at launch.
- **Raw dashboard dumps.** Metrics without interpretation.
- **Novels.** 8 pages of context no exec will read.

## What exec reporting IS

- **Outcome-led.** What moved / didn't move / why.
- **Exception-based.** What needs attention, not what's fine.
- **Decision-oriented.** What's the ask, the decision, the option set.
- **Concise.** 1-page for weekly; 3-page max for quarterly.

## Ready-to-use template — Weekly status (to product leadership)

```markdown
# [Area] — weekly — [YYYY-MM-DD]

## North Star + top KPIs
| Metric | Last wk | This wk | Trend | Note |
|---|---|---|---|---|

## What we shipped / progressed
- [item]: one sentence + impact (if measurable yet)
- [item]: ...

## What's at risk (exception-based)
- [risk]: impact + mitigation + owner + decision date if needed

## Decisions sought this week
- [decision]: recommendation + options + date needed by

## Follow-ups from prior weeks
- [item]: status

## Looking ahead 2 weeks
- [milestone]
- [milestone]
```

Rule: if nothing is new, skip the section. Short reports with specific content beat long reports with boilerplate.

## Ready-to-use template — Monthly operating review (QBR precursor)

```markdown
# [Area] operating review — [Month / Quarter YYYY]

**Presenter:** @pm   **Audience:** product leadership, cross-functional partners

## TL;DR (30 seconds)
- top outcome this period:
- top risk / surprise:
- top ask:

## Against the plan
| Bet | Expected outcome | Actual outcome | Status |
|---|---|---|---|
| [bet 1] | [target] | [actual] | hit / miss / in progress / killed |

## KPI tree movement
[Per-metric narrative — what moved, what didn't, why. Segment view where meaningful.]

## What we learned
- [learning]: implication for strategy / roadmap / team
- [learning]:

## What we're changing
- [change]: because [reason]

## Risks for next period
- [risk]: mitigation + who + when

## Asks of leadership
- [ask]: specific, with recommendation + options + date

## Appendix (optional)
- launch scorecards
- experiment readouts
- dashboards
```

## Ready-to-use template — One-off escalation / exec memo

When a specific decision or issue needs exec attention outside normal cadence.

```markdown
# Memo — [topic] — [YYYY-MM-DD]

**To:** @exec
**From:** @pm
**Re:** [decision sought / issue / recommendation]
**TL;DR:** [one sentence]

## The situation (3 sentences)

## What's at stake (2 sentences — financial, customer, competitive, strategic)

## Options (2-3, each with pros + cons + cost in 3 lines)
- A: ...
- B: ...
- C (preferred): ...

## Recommendation + rationale (1 paragraph)

## Risks + mitigations of recommended option (3 bullets max)

## Ask
Specific. "Approve [X] by [date]" OR "30-min discussion before [date]."

## Appendix
Link to detailed docs if the exec wants to go deeper.
```

**Keep the memo to 1 page.** Appendix can be long; the memo itself cannot.

## Writing discipline

- **Exception-based.** Don't list everything on track. List what's changed, what's at risk, what needs a decision.
- **Outcome > output.** Metric movement > feature ship count.
- **Specificity.** "Significantly improved" → "moved from X to Y".
- **Ask up-front.** If there's an ask, it's in the first paragraph, not the last.
- **One memo per decision.** Don't pile 3 unrelated decisions into one memo.
- **Include options, not just problems.** Escalating without options = status.
- **Know your exec.** Some prefer TL;DR + appendix; some prefer narrative; some prefer slide decks. Adapt.

## Common anti-patterns

- **Green-green-green-RED.** Reporting everything fine until it isn't. Leadership hates surprises.
- **Output theatre.** "We shipped 5 features." Nobody cares.
- **Buried ask.** The decision the exec needs to make is on page 4.
- **Dashboard dumping.** 7 charts, no narrative.
- **"We did X, then Y, then Z."** Chronological ≠ informative.
- **Endless followups.** Items from 6 months ago still in the follow-ups section, unchanged.
- **Sanitisation.** Removing bad news from the narrative. Trust collapses when it surfaces anyway.
- **Missing decisions.** "Here's an update." But what are you asking me to decide?

## Cadence — what to report, when, to whom

| Cadence | Audience | Format | Length | Focus |
|---|---|---|---|---|
| Weekly | product leadership | 1-pager | < 500 words | exceptions + asks |
| Bi-weekly | cross-function leaders | review meeting + notes | 15 min | coordination + blockers |
| Monthly | area leadership | operating review | 3 pages / 30 min | outcomes vs plan + learnings |
| Quarterly | broader exec + stakeholders | QBR | 6-10 slides / 45 min | strategic narrative + year-ahead |
| Ad hoc | specific exec | memo | 1 page | specific decision |

## Seniority signals

- **Beginner:** provides project updates.
- **Intermediate:** reports progress clearly for one area with exception-based narrative.
- **Advanced:** builds concise, decision-oriented narratives that prompt specific leadership decisions.
- **Expert:** becomes the go-to for portfolio-level reporting that shifts investment and strategy.

## Files

- weekly: posted in Slack / Confluence in team space; link from `.ai/memory/projects/<slug>/reports/`
- monthly: `.ai/memory/projects/<slug>/operating-reviews/<YYYY-MM>.md`
- escalation memos: `.ai/memory/projects/<slug>/exec-memos/<topic>-<date>.md`
- quarterly QBR: dedicated folder linked to strategy refresh
