# Opportunity Solution Tree and assumption map — stage 3 to 4 bridge

## What it is

The artefact that carries discovery into a bet without losing the thread. An Opportunity Solution Tree (Teresa Torres) hangs everything off one **outcome**: the opportunities (user needs or pains, in the users' words) that could move it, the solutions considered for each opportunity, and the experiments that test the riskiest assumptions behind the chosen solution. The **assumption map** is the tree's last layer made explicit: every leap of faith under the chosen solution, typed, scored, and either tested or accepted by a named owner.

It sits between `discovery/<topic>/synthesis.md` (stage 3) and `one-pager-<topic>.md` (stage 4 in `skills/WORKFLOW.md`). The one-pager cites the node it comes from; the tree shows which alternatives were considered and which assumptions are still open.

## Why it matters

Without the tree the pipeline jumps from "problem framed" to "bet chosen": the one-pager arrives with one solution, no visible alternative, and a confidence level nobody can trace back to evidence. The tree makes the choice auditable (which opportunity, ranked against which others, with which sibling solutions rejected) and turns "we assume users will..." into a row with an owner and a test.

## Ready-to-use template — Opportunity Solution Tree

```markdown
# Opportunity Solution Tree — [topic] — [YYYY-MM-DD]

**Outcome (O):** [product outcome as metric + direction + horizon, from the impact brief or strategy memo]
**Source synthesis:** discovery/<topic>/synthesis.md ([date])

## O1 — [opportunity in the users' words]
- Evidence: [synthesis theme, n of N interviews, quant signal]
- Scorecard: [total] · rank [n of N] (dimensions without evidence: unknown / not scored)
- Solutions: O1-S1 [solution] · O1-S2 [solution]   (at least two per pursued opportunity)
- Experiments: O1-S2-E1 [smallest test of the riskiest assumption; hypothesis template in opportunity-hypothesis.md]

## O2 — [opportunity]
...

## Parked opportunities
- O3 — [opportunity]: [why parked: scorecard rank, off-strategy, out of reach this horizon]
```

IDs are the traceability contract: `O<n>` opportunity, `O<n>.<m>` sub-opportunity (optional), `O<n>-S<k>` solution, `O<n>-S<k>-E<j>` experiment, `O<n>-S<k>-A<m>` assumption. The one-pager cites the solution node (`O1-S2`) and lists the open `A` rows.

Scoring reuses the six-dimension scorecard in `references/opportunity-hypothesis.md` (pain severity, frequency, segment reach, strategic alignment, evidence strength, reachability). Any dimension the synthesis does not support is marked `unknown / not scored`, stays out of the total, and is never guessed.

## Assumption map

For the chosen solution, list every assumption that has to be true for it to work. This is Torres's third habit and the artefact-side counterpart of `inference-discipline`.

| ID | Assumption | Type | Importance (1-5) | Evidence strength (1-5) | Status | Test or decision |
|---|---|---|---|---|---|---|
| O1-S2-A1 | Approvers act on an in-app inbox within the day | desirability | 5 | 3 | inferred: 11/14 interviews name the pain, none has seen an inbox | O1-S2-E1 |
| O1-S2-A2 | The inbox ships without a new email provider | feasibility | 3 | 4 | verified: platform team confirmed on [date] | none needed |

Types: desirability (users want it), viability (the business can sustain it), feasibility (we can build it), usability (users can use it), ethical (we should do it).

Importance: 1 = if false, the solution still works with a cosmetic change; 2 = a secondary benefit is lost, the primary metric target still holds; 3 = the solution needs a material redesign or misses the primary target; 4 = the parent opportunity is no longer served by this solution; 5 = the solution has no reason to exist (outcome unreachable) or breaks an ethical or legal constraint.

Evidence strength: 1 = one opinion or one anecdote (one person, one account); 2 = several anecdotes from the same kind of source; 3 = a pattern across three or more interviews or one quantitative signal, not triangulated; 4 = qualitative and quantitative evidence triangulated; 5 = tested directly (experiment or production data on this segment).

Risk = Importance × (6 − Evidence strength), from 1 to 25. Test the highest risk first; break ties toward the weaker evidence. One test, one assumption.

Status is derived from the evidence and written out in words, never as a bracket tag: `verified` needs strength 4 or 5 with the source named (synthesis theme, data pull, experiment id); `inferred` is strength 3 with the basis named; `unverified` is strength 1 or 2 with the verification step named. The bracket tags of `inference-discipline` are conversation-only markers and never appear in artefacts, which is why this column is prose.

Exit rule for the stage-4 handoff: every `unverified` assumption has either a test (`O<n>-S<k>-E<j>`) or an explicit accepted-risk decision recording the owner, the rationale, and the condition or date that reopens it. An `unverified` assumption with neither blocks the handoff. A missing test never turns into accepted risk by default. `verified` and `inferred` assumptions do not block (an `inferred` one can still get a test later).

## Rules

- The outcome is a metric with a direction and a horizon, never a feature or an output ("ship the inbox").
- Every opportunity comes from synthesis evidence; quote the theme and the count. No opportunity without a source.
- At least two solutions per pursued opportunity. The one-pager's rejected alternative is a sibling solution from this tree.
- Experiments reuse the hypothesis template in `references/opportunity-hypothesis.md`; the tree does not copy it.
- A material feasibility assumption names the tech lead or architect who reviewed it and the smallest technical test that could change the decision. This is early evidence, not detailed architecture.
- Prune explicitly. A parked opportunity keeps its row and its reason so nobody re-proposes it in six months.
- A solution that arrives without a parent opportunity (a stakeholder ask, a competitor feature, a demo request) is attached to an opportunity, mapped as an assumption to test, or parked. It does not become a one-pager.

## Anti-patterns

- **Solution-first tree.** One solution with an opportunity written afterwards to justify it.
- **Orphan solution.** A solution node with no parent opportunity. It is an idea, not a bet.
- **Outcome as output.** "Launch the new approval flow" is a deliverable; the outcome is the metric it should move.
- **Desirability-only map.** Every row is "users will want it" while feasibility, viability and ethics stay unexamined.
- **Customer said so.** One account's request scored as verified demand. One account is one anecdote: strength 1.
- **Invented scores.** A dimension scored without evidence to make the total look complete. Write `unknown / not scored`.

## Files

The tree lives beside the synthesis as `discovery/<topic>/opportunity-tree.md` and is the stage-3 handoff artefact named in `skills/WORKFLOW.md`. Experiments persist to `.ai/memory/projects/<slug>/experiments.md` as today. The one-pager (`pm-phase-define/references/one-pager.md`) links back to the tree node and lists the open assumption rows.
