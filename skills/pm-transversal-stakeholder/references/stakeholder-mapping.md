# Stakeholder mapping

## What it is

For a given initiative or decision: **who are the stakeholders, what do they need, what do they fear, and how should you engage them?** Done well, it's a 1-page artefact that prevents 90% of stakeholder surprises.

## Why it matters

"Stakeholder management" as an undifferentiated activity is a soft skill. Stakeholder mapping as a **specific artefact produced per initiative** is a hard skill — and a massive time-saver.

## Influence × Interest matrix

The standard 2×2 frame. For each stakeholder, plot:

|              | **Low interest** | **High interest** |
|---|---|---|
| **High influence** | **Keep satisfied** — inform at milestones; don't drown in detail | **Manage closely** — active engagement; they'll shape outcome |
| **Low influence** | **Monitor** — broadcast communication is enough | **Keep informed** — detailed updates; they care and talk to others |

This is a starting frame, not the final answer. Real stakeholder work is about understanding each person's specific lens.

## Ready-to-use template — Stakeholder map

```markdown
# Stakeholder map — [Initiative] — [YYYY-MM-DD]

**PM:** @name
**Links:** PRD / DACI / strategy memo

## Initiative summary
One sentence.

## Stakeholders
| Name / role | Function | Influence (L/M/H) | Interest (L/M/H) | What they want | What they fear | Engagement plan |
|---|---|---|---|---|---|---|
| @exec-1 (VP Product) | Leadership | H | H | metric movement + strategic coherence | losing focus to new bets | weekly memo + monthly review; decision ask for budget |
| @eng-dir | Eng Leadership | H | M | feasibility + team load | scope creep | DACI contributor; kickoff attendance |
| @pmm-lead | Marketing | M | H | positioning + launch readiness | late enablement | weekly sync + review messaging W-3 |
| @legal | Compliance | L | H | privacy + ToS | surprise data usage | intake W-1; review W-2 |
| @sales-lead | Revenue | M | M | customer pipeline impact | deals blocked by incomplete feature | beta customer list + enablement W-5 |
| @support-lead | Support | L | H | readiness + KB | ticket spike | playbook W-4 |
| @partner-customer-X | External | L | M | beta access + migration help | breaking change disrupting their ops | opt-in beta + account-manager touch |

## Groupings
- **Manage closely:** @exec-1, @eng-dir (H × H — named stakeholder syncs)
- **Keep informed:** @pmm-lead, @support-lead, @sales-lead (high interest — detailed channel)
- **Keep satisfied:** [names] (high influence, low interest — exception-based)
- **Monitor:** [names] (broadcast only)

## Risks
- @exec-1 expected early wins by Q2 → need to reset timeline expectations before kickoff
- @legal intake pipeline is congested → start the request now, not W-1

## Engagement cadence
- weekly 1:1 with @exec-1 (15 min)
- async weekly update to "keep informed" list
- bi-weekly sync with PMM + Sales for launch prep
- monthly portfolio review

## Red-flag signals (early warning)
- @exec-1 starts asking other PMs for input on this → they're unsure about us
- Sales stops mentioning this in pipeline calls → enablement stale
- Support ticket volume ticks up on unrelated features → team attention drifting
```

## Engagement plan — what to do with each group

### Manage closely (H influence, H interest)
- named sync cadence (weekly or bi-weekly)
- first to know about changes
- asked for input before it's final
- receive tailored memos (not the same as everyone)

### Keep informed (L influence, H interest)
- detailed regular updates (weekly digest)
- invited to demos and reviews
- easy way to ask questions (Slack channel, office hours)
- they often talk to others, so consistent messaging matters

### Keep satisfied (H influence, L interest)
- exception-based communication
- milestone updates only
- concise: 1-2 sentences when something matters
- never surprise them — preview before wider comms

### Monitor (L influence, L interest)
- broadcast channels only (team Slack, all-hands)
- no dedicated effort
- listen for if/when their interest or influence shifts

## Dissent protocol

When a stakeholder disagrees with the recommendation:

1. **Understand first.** Ask why; listen; restate their position. Often disagreement = missed context, not bad faith.
2. **Capture on the DACI page.** "@contributor-X disagrees because [reason]. Driver considered and: [addressed / accepted with rationale / escalating]."
3. **Decide on the record.** Either adjust the recommendation, or state that you considered and proceeding anyway, or escalate.
4. **Don't hide dissent.** Hidden disagreement becomes ambushes in exec meetings.

## Anti-patterns

- **Inviting everyone.** 14 people in the sync → nobody owns. Pick a small consult set; broadcast to the rest.
- **"We already talked about it."** No written record → re-argued in 2 weeks.
- **Status-sharing as alignment.** Sending a weekly update ≠ getting alignment on decisions.
- **Missing the "fears" column.** You know what they want; you don't know what makes them anxious → blindsided.
- **Static map.** Written once, never updated as stakes shift.
- **Engagement asymmetry.** Spending 80% of stakeholder time on the one most visible exec, ignoring the legal team that will block launch if ignored.

## When to refresh

- at project kickoff
- when a new function gets pulled in
- when influence or interest clearly shifts (an exec hands off to a new one, a team reorg, a market change)
- at quarterly planning
- before any major decision

## Files

`.ai/memory/projects/<slug>/stakeholders.md`. Linked from the PRD and DACI pages. Kept current; stale maps are dangerous.
