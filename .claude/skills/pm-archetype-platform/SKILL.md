---
name: pm-archetype-platform
description: >-
  Platform / API / infrastructure PM archetype lens. Invoke when the product is
  something other products are built on — internal platforms, public APIs,
  SDKs, CLI tools, partner integrations, infrastructure primitives. Users are
  usually developers (internal teams, external customers, partners) or
  downstream product teams. Optimises for leverage, reliability, adoption,
  abstraction quality, developer experience, and migration discipline — not
  end-user delight. Trigger on "API contract", "deprecation policy", "breaking
  change", "como deprecar X?", "quem consome esse endpoint?" — full
  trigger-phrase list in the skill body. Applies most strongly to the public
  API gateway, device SDKs, and shared libraries that many services depend on.
---

# PM Archetype — Platform / API / infrastructure products

> Product-type lens. Pairs with phase skills when the product's users are developers, partners, or downstream product teams — not end-users. The phase skills cover *when* and *how to sequence*; this skill covers *what's special about platforms* (long tails, leverage, deprecation as PM work).

## Prime directive

**Abstractions that compound.** Build primitives downstream teams choose willingly because they're better than rolling their own. Avoid one-off bespoke requests that pollute the platform.

## When to invoke

The product or feature is consumed by code, not clicked by an end-user:

- public API or SDK consumed by external customers / partners
- internal API consumed by other product teams
- shared library / framework / primitive (e.g. a shared messaging/event library or a common auth client)
- CLI / DevTools / build infrastructure
- platform capability that other features depend on (auth, identity, storage, telemetry)

This archetype most often applies to the public API gateway, the device-side SDKs, the shared messaging/event library, and identity-provider extensions that other services depend on.

### Trigger phrases

Any of these in a request points here: "platform", "API contract", "SDK", "CLI", "partner integration", "developer experience", "DevEx", "DX", "migration plan", "deprecation", "deprecation policy", "backwards compatibility", "breaking change", "versioning", "SLO", "SLA", "p95 latency", "error rate", "adoption rate", "consumer team", "downstream team", "infrastructure primitive", "reusable abstraction", "internal tool", "tool for engineers", "essa API ainda é usada?", "como deprecar X?", "quem consome esse endpoint?".

## Required reading before output

- `.ai/rules.md`, `.ai/app.md`, `.ai/memory/active-context.md`
- relevant project memory — **prior contracts and ADRs are load-bearing**; platforms accumulate decisions that constrain future work

## References this skill chains to

- `.claude/skills/pm-phase-discover/` — especially `jtbd-segmentation.md` adapted to developer personas
- `.claude/skills/pm-phase-define/references/kpi-tree.md` — platform-specific metrics (adoption rate, migration velocity, API error rate, p95 latency, DevEx NPS)
- `.claude/skills/pm-phase-develop/references/technical-fluency.md` — essential for platform PMs
- `.claude/skills/pm-phase-develop/references/prd-writing.md` — platform PRDs emphasise contracts + NFRs
- `.claude/skills/pm-phase-deliver/references/metric-quality-guardrails.md` — reliability + migration guardrails
- `.claude/skills/pm-transversal-stakeholder/` — consumer teams are critical stakeholders
- your engineering architecture partner — for service topology + signed-update trust-chain implications
- a service-inventory pass — to audit which downstream services consume the platform piece you're touching

## Platform-specific metrics

- **Adoption** — % of eligible consumer teams / apps / customers using this capability
- **Migration velocity** — when a new version / pattern is released, how fast do consumers migrate?
- **Deprecation discipline** — how long do deprecated capabilities linger? What's the tax?
- **Reliability** — p50 / p95 / p99 latency, error rate, availability SLO, incident count
- **Developer experience** — time-to-first-success for new consumers, docs quality, support volume
- **Abstraction quality** — are consumers building *with* the platform or *around* it?

## Workflow

1. **Identify the consumer persona** — which downstream team / developer / customer archetype?
2. **Describe the JTBD in platform terms** — "consumer wants to [accomplish X] without [building plumbing Y]"
3. **Define the contract** — API shape, data model, CLI signature, SDK surface (see `prd-writing.md` and `technical-fluency.md`)
4. **Name NFRs explicitly** — latency, availability, backwards-compat commitment, deprecation policy
5. **Design the adoption path** — how will consumers discover + adopt + stay up-to-date?
6. **Plan migrations + deprecations** — platform work has long tails; deprecations are PM work
7. **Architecture check** — loop in your engineering architecture partner for trade-offs and run a service-inventory pass to audit current consumers
8. **Failure-mode analysis** — loop in your QA lead (platforms fail in novel ways: contract drift, partial migration, version skew)
9. **Update memory** — durable platform decisions belong in ADRs (see `pm-phase-define/references/decision-memo-daci.md`)

## Platform-specific anti-patterns

- **One-off feature requests into the platform.** A consumer asks for a specific thing; shipping it sets a precedent that distorts the API.
- **Optimising for technical elegance without adoption.** A beautiful API nobody uses.
- **No deprecation policy.** Old things live forever; the platform accretes complexity.
- **Hidden breaking changes.** A version bump that subtly changes behaviour → consumers don't migrate → you're stuck supporting both forever.
- **Under-investing in docs.** Great platforms with bad docs fail in the market.
- **No migration plan.** Shipping v2 without helping consumers leave v1 = you maintain two things forever.
- **No version skew handling.** New server, old client — and no graceful failure path.

## Output format

```text
## pm-archetype-platform recommendation

### Consumer persona + JTBD
...

### Contract (API / data / CLI / SDK)
shape + types + error model + idempotency / pagination / pagination cursor

### NFRs + SLOs
latency, availability, error budget, backwards-compat commitment

### Adoption + migration plan
discovery, onboarding, upgrade path, who notifies whom

### Deprecation policy (for what this replaces, if any)
sunset window + migration tooling + comms cadence

### Reliability guardrails
SLO breach detection, paging, rollback path

### Open questions for the architect
explicit hand-off list before implementation

### Memory updates
```

## Integration

- Upstream: `pm-phase-discover` (developer JTBDs), `pm-phase-define` (platform KPI tree, deprecation doctrine, ADRs).
- Build phase: `pm-phase-develop` (PRD with explicit contract + NFRs + version policy).
- Launch phase: `pm-phase-deliver` (staged rollout, version-skew monitoring, adoption metrics).
- Transversals: `pm-transversal-stakeholder` (consumer teams as a first-class stakeholder group), `pm-transversal-docs` (developer docs, OpenAPI specs, changelog discipline).
- Engineering pairings: your engineering architecture partner (cross-service blast radius), your backend tech lead (per-service idioms), your QA lead (contract tests, version-skew probes).
- Inventory: run a service-inventory pass to map current consumers before changing a contract.
- Copilot mirror: [.github/agents/pm-platform.agent.md](../../../.github/agents/pm-platform.agent.md).

## Success criteria

- consumers adopt willingly; no mandates required
- migration tax decreases over time
- deprecations actually close
- reliability SLOs held or improved
- new consumer teams reach first success quickly
