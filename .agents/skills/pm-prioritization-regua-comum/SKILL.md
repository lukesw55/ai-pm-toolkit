---
name: pm-prioritization-regua-comum
description: >
  The "Régua Comum" product-prioritization model — Impact × Effort with a
  single shared impact ruler. Use whenever the user needs to prioritize
  initiatives, score a backlog, run or prepare a prioritization session, decide
  what goes into the next PI, or tell product evolution apart from one-account
  customization. Triggers on "priorizar", "régua comum", "impacto x esforço",
  "o que fazer primeiro", "vale a pena fazer isso?", "isso é customização?",
  "score this backlog", "prioritization workshop", "ARR / Abrangência / CRA",
  "confiança", "HIPO". Scores three impact dimensions (Business impact,
  Abrangência, Strategic & risk), applies confidence and HIPO weighters,
  enforces the Abrangência lock against customization, rates effort, and plots
  the Impact × Effort matrix into a decision. Runs on Amplitude's North Star
  Framework as a working premise: impact is leverage on the North Star Metric
  through its inputs. The ruler is the same for everyone; who asks changes the
  *evidence*, not the *score*.
---

# Régua Comum — product prioritization

One shared impact ruler for every team. Whoever asks (sales, customer, CS, engineering, leadership) changes the **evidence**, not the **ruler**. Impact is always computed the same way, regardless of who brought the request or how urgent it looks.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## Core principle

Optimize for **product leverage**: prioritize what becomes a reusable capability, serves the OKRs the ruler is configured against, and is strategically relevant. The model exists to avoid two errors: (1) turning the roadmap into a queue of single-account commercial customizations, and (2) faking quantitative precision we don't have. Commercial urgency, a big customer's name, and leadership opinion do **not** raise impact on their own — they enter as evidence (or as an explicit, limited weighter) and are counterbalanced by confidence.

## Configure the ruler

The three dimensions are structural; what two of them serve is configured once per team, before any scoring.

- **D1 Business impact** names the commercial OKR it serves (recurring revenue in most instantiations).
- **D2 Abrangência** is fixed: does the problem generalize and does the solution become reusable?
- **D3 Strategic & risk** names the strategic, regulatory or security OKR it serves.
- **Materiality for D1** is a limit set once from your own revenue base. Never invent a threshold mid-session, and never import one from another company's ruler.

Write the configuration into the block at the top of `references/templates.md` and revisit it only when the OKRs change. `references/rubric.md` closes with one worked instantiation as an example of what a filled configuration looks like.

## North Star premise (working assumption)

The Régua Comum operationalizes Amplitude's North Star Framework. The OKRs this ruler serves sit downstream of one **North Star Metric (NSM)**, the leading indicator of revenue that captures the value customers get from the product. Lagging business results such as recurring revenue and net-new customers are what the NSM leads; they are not what you score directly. Your product's NSM and its inputs come from your North Star definition; until that converges, treat the NSM as a hypothesis and lean on the confidence factor.

Teams never move the NSM directly. They move a small set of **inputs** that produce it. Read any initiative through the levels of bets: the NSM is Level 0, an input is Level 1, an opportunity to move that input is Level 2, an intervention or feature is Level 3.

**Binding rule:** every scored initiative names the North Star input it intends to move (Level 1) and the opportunity it exploits (Level 2). If you cannot trace it to an input, that is the framework's roadmap-check signal: either the work is not valuable, or an input is missing from the model. Flag it before scoring; do not invent the link.

Prioritize by how much the input influences the NSM and how likely this initiative is to move that input. The three impact dimensions below are how the Régua Comum estimates that; they are not three unrelated scores.

## Official impact definition (read this aloud at the top of every session)

> **Impact is how much an initiative moves our OKRs through a reusable, strategically relevant capability, not how much a single account wants it, nor how urgent it seems, nor who champions it.**

## Procedure

Work each initiative through these steps. Use the template in `references/templates.md` (copy one block per backlog item). Detailed 1–5 rubrics live in `references/rubric.md`; worked examples in `references/examples.md`; the workshop and governance in `references/workshop.md`.

1. **Frame the demand.** Capture origin (Sales / Customer / CS / Security-Compliance / Discovery / Engineering / Pipeline), the problem, the value hypothesis, the evidence per source, and the **North Star input (Level 1)** the initiative intends to move plus the opportunity (Level 2). Origin never sets the score; it sets confidence. If no input link exists, raise it as a roadmap-check signal before scoring.

2. **Score the 3 impact dimensions, 1–5 each** (full rubric in `references/rubric.md`):
   - **D1 Business impact** — does it generate, unblock, expand, or protect the configured commercial outcome?
   - **D2 Abrangência** (includes reuse) — strong evidence it serves more than one customer/segment **and** the solution becomes a reusable capability, not a one-account customization?
   - **D3 Strategic & risk** — does it advance the configured strategic, regulatory or security position, or mitigate strategic risk?

   North Star reading: each dimension estimates how the initiative moves an input toward the NSM. D1 Business impact is the lagging commercial result the NSM leads, so score the input movement, not the NSM itself. D2 Abrangência is the breadth and reuse of that movement across the base, which is why a one-account pull scores low (the NSM is customer value, never a single account). D3 Strategic & risk covers strategic, regulatory and system-health inputs (the framework recommends a system-health indicator input).

3. **Compute raw impact** (simple average):

   ```
   Raw impact = (Business + Abrangência + Strategic) ÷ 3
   ```

4. **Apply the two weighters** — they are *not* impact dimensions; they adjust an already-computed impact:

   ```
   Final impact = Raw impact × Confidence factor × HIPO factor   (capped at 5.00)
   ```

   | Confidence (evidence quality — only discounts) | Factor |
   |---|---|
   | Low (1 source / hypothesis / no discovery) | 0.70 |
   | Medium (2+ sources or partial discovery) | 0.85 |
   | High (discovery + convergence, or documented regulatory/contractual obligation) | 1.00 |

   | HIPO (leadership conviction — explicit & limited) | Factor |
   |---|---|
   | Deprioritize | 0.85 |
   | Neutral (default) | 1.00 |
   | Prioritize | 1.15 |

   HIPO rules (non-negotiable): default is **Neutral**; any non-Neutral HIPO must be **logged** (who decided + one-sentence why) or it reverts to Neutral; HIPO is capped at ±15%, so it moves **at most one classification band** — it never rescues a weak item nor kills a strong one. Moving more than one band is a decision **outside the model** and must be annotated as such.

5. **Classify the final impact:**

   | Band | Impact |
   |---|---|
   | 1.00 – 2.49 | Low |
   | 2.50 – 3.74 | Medium |
   | 3.75 – 5.00 | High |

6. **Apply the Abrangência lock (the main protection against customization):**

   > No initiative may be classified **high impact** if it scores **low on Abrangência (1–2)**, except when it is **mandatory** for a documented regulatory or strategic obligation, critical security, or retention of **material recurring revenue** (a large deal/renewal provably at risk).

   *Material* is the limit written into the ruler configuration, never a number invented in the session. Allowed exceptions cover only those three cases and must be **logged** (owner, one-sentence justification, the OKR/risk it protects). HIPO does **not** disable the lock or waive the exception log. If **Abrangência = 1–2 and no valid exception**, it does **not** enter the product roadmap — route it: **parametrize** (turn into config that serves everyone, raising Abrangência), **deliver as a paid service/project** (outside the product roadmap), or **decline** with a clear reason.

7. **Rate effort — Low / Medium / High** (six signals in `references/rubric.md`). The worst signal pulls the score: any single "High" signal (risk, architecture, compliance) makes effort High. Rule of thumb: all Low = Low; some Medium, no Highs = Medium; any High = High.

8. **Plot Impact × Effort and read the quadrant:**

   |  | Low effort | Medium effort | High effort |
   |---|---|---|---|
   | **High impact** | 🟢 Top priority | 🟢 Plan (PI) | 🟡 Evaluate trade-off |
   | **Medium impact** | 🟢 Quick win | 🟡 Prioritized backlog | 🔴 Caution |
   | **Low impact** | ⚪ Opportunistic | 🔴 Avoid | ⛔ Do not prioritize |

9. **Record the decision and owner.** Map the quadrant to a recommended decision (Do now / Plan (PI) / Evaluate trade-off — consider phasing an MVP / Backlog / Customization / Decline) and assign a next step + owner. For high/high, prefer phasing (MVP first) to cut risk.

## Protection rules (summary)

- Sales requests enter the ruler like any other; Sales provides **evidence**, not the final score. No sales request is automatically high impact.
- An important customer raises **confidence in the problem**, not the impact of the solution. Score Abrangência separately.
- The Abrangência lock and exception log are the backbone — keep them honest.

## What to produce

A filled matrix/sheet plus a decision table (item → North Star input → quadrant → decision → owner → next step) and the logged list of exceptions and non-Neutral HIPOs — ready as input for PI Planning. When the input is qualitative or thin, be explicit about uncertainty via the confidence factor rather than inventing precision. For deeper quantitative validation of the evidence (datasets, SQL, A/B), chain with `data-science-analyst`; for turning decisions into roadmap narrative, chain with `pm-phase-define`.
