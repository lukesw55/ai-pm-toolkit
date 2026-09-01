# EVALUATE — five-dimension rubric

## What it is

A structured way to score a One Pager, PRD, or product pitch on five dimensions — user empathy, structured thinking, product taste, strategic awareness, communication — each anchored 1-5, with an explicit rule for turning five scores into one verdict. Adapted from Exponent's Product Sense Interview guide, where these are the dimensions interviewers use to assess a candidate's answer.

## Why it matters

An evaluation that only ever scores things "pretty good" isn't evaluating — it's rubber-stamping. The rubric exists to make weak judgement visible before an artefact advances, the same way `pm-phase-*`'s doctrine-adversarial evals exist to make weak premises visible before they're built on. See `../../DOCTRINE.md` — EVALUATE is calibrated disagreement applied to a document instead of a conversation.

## What EVALUATE is NOT

- **A grammar/formatting check.** Polish is not judgement. A beautifully formatted PRD built on an unvalidated user type still scores low on structured thinking.
- **A pass/fail gate.** It produces a verdict with reasoning, not a binary. See `skills/WORKFLOW.md` for how this connects (or doesn't) to formal advancement.
- **Diplomacy.** Scoring generously to avoid a hard conversation defeats the point. If the lowest score is a 2, say 2 and say why.

## The five dimensions (1-5 anchors)

### User empathy

Does the artefact demonstrate real understanding of a specific user's situation, not a generic "users want X"?

| Score | Anchor |
|---|---|
| 1 | No user specified, or "users" used as an undifferentiated mass throughout |
| 2 | A user type is named but described generically, no concrete pain or context |
| 3 | A specific user type with a plausible pain point, but thin evidence behind it |
| 4 | A specific user type, an evidenced pain point, and some sense of the user's broader context/constraints |
| 5 | The artefact reads as if the author has genuinely sat with this user's problem — concrete, evidenced, and the pain point's severity/frequency is explicit |

### Structured thinking

Does the reasoning follow a traceable order (problem → evidence → options → decision), or does it jump around / assert conclusions without showing the path?

| Score | Anchor |
|---|---|
| 1 | Conclusion asserted with no visible reasoning path |
| 2 | Some structure, but key steps are skipped (e.g., solution justified without a stated problem) |
| 3 | A clear structure exists but has a gap (an unranked option set, an unexplained jump) |
| 4 | Problem, evidence, and options are all traceable in order, with one minor gap |
| 5 | Fully traceable: problem → evidence → options considered and rejected with reasons → decision, no gaps |

### Product taste

Does the proposed direction show judgement about what's actually worth building — scope discipline, a defensible MVP cut, awareness of trade-offs — versus an unfiltered feature list?

| Score | Anchor |
|---|---|
| 1 | No scope discipline — everything proposed, nothing cut, no MVP boundary |
| 2 | Some scope named but no rationale for the cut |
| 3 | A defensible MVP cut exists, but trade-offs aren't acknowledged |
| 4 | MVP cut is justified and at least one trade-off is named explicitly |
| 5 | The scope decision itself demonstrates judgement — a specific alternative was considered and rejected with a reason, trade-offs are explicit, the cut clearly serves the stated goal |

### Strategic awareness

Does the artefact connect to a broader goal, and does it consider timing, competitive context, or second-order effects, or is it reasoning in a vacuum?

| Score | Anchor |
|---|---|
| 1 | No connection to any broader goal or context |
| 2 | A goal is named but the connection between it and this specific decision is asserted, not argued |
| 3 | The connection to the goal is argued, but timing/competitive/second-order considerations are absent |
| 4 | Goal connection is argued and at least one of timing/competitive/second-order context is addressed |
| 5 | The artefact reasons one level above the immediate task — goal, timing, and at least one second-order effect (on another team, another metric, a future decision) are all addressed |

### Communication

Is the artefact structured so a reader with less context can follow it — clear ask, appropriate length, the point findable without re-reading?

| Score | Anchor |
|---|---|
| 1 | No clear ask or takeaway; reader has to reconstruct the point |
| 2 | An ask exists but is buried or the document is padded well past what the content needs |
| 3 | The ask is findable but requires more than one pass to locate |
| 4 | The ask/takeaway is clear from an early read, length is reasonable for the content |
| 5 | The point is unmistakable on a single read, structure does the work of persuading, length matches the stakes (a One Pager is one page, a PRD isn't padded) |

## Scoring discipline

1. **Score all five dimensions independently.** Don't let a strong score on one dimension inflate another — a beautifully communicated artefact (5 on communication) can still score 2 on user empathy.
2. **Report the lowest score first.** Lead with the weakest dimension and the specific gap that produced it, not the strongest one. Burying a 2 behind three 4s is the failure mode this rubric exists to prevent.
3. **The ≤2-limits-verdict rule.** A score of 2 or below on *any* dimension caps the verdict at **sharpen**, regardless of how the other four dimensions score. A verdict is never computed as an average — one real weakness is not offset by four strengths. Two or more dimensions at ≤2, or any dimension at 1, caps the verdict at **back-to-discovery**.
4. **State what would move the score.** Every score below 5 gets one sentence: what specific addition or revision would move it up.

## Verdicts

- **Proceed** — no dimension ≤2; the artefact is ready to advance through the formal gate as normal.
- **Sharpen** — at least one dimension ≤2 (but not two-or-more, and no 1); specific, addressable gaps exist. Name them and what would close them; don't just say "needs work."
- **Back-to-discovery** — two or more dimensions ≤2, or any dimension at 1; the artefact isn't a formatting problem, it's a judgement problem that needs to be worked through again, likely with `pm-phase-discover` or a BUILD walk-through (`../six-step-framework.md`) before rewriting.

## Ready-to-use template

```markdown
## EVALUATE — [artefact name]

### Lowest-scoring dimension (reported first)
[Dimension]: [score]/5 — [specific gap]

### Scores
- User empathy: [score]/5 — [one line, evidence for the score]
- Structured thinking: [score]/5 — [one line]
- Product taste: [score]/5 — [one line]
- Strategic awareness: [score]/5 — [one line]
- Communication: [score]/5 — [one line]

### Verdict: [proceed / sharpen / back-to-discovery]
[One paragraph: why this verdict, referencing the ≤2 rule if it applied]

### What would move the weakest score
[Specific, actionable — not "add more detail"]
```

## Calibration examples (from Product Sense interview transcripts)

Paraphrased, not quoted; source videos linked. These are examples of *evaluator* judgement, not just *candidate* judgement — the skill this rubric formalises.

- **Map specific statements to specific skill buckets, not vibes.** An interviewer described scoring a candidate's answer by literally mapping named moments in the response (a personal anecdote about screen time, a specific metric mentioned) to the dimension it evidenced (impact, empathy, innovation) — the rubric's "cite the evidence for the score" discipline is the same move. ([Principal AI PM Mock Interview](https://www.youtube.com/watch?v=udB8AUO4dvM))
- **A red flag is a missing concrete example, not a missing buzzword.** The same interviewer treated generic or stale claims (a reference to old news, no personal example) as the actual signal of weakness — not the absence of impressive-sounding language. This is why the anchors above reward specificity over polish at every score band.
- **Genuine strength gets named as plainly as a genuine gap.** The interviewer highlighted a specific strong moment (naming the AI field's stale-knowledge risk directly) with the same directness used for red flags — calibration cuts both ways; a 5 stated plainly is as much a part of honest evaluation as a 2 stated plainly.
- **Report uncertainty in the evaluation itself.** Reported eval results were described with explicit honesty about what was actually validated versus still uncertain, rather than presenting a score as more settled than the evidence supports — this rubric's scores are read the same way: an anchor with thin supporting evidence is a real 3, not an aspirational 4.
- **A safe answer under ethical pressure is a process answer, not a slogan.** Asked how to handle a safety/ethics trade-off, a strong answer named concrete practice (pre-planning, adversarial eval testing of harmful prompts) rather than an absolute ("we'd never ship that") — the same specificity-over-assertion pattern the structured-thinking and product-taste anchors reward.

## Shadow-gate graduation criteria

Per `skills/WORKFLOW.md`, EVALUATE currently runs as a **mandatory non-blocking shadow gate** at stage 4 (One Pager) and stage 6 (PRD): running it is required, but its result never blocks advancement — the existing formal gates stay authoritative. Promoting it to a formal (blocking) gate is a future decision, not made in this batch, and should only happen once all of the following hold:

1. **Dimensions discriminate strong from weak in practice.** Across a meaningful sample of real evaluations, scores actually spread — if every artefact scores 4s and 5s regardless of quality, the rubric isn't discriminating and isn't ready to gate anything.
2. **The rubric is stable across contexts.** The same artefact, evaluated by the same process at different times or by different reasoning paths, produces materially the same scores. A rubric that swings wildly between runs would be gating on noise.
3. **A ≤2 score reliably indicates a material problem.** Spot-checking artefacts that scored ≤2 on some dimension should show the low score correlated with an artefact that genuinely needed rework — not a rubric quirk.
4. **The false-positive rate is acceptable.** Blocking (or requiring override for) an artefact that was actually fine costs real velocity — this should be measured, not assumed, before promotion.

When these hold, promotion should prefer **dimension-level blocking** (e.g., "user empathy ≤2 blocks advancement, other dimensions inform review") over a single aggregate score threshold — the whole point of five separate dimensions is that a weak spot in one area shouldn't be laundered by strength in another, and an aggregate score reintroduces exactly the averaging failure mode the ≤2-limits-verdict rule exists to prevent.

## Files

- evaluations tied to a real artefact: append to `.ai/memory/projects/<slug>/decisions.md` alongside the One Pager/PRD they evaluated, so the shadow-gate result is on record even though it didn't block
