# Impact Brief (GTM) — stage 2

## What it is

A **lightweight, business-and-GTM-first brief** that establishes why an opportunity is worth full discovery. It opens stage 3 and stays live while discovery changes the evidence; approval funds the learning, not a frozen business case.

Think of it as the smallest doc that lets PM + PMM + leadership agree "yes, this is worth 1-3 weeks of discovery effort".

## Why it matters

Without the Impact Brief, teams either:
- skip discovery on "obvious" bets that turn out to be low-leverage
- over-invest in discovery on bets with no viable GTM path
- discover in isolation from commercial reality

The brief compresses the commercial lens (segment, willingness to buy, positioning) into a one-pager **before** discovery work begins.

## Ready-to-use template — Impact Brief

```markdown
# Impact Brief — [Problem / Opportunity name] — [YYYY-MM-DD]

**Status:** Draft | In review | **Approved for discovery** | Rejected
**PM:** @name   **PMM:** @name   **Exec sponsor:** @name
**Links:** discovery-priorities.md entry / strategy memo / discovery synthesis and opportunity tree (when available)
**Stage:** Impact Brief (stage 2 of 8)

## TL;DR
Two sentences. Problem + why we care + what we propose to discover next.

## Problem (what we're hearing)
The pain/opportunity, in user language. Quotes + data if available. ≤ 150 words.

## Target segment
- who specifically (behavioural + context — see `jtbd-segmentation.md`)
- size (rough order-of-magnitude, not precise)
- acquisition path: how do we reach them

## Business impact (rough)
Not a sizing model yet — a credible order of magnitude.
- primary metric affected: [name + rough direction + rough magnitude]
- revenue / margin / retention implication: [$ range or % range]
- strategic-fit note: [which pillar in the strategy memo]

## GTM considerations
- pricing / packaging implications (if any):
- sales motion impact: self-serve vs sales-assisted
- partner / channel consequences:
- customer comms sensitivity (is this a trust-touching area?):
- competitive positioning: does this narrow or widen our differentiator?

## Risks that would kill this
Name 2-3 things that, if true, make this not worth pursuing.
- commercial risk:
- technical risk:
- positioning / brand risk:

## What discovery must answer
Update this table as evidence arrives. If discovery cannot change the business case, the questions are too weak.

| Question | Current answer + evidence | Effect on the case |
|---|---|---|
| Is the problem real and frequent for [segment]? | [unknown / evidence] | strengthens / weakens / invalidates |
| Is willingness-to-pay or willingness-to-switch strong enough? | [unknown / evidence] | strengthens / weakens / invalidates |
| Do the GTM assumptions hold (channel reach, positioning)? | [unknown / evidence] | strengthens / weakens / invalidates |

## Discovery plan (lightweight)
- method(s): [interviews / survey / data pull / competitive / mixed]
- sample: [N users, segment, recruit criteria]
- timebox: [1-3 weeks]
- owner: [@pm]
- handoff artefact: [synthesis + ranked hypotheses → stage 3 output]

## Invalidation condition
"We will NOT advance to a One Pager if [specific finding]."

During stage 3, keep this condition and the affected impact or GTM claim current. If it fires, stop or defer the bet rather than carrying the original brief forward.

## Decision ask
- approve: advance to stage 3 (Discovery)
- reject: archive with rationale + log what we learned
- defer: reason + refresh trigger
```

## Length

One page. Two max. If it's longer, you're either over-thinking (move to discovery to learn) or under-thinking (add sharper data and resubmit).

## Impact Brief vs PRFAQ vs One Pager — don't confuse them

| Artefact | Stage | Focus | Depth |
|---|---|---|---|
| **Impact Brief** | 2 (this doc) | "should we invest discovery?" — commercial lens | light, ≤ 1 page |
| **One Pager** | 4 | "should we invest build?" — validated problem + solution direction | medium, 1 page |
| **PRFAQ** | optional (usually around stage 5-6) | executive-level "working backwards" narrative | deeper, 2-5 pages |
| **PRD** | 6 | "what exactly are we building and how will we know it worked?" | 2-5 pages |

## Common anti-patterns

- **Technical design.** The brief needs a feasibility smell-test, not an architecture proposal. Test material technical unknowns during Discovery and leave detailed design for stage 6.
- **Frozen after approval.** Discovery changes the segment, impact estimate or GTM case, but the brief still presents the stage-2 assumptions as current.
- **Full sizing theatre.** Rough order of magnitude is fine; don't over-invest in precision before discovery.
- **Solution statement.** Don't pick the solution here; pick the problem worth investigating.
- **Missing GTM.** If PMM didn't read this, it's not an Impact Brief — it's just a problem memo.
- **No invalidation.** If no discovery finding could kill the idea, the brief isn't honest.

## Who signs off

- **Driver:** PM
- **Approver:** area product director (or equivalent)
- **Contributors:** PMM, exec sponsor (for strategic bets), tech lead (feasibility smell-test)
- **Informed:** Design, analytics, CS

Use DACI from `pm-transversal-stakeholder` if the approval spans multiple functions.

## Files

`.ai/memory/projects/<slug>/impact-briefs/<topic>.md`. Publish to Confluence via `pm-transversal-docs` when approved. Linked from `discovery-priorities.md`.
