# Rubrics 1–5 — impact and effort

The full scoring rubrics for the Régua Comum. `SKILL.md` carries only the summary; use these tables when you score.

The three dimensions are structural: every instantiation of the ruler has them. What each one *serves* is configurable — see `## Configure the ruler` in `SKILL.md` and the fill-in block at the top of `templates.md`. One worked instantiation is at the bottom of this file.

## Dimension 1 — Business impact
*Does this generate, unblock, expand, or protect the commercial outcome the ruler is configured to serve (recurring revenue in most instantiations)?*

| Score | Criterion | Signals / examples |
|---|---|---|
| 5 | Unblocks or protects material recurring revenue across several accounts; blocks an enterprise deal or a relevant renewal | A capability several prospects named as a deal-blocker; a paid tier that gates core value |
| 4 | Expands revenue across a band of accounts, opens a clear upsell, or improves trial-to-paid conversion | A plan upgrade path; tier enforcement moving free usage to paid |
| 3 | Contributes indirectly (reduces churn, improves activation) with no direct revenue line | First-use onboarding and activation; feature discovery |
| 2 | Small or one-off revenue, usually from a single account | A bespoke tweak to close one small deal |
| 1 | No perceptible revenue effect | A cosmetic request with no link to upsell or retention |

> **Materiality:** *material* means the limit written into the ruler configuration, set once from your own revenue base. Never invent a threshold mid-session, and never import one from another company's ruler.

## Dimension 2 — Abrangência *(includes reuse)*
*Does the problem serve several customers/segments **and** does the solution become a reusable capability, instead of a one-account customization? Key question: what is the best evidence that this holds for more than one customer and turns into reusable product?*

| Score | Criterion | Signals / examples |
|---|---|---|
| 5 | Problem is relevant across segments/prospects **and** the solution becomes a platform capability the whole base reuses, with no per-customer hard-coding | An obligation the entire base shares; enterprise IAM; a report export every account can run |
| 4 | Several sources signalled it **and** the solution is reusable across a broad segment with light parametrization | An on-prem / self-hosted edition for customers without public cloud |
| 3 | More than one source signalled it **or** there is a strong generalization hypothesis; reusable with moderate abstraction effort | Organization and multi-team management |
| 2 | Few signals beyond one account; reuse would mean rebuilding most of it | An integration designed around one customer's internal flow |
| 1 | Isolated request from a single account, hard-coded, not reusable | A field, report or export format tailored to one deal |

## Dimension 3 — Strategic & risk
*Does this advance the strategic, regulatory or security position the ruler is configured to serve, or mitigate strategic risk?*

| Score | Criterion | Signals / examples |
|---|---|---|
| 5 | Central to the configured strategic, regulatory or security value proposition, or mitigates critical strategic risk | Audit-ready evidence for a regulation the base is subject to; a security primitive the positioning depends on |
| 4 | Clearly reinforces the security / compliance-readiness narrative | Per-asset traceability of known vulnerabilities; pinned versus open tracking |
| 3 | Touches security/compliance without being central | Access governance (SSO/SCIM) read as control |
| 2 | Weak connection to security or strategy | A UX improvement with no security angle |
| 1 | No strategic, regulatory or security relevance | A purely cosmetic tweak |

> **Safe language:** when the dimension serves a regulation, describe the product as offering *readiness, enablement, evidence, operational support*. Do not claim the product certifies compliance with a regulation.

## Weighter — Confidence (discount for evidence quality)

In a data-immature environment qualitative evidence is acceptable; what matters is how many independent sources converge.

| Confidence | Factor | When to use |
|---|---|---|
| **Low** | 0.70 | Hypothesis with no validation; signal from **a single source** with no corroboration; discovery not done |
| **Medium** | 0.85 | Signal from **2+ independent sources** **or** partial discovery; coherent pattern with gaps |
| **High** | 1.00 | Discovery done **+** converging signals (sales + CS + pipeline), **or** a documented regulatory/contractual obligation |

**Acceptable qualitative evidence, by source:** sales signals (deal notes, win/loss, number of blocked opportunities) · current customers (QBR asks, repeated tickets, usability tests) · CS/support (same pain across accounts) · discovery (interviews, surveys, prototypes) · security/compliance (regulatory text, audit questionnaires, deadlines) · engineering/product (feasibility, technical debt) · pipeline (number of dependent opportunities).

Rule of thumb: **1 source = low; 2+ sources or partial discovery = medium; discovery + convergence or a documented obligation = high.**

## Weighter — HIPO (leadership conviction, explicit and bounded)

| HIPO | Factor | When to use |
|---|---|---|
| **Deprioritize** | 0.85 | Leadership wants the priority lowered (e.g. a strategic bet moving out of focus) |
| **Neutral** | 1.00 | Default. No strong conviction — the evidence speaks for itself |
| **Prioritize** | 1.15 | Leadership holds strategic conviction to raise it (e.g. "enterprise is this year's wedge") |

**HIPO honesty rules (non-negotiable):**
1. **Default is Neutral.** It only leaves Neutral with an explicit leadership decision made in the room.
2. **Every non-Neutral HIPO is logged** — who decided and why (one sentence). No log, back to Neutral.
3. **It rescues no weak item and kills no strong one:** capped at ±15%, it moves **at most one band**. Wanting to move further is a decision **outside the model**, annotated as such.
4. **Governance counts the HIPOs.** Many items depending on HIPO means the ruler is being worked around, not that the ruler is wrong.

## Effort rubric (Low / Medium / High)

Look at the six signals; **the worst signal sets the score**.

| Signal | Low | Medium | High |
|---|---|---|---|
| Technical complexity | Localized change, known pattern | Several components, something new | New component or a problem with no ready solution |
| Dependencies | None / team only | 1–2 teams or one partner | Several teams / external partners on the critical path |
| Risk | Low, reversible | Moderate | Can break existing flows or data |
| Discovery needed | Already understood | Light discovery | Significant discovery before estimating |
| Architectural impact | None | Contained adjustment | Touches foundations (auth, data model, platform) |
| Validation / compliance | Standard testing | Extra validation | Heavy security/compliance validation |

Rule of thumb: **all Low = Low; some Medium and no Highs = Medium; any High = High.**

## Reading the quadrants

- **Top priority** (high/low) — do it now; best return per unit of effort.
- **Plan (PI)** (high/medium) — goes into the next PI with sequencing and an owner.
- **Evaluate trade-off** (high/high) — worth it, but decide the opportunity cost; consider phasing (MVP).
- **Quick win** (medium/low) — good for filling capacity; batch several.
- **Prioritized backlog** (medium/medium) — normal queue, no urgency.
- **Caution** (medium/high) — only with a strong strategic reason; otherwise defer.
- **Opportunistic** (low/low) — only with spare capacity and no debt created.
- **Avoid** (low/medium) — usually not worth it.
- **Do not prioritize** (low/high) — say no, clearly.

## Example instantiation — embedded/IoT platform under the EU CRA

One configuration of the ruler, kept here as an example. These anchors belong to that domain, not to the model: another company configures D1 and D3 against its own OKRs and writes its own anchors.

- **D1 Business impact** serves ARR. Score 5 anchors: enterprise IAM (SSO/SCIM) that unblocks deals; a paid tier of the Vulnerability Manager. Score 4 anchors: upgrade from Developer to Professional; tier enforcement (free to paid).
- **D3 Strategic & risk** serves EU CRA readiness. Score 5 anchors: SBOM/VEX and audit-ready reports; encrypted partition and fTPM. Score 4 anchors: per-device CVE traceability; pinned versus open tracking.
- **Safe language in this domain:** describe the offering as *CRA readiness, CRA enablement, CRA evidence, CRA operational support, compliance readiness*. Do not claim the product "certifies CRA compliance".
- **Materiality limit for D1** in this instantiation: a deal or renewal above the account tier the commercial team defined as material. The number lives in the ruler configuration, not in this file.
