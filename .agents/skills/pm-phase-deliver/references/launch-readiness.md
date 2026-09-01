# Launch readiness and GTM coordination

## What it is

Coordinating the cross-functional work needed to bring a product or feature to market **successfully and safely**. A strong feature can fail commercially if launch readiness, enablement, and support planning are weak.

## Why it matters

Release is not adoption. Adoption needs awareness + enablement + support + measurement. Launch readiness ensures all four are in place before the gate opens.

## Launch stages (incremental de-risking)

```
Dark launch → Internal dogfood → Closed beta → Open beta → GA
     |              |                 |              |         |
     flag on,   our team uses     customers in   customers   ship to 100%
     no users   it in prod        under NDA      can opt in   gradually
```

Not every launch needs all stages. Use the riskiest-first principle:
- **If the risk is reliability/scale:** heavy dogfood + canary.
- **If the risk is UX confusion:** heavy beta with support touch.
- **If the risk is positioning/pricing:** heavier PMM + beta customer targeting.
- **If the risk is compliance/legal:** explicit legal sign-off + narrow rollout.

## Ready-to-use template — Launch plan

```markdown
# Launch plan — [Initiative] — [YYYY-MM-DD]

**Status:** Planning | In progress | **GA** | Paused | Rolled back
**PM:** @name   **PMM:** @name   **Tech lead:** @name
**Target GA date:** YYYY-MM-DD
**Links:** PRD / tracking plan / RAID / release-notes draft

## Launch bet recap
One sentence: what we're launching and what outcome we expect.

## Success criteria (3 / 6 / 12 weeks after GA)
| Window | Primary metric | Target | Threshold to call "success" |
|---|---|---|---|
| 3 wk | activation | X% | >= Y% |
| 6 wk | retention | X% | >= Y% |
| 12 wk | expansion / NPS | X | >= Y |

## Guardrails (must not break)
- reliability:
- support load:
- churn:
- trust / privacy incidents:

## Rollout stages + gates
| Stage | % users | Start | Duration | Exit criteria | Decision gate | Rollback criteria |
|---|---|---|---|---|---|---|
| Dark | 0% (flag only) | T-4w | 2w | instrumentation verified | PM + TL | feature flag off |
| Dogfood | internal only | T-2w | 1w | internal satisfaction + no P0 | PM + TL | flag off |
| Closed beta | 10 customers | T-1w | 2w | activation >= X%, NPS >= Y | PM + PMM | flag off + comms |
| Open beta | self-service opt-in | T+0 | 2w | same + no support spike | PM + CS | flag off + comms |
| GA | 100% gradual (10 → 25 → 50 → 100) | T+2w | 1w | monitored at each step | PM + TL | roll back to previous % |

## Enablement checklist

### Sales
- [ ] demo flow recorded
- [ ] pitch deck slide(s)
- [ ] objection handling doc
- [ ] pricing & packaging briefed
- [ ] win-loss feedback loop set up

### Customer Success
- [ ] playbook for onboarding customers to feature
- [ ] upsell/expansion talking points
- [ ] QBR slide template updated

### Support
- [ ] KB articles drafted + live
- [ ] ticket-triage criteria (what's a bug, what's expected behaviour)
- [ ] escalation path for edge cases
- [ ] staffing reviewed for expected volume bump

### Marketing / PMM
- [ ] landing / product page updated
- [ ] blog post (if public launch)
- [ ] email to interested / target customer list
- [ ] social posts scheduled
- [ ] analyst brief (for major launches)
- [ ] PR plan (if applicable)

### Documentation
- [ ] developer docs (if API/SDK)
- [ ] help-centre articles
- [ ] release-notes drafted (see `release-notes.md`)
- [ ] internal wiki updated

### Legal / Compliance
- [ ] ToS / privacy policy updates (if applicable)
- [ ] data-processing agreement updates (if EU/enterprise)
- [ ] regulatory filings (if applicable)

### Analytics
- [ ] tracking plan verified in staging + prod canary
- [ ] launch dashboard live
- [ ] alerting on primary metric + guardrails
- [ ] experiment / holdout configured

### Ops / Billing
- [ ] pricing changes in billing system (if applicable)
- [ ] provisioning automation
- [ ] usage metering

## Launch communications timeline
- T-4w: teaser internal comms + beta recruitment
- T-2w: internal enablement kickoff
- T-1w: beta starts
- T-3d: GA-prep all-hands + final readiness check
- T-0: GA announcement (email + blog + social)
- T+1d: customer-facing changelog
- T+1w: early-adopter follow-ups
- T+3w: first public readout

## Readiness review (T-3d)
A 30-min meeting with: PM, Tech Lead, Designer, PMM, Support Lead, CS Lead, Legal (if applicable), Analytics.

Each owner says one word: GREEN / YELLOW / RED. Yellow requires a specific mitigation; red blocks the launch or descopes.

## Rollback plan
- who has authority to roll back:
- how rollback happens (flag off, feature gate, version revert):
- how long the rollback takes:
- communication plan (internal + customer):
- what we preserve (data, in-flight work) during rollback

## Memory updates after GA
- launch memo: `.ai/memory/projects/<slug>/launches/<initiative>.md`
- close-out report after 6 weeks (see `post-launch-monitoring.md`)
```

## Readiness review — the rule

**One meeting, 3 outcomes:** GO (green), CONDITIONAL (yellow with named mitigations + owners), NO-GO (red → reschedule).

"Almost ready" does not exist. If a blocker exists, name it, name the owner, name the new date.

## Common anti-patterns

- **GTM involved too late.** PMM sees the feature 2 weeks before launch; messaging is generic; sales doesn't know.
- **"Release = adoption."** Ship, announce, move on. Result: features users don't know exist.
- **No launch owner.** PM assumes PMM owns launch; PMM assumes PM does. Result: gaps.
- **Missing support readiness.** Tickets pile up on day 2; support is blindsided; trust erodes.
- **No launch measurement plan.** Nobody knows if it worked.
- **Fear of rollback.** Teams treat rollback as failure. Rollback is a feature, not a bug.
- **Big-bang only.** 0 → 100% without canary. Scale or reliability surprises amplify.

## Seniority signals

- **Beginner:** supports launch tasks as assigned.
- **Intermediate:** coordinates one launch with adjacent teams using a checklist.
- **Advanced:** runs complex launches with clear readiness criteria and ownership; readiness review is genuinely informative.
- **Expert:** builds repeatable launch systems (templates + rituals + metrics of launch effectiveness) that scale across products and teams.

## Files

`.ai/memory/projects/<slug>/launches/<initiative>.md`. Publish to Confluence via `pm-transversal-docs`. Tracks launch → close-out → archived.
