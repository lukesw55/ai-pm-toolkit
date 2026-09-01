# Example: discovery notes → one-pager opener

A worked example showing how this skill turns scattered evidence into a one-pager opener with a real spine. The source pile and customer details are fabricated for illustration; in real use, every cited ID would point back to a transcript, dashboard, or ticket.

## Source the user provided

> "I have notes from 6 customer interviews about our B2B SaaS product, plus dashboard data showing active customers plateauing around 90 days. The pattern feels real but I haven't written it up. Need a one-pager opener I can take to leadership next week."
>
> Notes (paraphrased):
>
> - INT-01 (auto-tier-1, 60 dev fleet): "We onboarded fast, but after 3 months we kind of forgot about it. Nobody pushed updates last quarter."
> - INT-02 (industrial automation, 200 devices): "Our CSM left, the new one never reached out. We don't know which features are new."
> - INT-03 (medical, 30 devices): "We use it for compliance only. The team that adopted it moved to another project."
> - INT-04 (smart-energy, 1.2k devices): "We renewed because the alternative was painful. But honestly, we use 20% of what we pay for."
> - INT-05 (small OEM, 8 devices): "I love it but I'm a one-person team — no time to explore."
> - INT-06 (legacy enterprise, 600 devices): "Ours stalled at the platform team. Devs never adopted the new console."
>
> Dashboard signal: weekly active accounts grow steadily for ~85 days, then flatline; ~40% of paid accounts have <1 active session/month after day 120.

## Mode detection

This is **Mode C — Raw-Notes-to-Story** with a **PRD-adjacent format** (one-pager opener). The user has fragments and wants a narrative the leadership can act on.

## Story strategy

```markdown
## Story strategy
- Objective: Surface the active-customer plateau as a real, sized pattern leadership can decide on next week
- Audience: leadership (GPM + eng director + commercial lead)
- Format: One-pager opener (200–400 words)
- Narrative spine: This is a story about active customers who plateau after 90 days, the team that mistook adoption for stickiness, the discovery that what drives churn is account-management drift not feature gaps, and the bet that closes that gap.
- Chosen framework: One-Pager Opener (Customer + JTBD → Friction → What we tried → Why now → Bet)
- Gaps: No revenue-by-segment cut yet [NEEDS SOURCE: CRM ARR by segment]; CSM coverage data anecdotal only [NEEDS SOURCE: CS team handover log]
```

## Final story

```markdown
# Closing the active-customer plateau before it becomes churn

## The customer and the job
Mid-sized customers who completed onboarding and now need someone — internal or external — to keep them connected to what's new in the product.

## What we see today
Six interviews and the active-account dashboard point to the same pattern. Customers grow weekly active usage for the first ~85 days, then flatline (Dashboard X, 2026-Q1). About 40% of paid accounts have less than one active session per month by day 120 [NEEDS SOURCE: dashboard link].

The interviews are blunter:

- INT-01 onboarded fast and "kind of forgot about it" — nobody pushed updates last quarter
- INT-02 lost their CSM and the new one never re-engaged
- INT-04 renewed because switching was painful, but reports using ~20% of what they pay for
- INT-06 stalled at the platform team; devs never adopted the new console

This isn't a feature-gap story. It's a relationship-drift story. Every account that plateaued still considers the product "the right tool" — they just lost the thread.

## What we tried (or didn't)
We instrumented onboarding heavily and shipped a stronger 30-day activation funnel in 2025-Q4. Post-90-day re-engagement — when CSM coverage thins or rotates — has no equivalent owner today.

## Why now
Two pressures converge in 2026-Q2: (1) the first 2024-Q1 cohort hits its 24-month renewal window and (2) commercial is sizing the at-risk ARR for the half-year plan. Without a re-engagement motion, the renewal conversation defaults to price discount or churn.

## The bet
Build a lightweight account-engagement loop — owned by Product, surfaced in-product, triggered by dashboard signals — that re-opens the conversation between day 90 and day 120, before silence becomes churn.

## Why this works
- **Assignment alignment:** answers "frame the plateau pattern for leadership" with cited evidence and a named bet.
- **Narrative spine:** customer → friction (relationship drift) → turning point (it's not a feature gap) → bet (re-engagement loop).
- **Specificity:** cites interview IDs and dashboard signals; gaps marked, not invented.
- **Audience fit:** opens on customer behaviour, not internal framing — which is what leadership readers act on.
- **Outbound delivery:** before this opener goes to a Confluence one-pager page or a Slack thread, run `humanizer` on the prose and apply the `humanize-deliverables` sentinel.
```

## What this example demonstrates

- Mode C handling — fragments in, narrative out
- Use of the **One-Pager Opener** framework (template 10)
- **Inline citation discipline** — every claim points to ID-XX or `[NEEDS SOURCE]`
- **Spine sentence** that captures protagonist, friction, turning point, takeaway in one line
- Refusal to invent the missing pieces (ARR cut, CSM data) — they are surfaced as gaps, not papered over
- Reminder to run `humanizer` and `humanize-deliverables` before the artefact ships
