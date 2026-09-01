# Cross-functional delivery orchestration

## What it is

Coordinating **design, engineering, analytics, research, legal, operations, support, and GTM** work so that a product change lands coherently. Product value is realised through orchestration, not PM heroics.

## Why it matters

Most product failures are not build failures — they're coordination failures. Features ship without support prepared, without sales enabled, without analytics ready, without legal clearance. Orchestration makes sure the whole thing lands.

## The functions — typical responsibilities in a launch

| Function | Owns | Typical dependency on PM |
|---|---|---|
| **Engineering** | build, NFRs, production readiness | PRD + acceptance + NFRs + tracking spec |
| **Design** | UX, interaction, accessibility, motion | problem + constraints + states to cover |
| **Analytics / Data** | tracking plan review, dashboards, experiment setup | event schema + primary metric + cohort logic |
| **Research** | ongoing discovery, usability tests | research questions + sample |
| **Product Marketing (PMM)** | positioning, release messaging, launch plan | bet + target customer + differentiation |
| **Sales** | enablement, objection handling, pipeline impact | customer-facing benefits + pricing + demo flow |
| **Customer Success / Support** | onboarding guides, KB articles, ticket triage | user-facing changes + edge cases + migration |
| **Legal / Privacy / Compliance** | policy review, ToS, data handling | data inventory + use cases + risk assessment |
| **Operations** | provisioning, billing, internal tools | scale + rollout logistics |
| **Finance** | pricing, unit economics, forecast | business case + financial assumptions |

## Ready-to-use template — delivery plan

```markdown
# Delivery plan — [Initiative] — [date]

**Status:** Planning | In flight | Launching | Post-launch
**PM:** @name
**Links:** PRD / tracking plan / RAID / launch plan

## Bet recap
One sentence.

## Cross-functional roles (RACI-lite)
| Workstream | Lead | Key deliverable | By when | Status |
|---|---|---|---|---|
| Engineering | @eng-lead | working feature behind flag | W6 | on track |
| Design | @designer | final UX + accessibility | W3 | done |
| Analytics | @analyst | tracking plan QA | W4 | at risk |
| PMM | @pmm | launch messaging + FAQ | W5 | on track |
| Sales enablement | @sales-ops | demo deck + objection handling | W6 | not started |
| CS/Support | @cs-lead | KB articles + support playbook | W6 | not started |
| Legal | @legal | data/privacy review | W3 | in progress |
| Ops | @ops-lead | provisioning + billing | W5 | on track |

## Sequence (Gantt-lite or week-by-week)
- W1: discovery sign-off, design kickoff, legal intake
- W2: design v1 review, eng spike, analytics schema draft
- W3: design v2, legal sign-off, eng implementation begins
- W4: analytics plan QA, PMM messaging draft, internal demo
- W5: eng code-complete (flagged), support playbook, beta invitees
- W6: GA readiness review, sales enablement, launch

## Decision forums
- weekly sync (30 min) — all leads — RAID review + decisions
- async updates (per workstream) — by EOD Tuesday in Slack #init-X

## Handoffs
| From | To | Artefact | When |
|---|---|---|---|
| Design | Eng | final Figma + spec | W3 |
| PM | Analytics | tracking plan | W2 |
| Eng | Support | pre-launch walkthrough | W5 |
| PMM | Sales | enablement kit | W6 |

## Communications
- internal: weekly update in [channel] every Friday
- external: beta customers get invite W5; public launch W6
- exec: monthly status in review deck
```

## Orchestration discipline

### 1. Clarify who owns the "how", not just the "what"

PMs often fall into the trap of telling each function how to do their job. Don't. Engineering owns how to implement; design owns how to design; support owns how to support. PM owns: the *why*, the *outcome*, and the *coherence* across workstreams.

### 2. Shared visibility > status meetings

One living doc (delivery plan above) that everyone reads weekly beats 5 status meetings. Meetings are for friction — when something needs to change, not for reading out what's on track.

### 3. Explicit handoffs

The moment when Design hands off to Eng, or Eng hands off to Support, is where balls get dropped. Name them. Put them on the plan. Make the handoff artefact explicit ("the handoff is 'Figma file + spec + state coverage'").

### 4. Parallel-but-aware workstreams

Sales enablement can start as soon as the bet is approved, not wait for code-complete. PMM messaging can be drafted from the PRD, refined as design lands, finalised at beta. Don't gate the whole plan on the slowest function; just make sure each function starts with enough context.

### 5. Pre-launch readiness review

One meeting before GA. All leads say "my workstream is ready / has these open items". Open items have owners + dates. No "we'll figure it out".

## Common anti-patterns

- **PM as bottleneck.** Every decision routes through the PM; the team stalls when PM is OOO.
- **Heroics.** Late nights and weekend sprints to cover for bad coordination. Burns people.
- **Meeting bloat.** 4 status meetings per week, each 45 minutes, 8 attendees. That's a lot of expensive attention.
- **Late GTM.** Involving PMM/Sales/Support in week 5 of a 6-week sprint. Launch lands without context.
- **Escalation without options.** PM surfacing a blocker upward without having attempted resolution.
- **Ambiguous ownership.** "Analytics will handle tracking" — who specifically, what exactly, by when?
- **No handoff artefacts.** Eng thinks Design finished; Design thinks Eng is still waiting.

## Escalation — clean protocol

See `dependency-risk.md` for the 5-step escalation format: situation + attempts + options + recommendation + ask + date.

## Seniority signals

- **Beginner:** coordinates local workstreams.
- **Intermediate:** keeps one triad (PM/design/eng) + adjacent functions aligned.
- **Advanced:** runs complex cross-team delivery with minimal confusion; handoffs are clean.
- **Expert:** designs cross-functional mechanisms (templates, rituals, tooling) that improve execution quality at scale.

## Files

`.ai/memory/projects/<slug>/delivery-plans/<initiative>.md`. Link from PRD + RAID + launch plan.
