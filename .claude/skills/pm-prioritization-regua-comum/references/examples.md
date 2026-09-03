# Worked examples

Three examples across three quadrants, showing the weighters in action — including HIPO at its maximum **failing** to rescue a customization (Example B).

> **One instantiation, not universal anchors.** These examples come from an embedded/IoT platform whose ruler is configured with **D1 Business impact serving ARR** and **D3 Strategic & risk serving EU CRA readiness** (see the example instantiation at the bottom of `rubric.md`). The scores illustrate how the method behaves; the domain anchors are that company's configuration, not part of the model. Score notes are written as `D1 Business (ARR)` and `D3 Strategic (CRA)` so structure and configuration stay visible.

## Example A — Exportable vulnerability report for audit
*(SBOM/VEX/CVE audit-ready, tied to the Vulnerability Manager)*

| Field | Assessment |
|---|---|
| Origin | Security/Compliance + Marketing + Discovery |
| Problem | Customers need exportable, audit-ready evidence of CVEs/SBOM/VEX to demonstrate diligence (CRA readiness) |
| Scores | D1 Business (ARR) = **4** · D2 Abrangência = **5** · D3 Strategic (CRA) = **5** |
| Raw impact | (4+5+5)/3 = **4.67** |
| Confidence | **High** (1.00) — regulation + multiple sources |
| HIPO | **Neutral** (1.00) — the evidence stands on its own |
| Final impact | 4.67 × 1.00 × 1.00 = **4.67 → High** |
| Abrangência lock | Clear (D2=5) |
| Effort | **Medium** — reuses existing SBOM/VEX/CVE data; the work is formatting + validation |
| Quadrant | High + Medium = **Plan (PI)** |
| Decision | Plan for the next PI; a central compliance-evidence capability the whole base reuses |

## Example B — Bespoke tweak a prospect asked for to close a small deal
*(e.g. an export format tailored to one prospect's internal ERP)*

| Field | Assessment |
|---|---|
| Origin | Sales (one prospect) |
| Problem | Export format tailored to the prospect's ERP; sales says it unblocks a small deal |
| Scores | D1 Business (ARR) = **2** · D2 Abrangência = **1** · D3 Strategic (CRA) = **1** |
| Raw impact | (2+1+1)/3 = **1.33** |
| Confidence | **Medium** (0.85) — a real prospect request, but a single source |
| HIPO | **Prioritize** (1.15) — *a sales leader is pushing to land the logo* (logged) |
| Final impact | min(5 ; 1.33 × 0.85 × 1.15) = **1.30 → Low** |
| Abrangência lock | Triggers: D2=1 → **treat as customization** |
| Effort | **Low** |
| Quadrant | Low + Low = **Opportunistic** |
| Decision | **Does not enter the product roadmap.** Even with HIPO at its maximum it stays low — the model resists the pressure. Paths: parametrize (if reuse exists), deliver as a paid service, or decline. |

## Example C — Integration with a tool several enterprise prospects use
*(enterprise IAM: SSO + SCIM, identified as a deal-blocker in discovery)*

| Field | Assessment |
|---|---|
| Origin | Discovery + Pipeline (several enterprise prospects) |
| Problem | Enterprise prospects require SSO (authentication) and SCIM (provisioning) to adopt the product at scale |
| Scores | D1 Business (ARR) = **5** · D2 Abrangência = **5** · D3 Strategic (CRA) = **4** |
| Raw impact | (5+5+4)/3 = **4.67** |
| Confidence | **Medium** (0.85) — discovery done, but segment/revenue not yet confirmed |
| HIPO | **Neutral** (1.00) |
| Final impact | 4.67 × 0.85 × 1.00 = **3.97 → High** |
| Abrangência lock | Clear (D2=5) |
| Effort | **High** — touches identity architecture, the organization model, security validation |
| Quadrant | High + High = **Evaluate trade-off** |
| Decision | Strong candidate. **Phase it** to cut risk: SSO as the MVP first, SCIM after. Confirm segment and revenue before committing the full effort. |
