# Decision rights — DACI / RACI / RAPID

## What it is

An explicit mapping of **who drives, who decides, who contributes, and who is informed** for a given decision. Turns "stakeholder management" from a fuzzy soft skill into a hard-skill artefact that reduces ambiguity and latency.

## Why it matters

The vast majority of "stakeholder problems" are role-clarity problems. Named driver + named approver + named contributors + named informed + a date kills 80% of decision churn.

## DACI vs RACI vs RAPID — quick guide

| Framework | Focus | Roles | Best for |
|---|---|---|---|
| **DACI** | decision-making | Driver, Approver, Contributors, Informed | most product decisions |
| **RACI** | task accountability | Responsible, Accountable, Consulted, Informed | ongoing processes, operational tasks |
| **RAPID** | complex decisions | Recommend, Agree, Perform, Input, Decide | multi-layer enterprises, heavy governance |

**Default: DACI.** Most product decisions don't need the complexity of RAPID or the task-flavour of RACI.

## DACI — the roles

- **Driver** — the person who owns the decision process. Makes it happen. Writes the recommendation. Typically the PM for product decisions.
- **Approver** — the person with final authority. Usually one person. Says yes/no. Cannot be delegated mid-stream.
- **Contributors** — people with expertise or stake who must be consulted before the decision. They shape the recommendation but do not decide.
- **Informed** — people who need to know the outcome but don't have input. Informed AFTER the decision, not during.

Critical rule: **one driver, one approver**. Multiple of either destroys the model.

## Ready-to-use template — DACI page

```markdown
# DACI — [Decision title] — [YYYY-MM-DD]

**Status:** Decision pending | **Decided** | Implemented | Superseded
**Target decision date:** YYYY-MM-DD

## Decision at stake
One sentence. The question being decided.

## Context
What prompted this decision. 3-5 sentences. Link to PRD / strategy / sizing as applicable.

## One-way or two-way door
- reversibility: [low / medium / high]
- cost of being wrong: [estimate]
- rigor calibration: [higher rigor for one-way doors]

## Roles
- **Driver:** @name
- **Approver:** @name
- **Contributors:** @name (expertise: X), @name (expertise: Y), @name (expertise: Z)
- **Informed:** @name, @name, @team-channel

## Timeline
- [date] — contributors submit input
- [date] — driver posts updated recommendation
- [date] — approver decides
- [date] — informed audience notified

## Recommendation (1 paragraph)
From the driver. Specific. Actionable.

## Options considered
- **Option A:** [1-2 sentences]
- **Option B:** [1-2 sentences]
- **Option C:** [1-2 sentences]

## Trade-offs (explicit)
- we prioritise [value] over [value] because [reason]
- we accept [cost] to get [benefit]

## Contributor input (captured async)
- @contributor-1 ([expertise]): [summary of input]
- @contributor-2: [summary]

## Risks + mitigations
- [risk] — [mitigation or acceptance]

## Open questions for approver
- [question that blocks approval]

## Decision
- **Decided:** Option [X]
- **Decided by:** @approver
- **Decided on:** YYYY-MM-DD
- **Rationale:** [1-2 sentences]

## Follow-ups
- [ ] communicate to informed list
- [ ] update PRD / strategy / roadmap
- [ ] create implementation tickets
- [ ] update memory (`.ai/memory/projects/<slug>/decisions.md`)
```

## RACI — when to use

Use RACI for **ongoing processes** (a weekly launch calendar, a quarterly roadmap review) rather than one-off decisions.

- **Responsible** — does the work
- **Accountable** — owns the outcome (one per task)
- **Consulted** — provides input (two-way)
- **Informed** — kept up to date (one-way)

Common product examples:
- running the team standup: R = scrum master, A = eng lead, C = PM, I = stakeholders
- updating the public roadmap: R = PM, A = product director, C = PMM, I = sales/CS
- incident response: R = on-call eng, A = eng lead, C = SRE + PM, I = customer team

## RAPID — when to use

Use RAPID when a decision genuinely involves multiple layers of expertise and authority that DACI doesn't capture well.

- **Recommend** — owns the analysis + recommendation
- **Agree** — must sign off before decision (can veto)
- **Perform** — executes after decision
- **Input** — provides data/expertise (cannot veto)
- **Decide** — final authority

Use RAPID for: pricing changes, platform decisions, M&A, major organisational changes.

## Decision-rights anti-patterns

- **Multiple approvers.** "This needs to be approved by product, eng, marketing, and legal." Then nobody decides. Pick ONE approver; the others become contributors or informed.
- **Driver = Approver.** PM drives AND approves their own recommendation. Remove the check.
- **Informed = silent.** Informed audience hears nothing until they hit the change in production. Communicate actively.
- **Contributor overload.** Everyone is a contributor. Then consultation takes forever. 3-5 contributors is usually right.
- **Role drift mid-process.** Driver changes, approver changes, contributors change → nobody trusts the process.
- **No timeline.** "When everyone is ready." That means never.
- **No recorded rationale.** Decision happens in a meeting; nobody writes down why.

## When to escalate

Escalate (to approver's manager or to an exec forum) when:
- approver is unavailable and decision is time-critical → propose an interim approver
- contributors strongly disagree with driver's recommendation → surface the disagreement, not hide it
- decision spans multiple approver authorities → needs shared approval structure
- decision precedent matters beyond this case → exec forum may be warranted

How to escalate cleanly: see `pm-transversal-stakeholder/references/exec-reporting.md`.

## Integration

- `pm-phase-define/references/decision-memo-daci.md` has the decision-memo template itself
- This reference focuses on role design (DACI as governance mechanism)
- `.ai/memory/_templates/decision-log.md` is the Umberto memory template for logging decisions — use it alongside DACI

## Files

DACI pages → `.ai/memory/projects/<slug>/daci/<topic>.md`. Publish to Confluence via `pm-transversal-docs`. Linked from the decisions log and the PRD.
