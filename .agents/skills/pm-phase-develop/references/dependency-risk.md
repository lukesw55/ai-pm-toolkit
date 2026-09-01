# Dependency and risk management

## What it is

Identifying, sequencing, and actively managing **cross-team dependencies, delivery risks, and assumption risks** before they become schedule or quality problems.

## Why it matters

Experienced PMs are expected to **surface and reduce coordination failure** — not discover it at launch week. Dependencies are where plans go to die silently.

## RAID log — the standard artefact

**R**isks, **A**ssumptions, **I**ssues, **D**ependencies, all in one living document. Reviewed weekly by the delivery lead + PM.

## Ready-to-use template — RAID log

```markdown
# RAID — [Initiative / epic] — updated [date]

## Dependencies
| # | Item | Owner | Needed by | Status | Mitigation if slipped | Escalation path |
|---|---|---|---|---|---|---|
| D1 | SSO changes in platform team | @platform-lead | 2026-05-01 | on track | alt: skip SSO for v1, support email | @eng-director |
| D2 | Legal review of new data retention | @legal | 2026-04-20 | at risk | smaller data scope reduces review |@legal-director |

## Risks
| # | Risk | Likelihood (L/M/H) | Impact (L/M/H) | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Analytics team doesn't finish tracking plan by sprint start | M | H | PM drafts schema; eng co-implements; validate week 1 | @pm |
| R2 | Pricing change blocks packaging decision | L | M | pre-align pricing lead; DACI by end of week | @pm |

## Assumptions (unvalidated beliefs)
| # | Assumption | Invalidation trigger | Owner | Check by |
|---|---|---|---|---|
| A1 | 40% of users will opt in to new flow | <25% after 2 weeks on 10% cohort | @pm | week 3 |
| A2 | API latency stays <500ms at 10x load | load test shows >800ms | @eng | week 2 |

## Issues (realised problems — not risks anymore)
| # | Issue | Opened | Owner | Target resolution | Status |
|---|---|---|---|---|---|
| I1 | Design review delayed due to sick leave | 2026-04-15 | @design-lead | 2026-04-22 | in progress |

## Change log
- [date] [change summary]
```

## Dependency map — visualising it

Not every initiative needs a visual map, but multi-team programs benefit:

```
[My team initiative]
    |
    |-- depends on --> [Platform team: SSO enhancement] — needed by W4
    |-- depends on --> [Analytics team: tracking schema] — needed by W2
    |-- depends on --> [Legal: data retention policy review] — needed by W3
    |-- depends on --> [Design system: new component] — needed by W1
    |                              
    |-- blocks -------> [Marketing: launch page] — needs by W6
    |-- blocks -------> [Support: KB articles] — needs by W5
```

Tools: Miro/Mermaid/Confluence diagram. Keep it updated.

## Dependency discipline — the drill

For each dependency, answer:

1. **What exactly is being delivered?** "SSO support" is not specific enough. "Accept SAML assertions from our IDP and create a session cookie" is.
2. **Who owns delivery?** Named person, not a team.
3. **When is it needed?** Specific date, not "early May".
4. **What happens if it slips?** Plan B must exist at definition time.
5. **How will the dependency team know they're blocking us?** Shared visibility, not silent hope.

## Risk classification

Score risks by likelihood × impact:

|               | Impact: Low | Impact: Medium | Impact: High |
|---|---|---|---|
| **Likelihood: High** | monitor | mitigate | **mitigate urgently** |
| **Likelihood: Medium** | accept | mitigate | mitigate |
| **Likelihood: Low** | accept | monitor | mitigate |

For High × High: the plan must change. For others: mitigation is enough.

## Assumption risk — the hidden category

Assumptions are silent risks. They feel like facts until they fail.

Common load-bearing assumptions:
- users will adopt the new flow
- our latency budget holds at 10x traffic
- the legal review will approve without redesign
- the partner API behaves as documented
- our cohort analysis represents the population

**Rule:** the top 3 load-bearing assumptions must be named and have an invalidation check scheduled *before* launch week.

## Escalation — when and how

Escalate when:
- a dependency will slip past its needed-by date
- a risk has become an issue
- an assumption has just failed
- you need a decision above your authority to unblock

How to escalate cleanly:
1. State the situation in 2 sentences.
2. State what you've already tried.
3. Propose 2 options (not "please help").
4. State your recommendation.
5. State the specific ask + decision date.

Don't escalate without options. That's status, not escalation.

## Common anti-patterns

- **Hidden dependencies.** The team discovers at sprint 3 that they need approval from legal. At sprint 3.
- **No owner.** "The platform team will deliver SSO" — who specifically?
- **Optimism bias.** Everything is "on track" until the week before launch.
- **Late escalation.** Raising blockers when it's already too late to reroute.
- **Conflating likelihood and impact.** Treating a high-impact low-likelihood risk the same as a low-impact high-likelihood one.
- **RAID as theatre.** Updated once, never reviewed.

## Cadence

- **Weekly RAID review** — PM + delivery lead + tech lead. 15 min. Go item-by-item.
- **Sprint review of at-risk items** — escalate if not moving.
- **Pre-launch RAID sweep** — no open reds at launch.

## Seniority signals

- **Beginner:** tracks obvious blockers in tickets.
- **Intermediate:** maintains a usable risk + dependency view for one team.
- **Advanced:** anticipates multi-team failure points and gets ahead of them.
- **Expert:** builds operating mechanisms that make dependencies visible early org-wide.

## Files

`.ai/memory/projects/<slug>/raid.md` — single source of truth per initiative. Link from PRD and roadmap.
