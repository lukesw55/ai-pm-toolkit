# Release notes — user-facing + internal + customer

## What it is

Release communications that are **fit for audience**:

- **User-facing changelog** — what's new, why users should care, where to find it
- **Internal enablement one-pager** — for sales, CS, support to speak to customers confidently
- **Customer email / in-app notice** — timely, friendly, actionable
- **Migration notice** (if applicable) — for breaking changes or behaviour changes

## Why it matters

Release notes are the product's written face after each ship. Done well, they drive adoption, reduce support tickets, and build trust. Done badly (or skipped), users discover features accidentally and sales teams learn from customers.

## Audience matrix

| Audience | Artefact | Where it lives | Tone | Length |
|---|---|---|---|---|
| End users | Public changelog | /changelog, in-app, email | friendly, benefit-led | 50-150 words per item |
| Admins (B2B) | Release digest | email, Confluence external | informative, migration-aware | 100-300 words |
| Developers (API consumers) | Developer changelog | dev docs | precise, versioned, migration steps | full technical detail |
| Sales + CS + Support | Internal enablement | Confluence internal, Slack | pitch-ready, objection-handling | 1 page |
| Executives | Digest in monthly report | report deck | outcome-led, adoption signals | 2-3 bullets |

One ship = multiple artefacts, each tailored. Don't copy the eng PR description into the user changelog.

## Ready-to-use template — User-facing changelog entry

```markdown
## [YYYY-MM-DD] — [Feature name]

**One-liner:** [benefit in user language, max 15 words]

**What it does:** [2-3 sentences — what the user can now do that they couldn't before, and the main benefit. No eng jargon.]

**Who it's for:** [segment or role, if scoped]

**How to use it:** [2-3 sentences or numbered steps — action-oriented]

**Availability:** [all plans / Pro+ / Enterprise / API-only / rollout %]

**[Optional] Migration note:** [if any behaviour changes affect existing users]

**Learn more:** [link to help-centre / docs / blog]
```

## Ready-to-use template — Internal enablement one-pager

```markdown
# Enablement — [Feature] — [YYYY-MM-DD]

**Audience:** Sales / CS / Support
**PM:** @name   **PMM:** @name
**Links:** PRD / launch plan / public changelog

## What shipped (30 seconds)
- feature / capability:
- segment it helps:
- benefit:

## Why it matters (60 seconds)
- user problem it solves:
- what was previously painful:
- what outcome now becomes possible:

## Who to pitch it to
- primary ICP:
- secondary:
- DO NOT pitch to:
- good expansion trigger:

## Talking points (ready to use in a call)
- opener: "[one sentence]"
- the "aha" demo moment:
- the proof point:
- pricing/packaging note:

## Pitfalls + objection handling
| Objection / concern | Response |
|---|---|
| "Does it integrate with X?" | [current answer + roadmap if any] |
| "Is it secure / compliant?" | [short answer + link to docs] |
| "How does this compare to [competitor]?" | [sharp differentiator, 2 sentences] |
| "What happens to our current setup?" | [migration implication + link] |

## Demo flow (if applicable)
1. [step]
2. [step]
3. [step — payoff]

## Support scenarios + how to handle
- common question → expected answer or escalation path
- known limitations → how to frame with customer
- edge cases → ticket-triage criteria

## Where to find more
- public changelog: [link]
- help-centre: [link]
- internal wiki / demo env: [link]
- PM / PMM contact for questions:
```

## Ready-to-use template — Customer email (beta or GA)

```markdown
Subject: [Benefit-led, not feature-led — e.g. "Your dashboards just got faster"]

Hi [First name / Team],

[One sentence: what's new + why they'll care]

**What you can do now:**
- [benefit 1]
- [benefit 2]
- [benefit 3]

**How to get started:**
[1-2 sentences or a clear CTA button — "Open the dashboard" / "Try it now"]

[If relevant:] Already using [related feature]? [One line about how it integrates / replaces / extends]

[If migration:] **What's changing for you:** [specific + link to full migration guide]

Questions? Reply to this email or reach out to [CS contact] — we'd love to hear what you build with this.

[Sign-off, real name, team]

P.S. [Optional: a "nice to know" detail or a customer quote]
```

## Ready-to-use template — Developer changelog entry

```markdown
## v[X.Y.Z] — [YYYY-MM-DD]

### Added
- `POST /v1/foo` endpoint — [one-liner + docs link]
- New property `bar` on `/v1/baz` response

### Changed
- `GET /v1/foo` now returns pagination metadata (`pagination` object)
  - **migration:** no breaking change for existing consumers; new field optional

### Deprecated
- `POST /v1/old-endpoint` — use `/v1/new-endpoint` instead
  - **sunset:** YYYY-MM-DD
  - **migration guide:** [link]

### Removed
- [nothing / list]

### Fixed
- Rate-limit headers now include `X-RateLimit-Reset` (was missing for some routes)

### Security
- [details or "no security-relevant changes"]

### Full diff + migration guide
[link]
```

## Writing principles

- **Lead with benefit, not feature.** "Export reports to CSV" → "Share report data with teammates outside the product".
- **User language, not internal.** No project codenames, no service names, no eng jargon.
- **Specific, not grand.** "Faster" means nothing. "Dashboards load in under 1s for teams up to 500 users" means something.
- **What's different for the user?** Every release note answers this.
- **Migration upfront.** If behaviour changes, the user learns it before they hit it.
- **Link to depth.** Keep the note concise; link to docs / blog for detail.
- **Dates + availability.** "Rolling out to all users over the next week" beats silence.

## Common anti-patterns

- **PR-description dumping.** Copying eng merge messages into a user-facing changelog.
- **Marketing hype.** "Revolutionary AI-powered experience" with no benefit.
- **"Improvements and bug fixes."** Fine when true; misleading when a material change hides inside.
- **No enablement.** Public changelog exists, internal teams learn from customers.
- **No migration notice.** Breaking change ships silently; tickets surge.
- **No audience tailoring.** Same copy for end users, admins, and devs.
- **Unlinked release notes.** No way to go deeper; no way to see history.

## Cadence + tooling

- **Per-ship release note** (for user-visible features) — drafted in the PRD, finalised before GA.
- **Monthly or quarterly digest** — for customers who don't watch the per-ship changelog.
- **Versioned changelog for APIs** — immutable log; no retroactive edits.
- **Confluence / docs site** — public changelog lives here; internal enablement in internal space.

## Seniority signals

- **Beginner:** writes accurate feature notes.
- **Intermediate:** tailors release notes per audience + produces enablement material.
- **Advanced:** orchestrates release comms across all channels with consistent voice + strong benefit framing; adoption lifts post-release.
- **Expert:** builds release-notes systems (templates, style guide, cadence, tooling) that other teams adopt.

## Files

- Public changelog: Confluence external / docs site (content drafted in `.ai/memory/projects/<slug>/release-notes/<version>.md`)
- Internal enablement: Confluence internal (drafted alongside)
- Customer emails: linked in launch plan
- All linked bidirectionally with the PRD and launch plan
