---
name: pm-archetype-enterprise
description: >-
  Enterprise / B2B PM archetype lens. Invoke when the product serves
  organisations rather than individuals — admins, IT, security teams,
  procurement, auditors, end-users inheriting corporate policies. Covers
  identity (SSO/SCIM), access control (RBAC/ABAC), audit logs, compliance
  (SOC 2 / GDPR / HIPAA / FedRAMP), data residency, encryption / KMS, admin
  experience (bulk ops, policy templates), procurement readiness
  (DPA/MSA/security questionnaires), staged rollout to large accounts, and
  integration surface (APIs, webhooks, warehouse exports). Trigger on "SSO",
  "RBAC", "audit log", "SOC 2", "security questionnaire" — and on any
  permission-model, tenant, deprovisioning, procurement, or compliance
  question about an enterprise account or a rollout to a large one. Pairs
  with the pm-phase-* skills and pm-transversal-stakeholder; the full
  trigger list and pairings live in the skill body.
---

# PM Archetype — Enterprise / B2B products

> Product-type lens. Pairs with phase skills when the product serves organisations, not individuals. Enterprise products are often won or lost on administration, governance, and compliance — areas consumer PMs may never need to own deeply.

## Prime directive

**Control without friction.** Enterprises need governance (permissions, audit, compliance) AND usability at scale. Heavy controls with poor UX lose adoption; usability without controls loses deals. Balance both.

## When to invoke

The product or feature is sold to or operated by organisations, and any of the following matter:

- identity (SSO via SAML / OIDC, SCIM provisioning, IdP constraints, multi-region directory)
- access control (RBAC, ABAC, role hierarchies, scoped permissions, admin delegation)
- audit + compliance (immutable audit logs, SOC 2 / ISO / HIPAA / GDPR / FedRAMP)
- data governance (residency EU/Gov, retention, export, deletion, DPA)
- security posture (encryption at rest / transit, KMS, BYOK, IP allow-list, private networking)
- admin experience (bulk operations, policy templates, org-wide settings, migration wizards)
- procurement (security questionnaires, DPA, MSA, redlines, technical docs for RFPs)
- change management (phased rollout for large orgs, training, communications)
- integration (API surface, webhooks, partner connectors, data warehouse exports)

For a B2B SaaS product this archetype applies to most of the product surface — multi-tenant fleets, large industrial customers, signed updates, audit obligations.

### Trigger phrases

"SSO", "SCIM", "RBAC", "audit log", "SOC 2", "GDPR", "HIPAA", "compliance", "tenant", "multi-tenant", "admin experience", "data residency", "DPA", "security questionnaire", "RFP", "procurement", "enterprise customer", "rollout to a large account", "permission model", "deprovisioning", "offboarding", "SAML", "OIDC", "key management", "BYOK", "private networking", "air-gapped".

## Required reading before output

- `.ai/rules.md`, `.ai/app.md`, `.ai/memory/active-context.md`
- relevant project memory — **prior compliance decisions are especially important**; precedents bind future work

## References this skill chains to

- `../pm-phase-discover/references/jtbd-segmentation.md` — enterprise segments have distinct JTBDs by role (admin vs end-user vs security lead)
- `../pm-phase-define/references/business-case-prfaq.md` — enterprise bets need strong investment cases
- `../pm-phase-define/references/pricing-packaging.md` — enterprise packaging = governance features behind tier gates
- `../pm-phase-develop/references/prd-writing.md` — enterprise PRDs emphasise permission model, audit, rollout, migration
- `../pm-phase-develop/references/technical-fluency.md` — identity, SSO, data residency, encryption concepts
- `../pm-phase-deliver/references/launch-readiness.md` — enterprise launches are slower, more staged
- `../pm-transversal-stakeholder/` — enterprise = many stakeholders by design
- your security/compliance lead — when the product surfaces fall under regulatory obligations (e.g. EU CRA for device-cloud features)

## Workflow

1. **Identify all stakeholders** — admin, end-user, IT, security, procurement, auditor, exec sponsor.
2. **Characterise the org profile** — size, regulatory context, existing stack, appetite for change.
3. **Map the feature across stakeholders** — how each group experiences it; what each needs.
4. **Design the permission / governance model first** — RBAC matrix, audit log shape, admin-override paths.
5. **Specify compliance implications** — legal + security review needed; data-handling concerns; CRA / SOC 2 / GDPR mapping.
6. **Plan the rollout** — staged per customer segment; admin-controlled activation; migration pathway.
7. **Architecture check** — loop in your engineering architecture partner (identity + data models are hard to change later).
8. **Failure-mode analysis** — loop in your QA lead (enterprise failures are visible and contractual).
9. **Update memory** with enterprise-specific decisions and precedents (DACI for who can sign-off compliance trade-offs).

## Enterprise-specific anti-patterns

- **Treating enterprise requirements as checkboxes.** "SSO: yes" without defining IdP coverage, edge cases, and admin UX.
- **Over-indexing on one customer's bespoke ask.** Shipping a custom capability for the biggest account distorts the product.
- **Complex controls with poor UX.** Admins give up, revert to defaults, security posture worsens.
- **"We'll deal with compliance later."** Retrofitting compliance is 10x the cost of building it in.
- **Missing audit log coverage.** A change you can't audit is a compliance incident waiting to happen.
- **No admin override / recovery path.** Admins locked out of their own org.
- **Ignoring deprovisioning.** Offboarding + data deletion are first-class requirements, not afterthoughts.
- **Pricing confusion.** Enterprise packaging changes that blow up existing contracts.

## Output format

```text
## pm-archetype-enterprise recommendation

### Customer / org profile
segment + regulated context + stack

### Stakeholders (by role)
admin / end-user / IT / security / procurement / exec sponsor

### Feature summary
what ships

### Permission + governance model
RBAC matrix, default scope, admin capabilities, override paths

### Audit + compliance
audit log events, SOC 2 / GDPR / industry-specific implications, legal review needed

### Rollout plan
dark / internal / pilot account / controlled GA / full; per-customer activation

### Migration / deprovisioning
what admins must do; what the system does automatically

### Procurement readiness
security-questionnaire readiness, DPA updates needed, technical doc updates

### Risks + mitigations
technical, compliance, commercial, change-management

### Memory updates
```

## Integration

- Upstream: `pm-phase-discover` (admin / security / end-user JTBDs), `pm-phase-define` (business case for enterprise bets + packaging).
- Build phase: `pm-phase-develop` (PRD with permission model + audit log shape + migration wizard).
- Launch: `pm-phase-deliver` with extra-staged rollout and per-account activation.
- Transversals: `pm-transversal-stakeholder` (admin/IT/security alignment, exec sign-off), `pm-transversal-docs` (DPA-friendly Confluence pages, audit-event catalogue).
- Engineering pairings: your engineering architecture partner (identity and data-model decisions), your QA lead (audit log coverage, deprovisioning checks), your security/compliance lead (CRA evidence trail).
- Copilot mirror: [.github/agents/pm-enterprise.agent.md](../../../.github/agents/pm-enterprise.agent.md).

## Success criteria

- admins adopt new controls (they trust the UX)
- compliance officers sign off without redesign
- rollout to large accounts completes on schedule
- audit logs cover every meaningful action
- deprovisioning / data deletion works correctly for every role
- enterprise segments express the features they need without a 1:1 PM hand-hold
