# Customer research design and synthesis

## What it is

Planning, running, and synthesising qualitative and mixed-method research so that product decisions rest on evidence rather than anecdotes.

## Why it matters

Experienced PMs don't "just talk to customers" — they choose the right method, sample, and synthesis approach for the specific decision blocking the team.

## Method selection

| Decision | Methods that fit | Avoid |
|---|---|---|
| "What problem do users actually have?" | Open interviews, diary studies, contextual inquiry | Surveys (too leading), NPS (too blunt) |
| "Is this hypothesis true for our segment?" | Targeted interviews w/ screener, concept tests | Unstructured interviews with random users |
| "How do users currently do X?" | Contextual inquiry, session replays, journey mapping | Hypothetical interviews ("would you use…") |
| "Which option resonates?" | Preference tests, prototype usability, survey with scoring | A/B on prototypes without usage context |
| "At what scale does this pain happen?" | Survey + segment filter, behavioural analytics | Interviews alone (wrong tool for frequency) |

## Planning template

```markdown
# Research plan — [topic]

## Decision this unblocks
One sentence. If the research doesn't change a decision, don't run it.

## Research questions (ranked)
1. ...
2. ...
3. ...

## Method + why
Choice + 1-line rationale.

## Sample
- segment(s): 
- size: (e.g., 6–8 interviews — saturation usually at 5–7 per segment)
- recruitment criteria (screener questions):

## Guide / instrument
- opening:
- core questions (open, non-leading):
- probe prompts:
- wrap-up:

## Synthesis plan
- coding scheme (open → axial)
- themes ≥ 3 users = strong; 2 = watch; 1 = anecdote
- triangulate with: [quant source]

## Output
- insight repo entries
- problem-brief revisions (if applicable)
- experiment backlog additions

## Timeline + owner
```

## Interview guide — do's and don'ts

**Do:**
- ask about past behaviour ("tell me about the last time you…")
- ask about specific artefacts they interact with
- ask "why" up to 5 times (5 Whys, but gently)
- leave silence — users fill it with real answers
- ask about workarounds ("what do you do when that happens?")

**Don't:**
- ask hypothetical future questions ("would you use a feature that…")
- lead with the feature name or solution
- ask leading yes/no questions
- interrupt a tangent that might reveal a bigger pain
- pitch the product

## Synthesis — coding in two passes

**Pass 1 — open coding:** Read/listen once. Tag every interesting excerpt with a short descriptor. Don't try to name themes yet.

**Pass 2 — axial coding:** Group tags into themes. Ask per theme:
- how many users? (≥3 out of 5-7 is a real theme)
- what segment?
- how painful is this compared to other pains they mentioned?
- what would they have paid/traded to avoid it?

**Output per theme:**
```
## Theme: [short name]
- Definition:
- Frequency: X / Y interviews
- Segment pattern: 
- Representative quotes (3):
  - "quote" — [user ID or segment]
- Product implication:
- Confidence: low / med / high
- Next research question (if any):
```

## Triangulation

Every qualitative theme should be checked against quantitative evidence before it becomes a bet:

- Theme: "checkout is confusing" → check funnel drop-off at checkout steps
- Theme: "users don't understand pricing" → check pricing-page time-on-page + conversion
- Theme: "onboarding is too long" → check time-to-first-value by cohort

If quali and quant agree → high confidence.
If quali and quant disagree → investigate (quali sampling bias? quant instrumentation gap? different segments?).

See `pm-transversal-analysis/references/triangulation.md` for deeper triangulation protocol.

## Common anti-patterns

- **Sales-call interviews.** Pitching instead of asking. Users get polite; you get no signal.
- **Loud-customer sampling.** Talking only to who complains the loudest. Segment-biased.
- **Solution-first questions.** "Would you use a dashboard for X?" leads the witness.
- **Quote-dumping.** Slide of 10 quotes, no synthesis, no implication.
- **One-method mania.** Using interviews for every question, even ones that need scale.

## Files

Persist to `.ai/memory/projects/<slug>/research/<topic>/` — plan, guide, raw notes (timestamps!), synthesis. Link themes to insight repo.
