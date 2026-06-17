# Technical fluency (PM lens)

## What it is

Understanding enough of **architecture, APIs, data flows, constraints, observability, and feasibility** to make sound product trade-offs *with* engineering — not out-engineer them.

## Why it matters

Experienced software PMs do not need to write production code, but they must **reason credibly about technical shape and cost**. The best PM trade-off conversations happen between engineers and PMs who speak the same domain well enough to challenge each other.

## What a software PM should be able to do

- read a system architecture diagram and ask informed questions about data flow, latency, and reliability
- discuss API contracts (REST endpoints, GraphQL queries, webhooks, rate limits) and their trade-offs for consumers
- reason about data models — entities, relationships, source-of-truth, mutations — at a product level
- discuss non-functional requirements (NFRs): latency, throughput, availability (SLOs), durability, security, privacy
- evaluate a proposed technical approach for **reversibility, coupling, migration cost, and observability**
- understand feature flags, rollout strategies, and kill switches
- know what a database migration, a breaking API change, or a schema evolution costs
- read a sequence diagram or a dependency graph
- interpret an incident timeline or a postmortem
- ask useful questions about AI/ML systems: training data, evals, drift, inference cost, failure modes (for AI PMs — load the `pm-archetype-ai` skill; the Copilot equivalent is `.github/agents/pm-ai.agent.md`)

## What a software PM does NOT need to do

- write production code
- design algorithms
- own system architecture decisions (that's the tech lead / architect)
- decide on frameworks, languages, or tooling
- optimise queries or debug production incidents

The line is: **understand enough to make informed product trade-offs; don't usurp the eng role.**

## Ready-to-use template — technical trade-off memo

```markdown
# Technical trade-off memo — [topic] — [date]

**Status:** Options | **Recommendation** | Decided
**PM:** @name  **Tech lead:** @name
**Linked:** PRD / ADR / RAID

## Context
Product problem or capability gap prompting this trade-off. 3–5 sentences.

## Constraints
- must-haves (latency, reliability, security, compliance, cost):
- budget:
- timeline:
- existing systems to integrate with:

## Options

### Option A — [short name]
- approach (2–3 sentences):
- effort: [person-weeks]
- reversibility: [low / medium / high]
- ongoing cost: [$ or engineer-hours/month]
- affects: [which services / APIs / consumers]
- pros (for product outcomes):
- cons (for product outcomes):
- technical concerns (from eng):

### Option B — [short name]
- ...

### Option C — [short name]
- ...

## Recommendation
Option [X]. Optimises for [speed/quality/reversibility/cost]. Accepts [trade-off].

## NFRs this affects
- latency: [current → proposed]
- availability: [current → proposed]
- security / privacy implications:
- observability (can we monitor it?):

## Migration cost
- users affected:
- data migration required:
- API consumers affected (internal / external):
- rollback plan:
- deprecation timeline:

## Open questions for eng
- ...
```

## Ready-to-use template — API proposal (from PM side)

When PM is shaping an external API's product contract:

```markdown
# API proposal — [capability] — [date]

## Consumer story
As a [developer integrating with our API], I want to [do X], so that [outcome].

## Use cases (ranked)
1. Primary use case
2. Secondary
3. Edge

## Proposed surface
- endpoint / method / query / mutation:
- request params:
- response shape:
- error modes:
- auth model:
- rate limiting:

## Evolution considerations
- versioning strategy (v1 / v2 / evolution):
- deprecation policy:
- backwards compatibility commitments:

## Developer experience
- docs plan:
- examples / SDKs:
- sandbox / test environment:
- debugging tools / request IDs:

## Non-functional
- latency target (p50, p95, p99):
- availability (SLO):
- pagination for large responses:

## Security + compliance
- auth / authz model:
- PII / regional data handling:
- audit logging:
```

## Key concepts cheat-sheet (for PMs who want sharper vocabulary)

- **SLA / SLO / SLI** — agreements (SLA, contractual), objectives (SLO, internal target), indicators (SLI, actual measurement). Know the difference; don't confuse.
- **p50 / p95 / p99** — latency at 50th, 95th, 99th percentile. p99 matters for tail users; averages hide them.
- **Idempotency** — a request that can be retried without changing the result beyond the first successful call. Matters for payments, signups, external integrations.
- **Eventual consistency** — data propagates asynchronously; reads may lag writes. Common in distributed systems. User-facing implications: "I just did X but it's not showing yet."
- **Rate limiting** — requests allowed per time window. Design considers: per-user? per-API-key? per-endpoint? How do consumers handle 429?
- **Feature flag** — runtime switch to enable/disable code paths. Used for rollouts, A/B, kill switches.
- **Canary release** — rollout to a small % first, then expand. Catches issues before full blast.
- **Blue/green deployment** — two production environments; switch traffic between them. Zero-downtime deploys.
- **Migration** — moving data, schema, or users from system A to system B. Usually more expensive than the build.
- **Circuit breaker** — automatic stop when a dependency fails repeatedly. Prevents cascading failures.

## Common anti-patterns

- **Cargo-cult jargon.** Using "microservices" and "event-driven" without understanding what they cost.
- **Promising incoherent solutions.** Committing to an outcome the architecture can't cheaply produce.
- **Ignoring NFRs.** "Ship it fast" — but it can't hold the traffic or meet privacy requirements.
- **Over-relying on eng to translate.** Every technical implication hits the PM's inbox; PM should be able to reason about most without a lookup.
- **Under-relying on eng.** Making technical design decisions without the tech lead.
- **Dismissing migration cost.** "Just migrate it" → 6-month project surfaces.
- **Skipping observability.** Shipping without metrics/logs to monitor = shipping blind.

## How to get more fluent

- attend architecture review meetings and ask questions
- read postmortems (incident writeups) in your product area
- read the API docs of at least one competitor and one adjacent platform
- pair with an engineer on a design review; ask "why" a lot
- learn to read system diagrams (sequence, deployment, data-flow)
- spend 30 min monthly browsing your product's observability dashboards

## Seniority signals

- **Beginner:** understands the basic architecture of the area.
- **Intermediate:** discusses trade-offs fluently with technical partners.
- **Advanced:** shapes product choices based on reasonable technical understanding; catches feasibility issues early.
- **Expert:** bridges technical and customer value in complex platform or infra contexts; respected by senior engineers as a product-thinking peer.

## Files

Technical trade-off memos → `.ai/memory/projects/<slug>/tech/<topic>.md`. API proposals → `.ai/memory/projects/<slug>/tech/api-<capability>.md`. ADRs for durable decisions → see `pm-phase-define/references/decision-memo-daci.md`.
