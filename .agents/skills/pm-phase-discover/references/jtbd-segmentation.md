# JTBD, segmentation, and need modelling

## What it is

Structuring demand into meaningful user groups, jobs, contexts, and needs so the team can make targeted trade-offs instead of designing for "everyone".

## Why it matters

Segments and jobs are the scaffolding that keeps strategy, positioning, prioritisation, and GTM coherent as the product grows. Without them, every request looks equally important and the team designs for a composite average that nobody actually is.

## JTBD in one paragraph

A **Job-to-be-Done** is the progress a user is trying to make in a specific situation. Jobs are stable; solutions come and go. "Become confident I won't be late" is the job; "alarm clock" and "Google Calendar reminder" are competing solutions.

## JTBD template

```markdown
## Job: [short verb phrase]

**Situation (when):**
- trigger:
- context:
- emotional state:

**Motivation (want):**
- functional goal:
- emotional goal:
- social goal (how they want to be perceived):

**Expected outcome (so that):**
- what "done well" looks like:

**Current solutions + pains:**
- how they solve this today:
- what still hurts:

**Frequency + importance:**
- how often:
- how much it matters when it happens:
```

## Segment definition — not personas

**Behavioural segment ≠ demographic persona.** Demographics (age, role, company size) are often marketing segments. Product segments are defined by **behaviour + context + job**:

| Weak segment (marketing-ish) | Strong segment (product-ish) |
|---|---|
| "SMB users" | "Single-admin accounts with < 5 seats and weekly login pattern" |
| "Enterprise" | "Multi-team accounts with SSO, 3+ roles, quarterly license reviews" |
| "Millennials" | "Users who signed up via mobile and haven't touched desktop in 30d" |

## Segmentation template

```markdown
# Segment: [name — behavioural + context]

## Definition (filterable)
Behaviour + context criteria. If it can be queried in the data warehouse, good.

## Size + reachability
- total count (or % of user base):
- growth trend:
- acquisition path(s):

## Jobs they are trying to do
- primary:
- secondary:

## Pains / failure moments
- frequency:
- severity:

## Current solutions
- in-product:
- workarounds:
- competitors:

## Strategic fit
- does this segment align with the product strategy?
- are we under- or over-investing?
```

## Journey map — when to use

Use a journey map when the same user moves through multiple stages and the insight is **where the breakdown happens across time, not in one moment**. Otherwise a single-moment JTBD is enough.

Skeleton:

| Stage | User goal | User action | Pain / friction | Emotional state | Opportunity |
|---|---|---|---|---|---|
| Discover | ... | ... | ... | ... | ... |
| Evaluate | ... | ... | ... | ... | ... |
| Onboard | ... | ... | ... | ... | ... |
| Use (steady state) | ... | ... | ... | ... | ... |
| Upgrade / expand | ... | ... | ... | ... | ... |
| Churn risk | ... | ... | ... | ... | ... |

## Common anti-patterns

- **Decorative personas.** "Marketing Mary, 34, likes yoga." No filter, no behaviour, no job.
- **All users as one.** Designing for "the user" when 3 segments have fundamentally different jobs.
- **Power-user bias.** Building for the loudest cohort; missing the new-user activation pain.
- **Too many segments.** 9 segments that the team can't remember. 2–4 is usually right for a product area.
- **Stable demographics, shifting behaviour.** Defining segments by attributes that don't predict product decisions.

## Validation

A segment model is good when:
- the team can name the top 2–3 segments without checking notes
- prioritisation conversations reference segments ("this helps segment A but hurts segment C")
- analytics can actually produce the segment (query-able definition)
- a new team member can be taught the segments in 15 minutes

## Files

Persist to `.ai/memory/projects/<slug>/segments.md` + `jtbd.md` + `journey.md` (if used). Keep them short and navigable.
