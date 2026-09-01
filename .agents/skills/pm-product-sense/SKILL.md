---
name: pm-product-sense
description: Cross-phase skill for **product sense** — the structured judgement that turns ambiguity into a defensible product decision. Two modes. **BUILD** walks a decision through six steps (clarifying questions → strategy/goal → user types → pain points → solutions → MVP), each step constraining the next. **EVALUATE** acts as a critical interviewer, scoring a one-pager/PRD/pitch on five dimensions (user empathy, structured thinking, product taste, strategic awareness, communication) with 1-5 anchors and a proceed/sharpen/back-to-discovery verdict. Adapted from Exponent's Product Sense Interview guide (tryexponent.com/blog/product-sense-interview). Invoke BUILD for "how would you approach...", an ambiguous product decision, or an interview-style product-sense question; invoke EVALUATE to pressure-test a one-pager or PRD before it advances. Runs as a **mandatory non-blocking shadow evaluation** at stages 4 and 6 — see `skills/WORKFLOW.md`.
---

# PM Product Sense — structured judgement under ambiguity

> Transversal, cross-phase skill. BUILD is most useful in Discover/Define when a decision is genuinely open; EVALUATE is most useful right before a One Pager (stage 4) or PRD (stage 6) advances, as a second, more adversarial read before the formal gate.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## When to use this skill

Invoke **BUILD** when:

- the ask is genuinely ambiguous ("how would you improve X", "what should we build for Y") with no problem statement yet handed to you
- a product decision needs to be reasoned through from first principles rather than assembled from an existing brief
- practising or producing an interview-style product-sense answer

Invoke **EVALUATE** when:

- a One Pager or PRD is about to advance and needs a critical, structured second read
- a pitch or recommendation needs pressure-testing before it goes to stakeholders
- the shadow evaluation at stage 4 or stage 6 is required (see `skills/WORKFLOW.md` — non-blocking, but running it is not optional)

Skip BUILD when the problem is already validated and framed — use `pm-phase-define` or `pm-phase-develop` directly. Skip EVALUATE for artefacts that aren't decision-shaped (status updates, release notes — those go through `pm-transversal-comms`).

## Prime directive

**Product sense is judgement made checkable, not a vibe.** The six BUILD steps and the five EVALUATE dimensions exist so that "this feels right" turns into a decision someone else can audit — what was assumed, what was ruled out and why, and what evidence would change the call.

## Core sub-skills

### 1. BUILD — six-step decision framework

Clarifying questions → strategy/goal → user types → pain points → solutions → MVP. Each step constrains the next: skipping straight to solutions without naming user types and pain points first is the single most common product-sense failure.

Outputs: a structured decision walk-through, mappable onto a One Pager (`pm-phase-define/references/one-pager.md`).

Anti-patterns: jumping to a solution before naming the user and the pain point it addresses, picking one user type "out of the gate" instead of enumerating candidates first, no explicit vision/goal statement, features with no MVP cut.

→ Deep-dive: `references/six-step-framework.md`

### 2. EVALUATE — five-dimension rubric

User empathy, structured thinking, product taste, strategic awareness, communication — each scored 1-5 against explicit anchors. The lowest-scoring dimension is reported first, not buried; a score of ≤2 on any dimension limits the overall verdict regardless of how the other four score.

Outputs: a scored evaluation with verdict (proceed / sharpen / back-to-discovery), the lowest dimension surfaced first, and what would move the score.

Anti-patterns: averaging away a real weakness, scoring generously to avoid a hard conversation, evaluating polish (writing quality) instead of the underlying judgement.

→ Deep-dive: `references/evaluation-rubric.md`

## Workflow

**BUILD:**

1. Ask clarifying questions before assuming scope — don't silently pick an interpretation.
2. State the strategy/goal this decision serves, explicitly.
3. Enumerate user types (plural) before picking which to focus on.
4. Surface pain points per user type, ranked by severity — not a flat list.
5. Generate solution candidates tied back to a specific pain point; reject weak ones with a stated reason, not silently.
6. Cut to an MVP against the stated goal — what's in, what's explicitly out, how success is measured.

**EVALUATE:**

1. Read the artefact once for what it's actually claiming, not for polish.
2. Score all five dimensions independently against the anchors in `references/evaluation-rubric.md`.
3. Report the lowest score first, with the specific gap that produced it.
4. Apply the ≤2-limits-verdict rule before compositing a verdict.
5. State what evidence or revision would move the weakest dimension.

## Output contract

```text
## BUILD — [decision]
### Clarifying questions asked
### Strategy / goal
### User types considered (+ which is targeted, and why)
### Pain points (ranked)
### Solution candidates (+ rejected, with reason)
### MVP (in / out / success metric)

## EVALUATE — [artefact]
### Lowest-scoring dimension (reported first)
### Scores — user empathy / structured thinking / product taste / strategic awareness / communication (1-5 + evidence)
### Verdict — proceed / sharpen / back-to-discovery
### What would move the weakest score
```

## Integration

- Stage 4 (One Pager) and stage 6 (PRD): **mandatory non-blocking shadow evaluation**. Running EVALUATE is required before advancing; its result does not block the formal gate, which stays authoritative. See `skills/WORKFLOW.md` for the exact wording and `references/evaluation-rubric.md` for graduation criteria toward a future formal gate.
- `pm-phase-define/references/one-pager.md`: BUILD's six steps map onto the One Pager's five-unlocks quality bar (see `references/six-step-framework.md` for the mapping).
- `pm-phase-develop/references/prd-writing.md`: EVALUATE reads a PRD the same way it reads a One Pager — for judgement, not formatting.
- Doctrine: EVALUATE is where calibrated disagreement is the whole job — see `../DOCTRINE.md`. A rubric that only ever scores high isn't evaluating.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is the BUILD output contract or the EVALUATE scorecard as written above; Standard adds the reasoning behind each score/step; Caveman is the verdict/MVP line only.

## Success criteria

- BUILD answers name a user type and a pain point before any solution appears
- BUILD answers include at least one rejected solution with a stated reason
- EVALUATE scores lead with the lowest dimension, not the highest
- EVALUATE never produces a "proceed" verdict alongside an unaddressed ≤2 score
- shadow evaluations run at stage 4 and stage 6 without blocking advancement
