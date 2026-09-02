# Output templates

Flexible starting points. Adapt language, headings, length, and section names to the user's request. The first eight templates cover general formats; the last five are PM-specific and were added when this skill was forked into the PM skills repo.

---

## 1. Narrative assignment response

```markdown
# [Title]

[Concrete hook: a moment, contradiction, example, or problem.]

[Thesis: direct answer to the assignment.]

## [Beat 1: Context]
[Background the prompt requires.]

## [Beat 2: Tension / Problem]
[Key conflict, misconception, gap, or stakes.]

## [Beat 3: Analysis / Evidence]
[Develop the argument using provided evidence. Use placeholders for missing sources.]

## [Beat 4: Turning Point / Insight]
[What the analysis reveals.]

## [Conclusion: Takeaway]
[Answer the prompt again with a stronger final insight.]
```

## 2. Story strategy brief (planning artefact)

```markdown
## Story strategy
- Objective:
- Audience:
- Format:
- Narrative spine:
- Chosen framework:
- Primary emotion (if any):
- Key proof:
- Gaps:

## Beat outline
1.
2.
3.
4.
5.
```

## 3. Article / blog story

```markdown
# [Specific, curiosity-driven title]

[Lede: a concrete scene, contrast, or sharp claim.]

## [The problem hidden in plain sight]
[Context + friction.]

## [What changed]
[Turning point, insight, discovery.]

## [Why it matters]
[Implications for the audience.]

## [How to apply it]
[Steps, principles, recommendations.]

## [Closing line]
[Memorable takeaway.]
```

## 4. Video script

```markdown
# Video script: [Title]

## Hook (0:00–0:10)
Visual:
Voiceover:
On-screen text:

## Setup
Visual:
Voiceover:

## Tension
Visual:
Voiceover:

## Reveal / insight
Visual:
Voiceover:

## Payoff
Visual:
Voiceover:

## CTA
Visual:
Voiceover:
```

## 5. Slide storyline

Each slide title is a complete-sentence claim and the Evidence field proves exactly that claim. For a full deck (QBR budget, SCQA opener, render handoff) see `references/deck-storyline.md`.

```markdown
# Slide storyline: [Title]

## Slide 1 — [Claim title]
Evidence (proves the title):
Visual:
Speaker note:

## Slide 2 — [Claim title]
Evidence (proves the title):
Visual:
Speaker note:

## Slide 3 — [Claim title]
Evidence (proves the title):
Visual:
Speaker note:

## Closing slide — [Claim title]
Evidence (proves the title):
Visual:
Speaker note:
```

## 6. Case study

```markdown
# Case study: [Protagonist / project / client]

## Snapshot
- Protagonist:
- Challenge:
- Intervention:
- Result:
- Evidence gaps:

## The challenge
[What was difficult and why it mattered.]

## The approach
[What was done, in sequence.]

## The turning point
[Insight, decision, or experiment that changed the trajectory.]

## The result
[Use only provided proof. Mark missing metrics as `[NEEDS METRIC]`.]

## What others can learn
[Generalisable takeaway.]
```

## 7. Lesson story

```markdown
# Lesson story: [Topic]

## Opening puzzle
[Relatable scenario or misconception.]

## What students need to notice
[Key observation.]

## Explanation
[Clear explanation with analogy or example.]

## Practice moment
[Activity, question, mini-task.]

## Reflection
[What learners should now understand.]
```

## 8. Social sequence

```markdown
# Social story sequence: [Theme]

## Post 1 — Hook
[One strong tension or question.]

## Post 2 — Context
[What the audience needs to know.]

## Post 3 — Conflict
[Problem or misconception.]

## Post 4 — Insight
[The reveal.]

## Post 5 — Application
[How the audience can use it.]

## Post 6 — CTA
[Next action.]
```

---

## 9. Discovery synthesis story *(PM)*

```markdown
# Discovery synthesis: [Topic / segment / question]

## Question
[The discovery question, stated as it was originally framed.]

## Method
- Sample: [n, segment, recruitment method]
- Instruments: [interview guide, survey, dashboard, replay set]
- Period: [date range]

## Finding
[Plain-language statement of what the evidence shows.]

## Pattern
[The recurring shape across customers / sessions / segments. Cite evidence by ID.]

## Implication
[What this pattern means for the product / segment / bet. One paragraph.]

## Open
- [What's still unknown]
- [What would falsify the pattern]
- [`[NEEDS SOURCE: …]` for any gap]

## Evidence index
- [ID-01]: [short label] — [link or pointer]
- [ID-02]: …
```

## 10. One-pager opener *(PM)*

The opener is the first 200–400 words of a one-pager. The rest of the one-pager (sizing, GTM, plan) is built with `pm-phase-define` / `pm-phase-discover`; this template only covers the narrative opener.

```markdown
# [One-pager title — name the bet, not the framing]

## The customer and the job
[Who this is for, in one sentence. Name the segment and the JTBD in concrete terms.]

## What we see today
[Friction observed in the evidence. Cite inline:
- Interview ID-XX said […]
- Dashboard X shows […]
- Ticket ABC-123 captured […]
]

## What we tried (or didn't)
[Prior attempts or absence of attempts. Honest about the gap.]

## Why now
[The specific change in context that makes this the right moment, not just "we should do it eventually."]

## The bet
[One sentence stating what we'll build and why. Feature scope lives later in the one-pager — not here.]
```

## 11. PRD problem statement *(PM)*

Drop-in for the first section of a PRD, before solution scope.

```markdown
## Problem statement

### Customer + JTBD
[One sentence.]

### Friction observed
[2–4 bullets, each citing evidence. No internal jargon unless the PRD audience uses it natively.]

### Stakes
[Why this matters now, with the cost of inaction stated.]

### Non-goals
[1–3 bullets naming what this PRD explicitly does not address.]

### Bet
[One sentence — the wedge.]
```

## 12. Decision memo / DACI rationale *(PM)*

```markdown
# Decision memo: [Decision name]

**Decision:** [The call, in one sentence.]
**Owner:** [Driver, per DACI]
**Date:** [YYYY-MM-DD]
**Reversibility:** [Easy / hard / one-way door]

## Why now
[The trigger that forced the decision.]

## Context
[Minimum required background. Cut anything the reader already knows.]

## Options considered
| Option | Main upside | Main trade-off |
|---|---|---|
| [Chosen] | […] | […] |
| [Alternative 1] | […] | […] |
| [Alternative 2 — if any] | […] | […] |

## Choice and reasoning
[Why this option won, in one or two sentences.]

## Acknowledged risk
[What could go wrong, named not buried. One sentence.]

## What we decide later
[What's deliberately deferred, with the trigger that would re-open the question.]
```

## 13. Release notes narrative *(PM)*

External-facing release notes. Bypass the "we are thrilled to announce" register.

```markdown
# [Product / area] — [release name or date]

## What changed
[One sentence. User-language. No internal codename in the title.]

### [Change 1 — user-visible name]
[What it does, in their language.]
[Why it matters — only when non-obvious.]
[How to use it: [pointer to UI / doc / API].]

### [Change 2 — user-visible name]
[…]

## Smaller changes
- [Trivia bullet]
- [Trivia bullet]

## What's next
[Only if there's a credible follow-up. Otherwise omit this section entirely.]
```

---

## How to pick a template

| If the user said… | Start with… |
|---|---|
| "story for the exec memo" / "decision memo" / "DACI rationale" | Template 12 |
| "PRD opener" / "problem statement" | Template 11 |
| "one-pager narrative" / "open the one-pager" | Template 10 |
| "release notes story" / "draft the release notes" | Template 13 |
| "discovery synthesis story" / "synthesise these interviews" | Template 9 |
| "case study from this customer" | Template 6 |
| "slide storyline" / "QBR narrative" / "deck flow" | Template 5 |
| "video script" / "social video" | Template 4 |
| "social sequence" / "thread / posts" | Template 8 |
| "lesson" / "teaching" / "explainer for newcomers" | Template 7 |
| "essay" / "academic assignment" / "homework" | Template 1 |
| "blog post" / "article" / "write-up" | Template 3 |
| "I just want a story strategy first" | Template 2 |

When two templates fit (e.g. case study and one-pager opener both work for a customer story), pick the one closer to the audience's expectations and reading habit.
