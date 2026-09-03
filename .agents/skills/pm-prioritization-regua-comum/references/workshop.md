# Prioritization workshop and governance

## Running a workshop (60–90 min)

**Participants:** Product (facilitates), Engineering (effort), Sales and CS (market evidence), the owner of the strategic dimension in your ruler configuration (security, compliance, or whoever owns D3), leadership (HIPO, exceptions, tie-breaks). 5–7 people.

**Inputs to prepare beforehand:** a short list of candidate initiatives (8–15), a blank template (see `templates.md` or the sheet), the ruler configuration filled in, and the official impact definition visible in the room.

| Step | Time | What happens |
|---|---|---|
| 1. Frame | 5 min | Read the impact definition and the protection rules aloud. Remind everyone: the ruler is the same for all. |
| 2. Evidence | 15 min | For each item, Sales/CS/the D3 owner bring evidence in 1–2 sentences. No defending scores yet — facts only. |
| 3. Impact scores | 20–30 min | Score the 3 dimensions item by item. Disagreement > 1 point → hear both sides for 60s and close. Product records. |
| 4. Weighters | 10 min | Set confidence (by source count) and HIPO (default Neutral; leaving it needs a **logged** leadership decision). Compute final impact. |
| 5. Lock + effort | 10 min | Apply the Abrangência lock and log exceptions. Engineering gives effort (Low/Medium/High). |
| 6. Plot and decide | 10–15 min | Place on the matrix, read the quadrant, record decision and owner per item. |

**Expected output:** filled matrix/sheet + decision table (item → quadrant → decision → owner → next step) + the logged lists of exceptions and non-Neutral HIPOs — ready as input for PI Planning.

Tips: time-box each item; the facilitator cuts long debates; no reopening scores outside the right step.

## Protection rules against customization

- **a) Sales requests** enter the ruler like any other. Sales provides **evidence**, not the final score. No sales request is automatically high impact.
- **b) Current-customer requests** raise **confidence in the problem**, not the impact of the solution. Score Abrangência separately: "ACME asked for it" raises confidence; it only becomes high impact if the problem generalizes **and** the solution is reusable.
- **c) Abrangência lock (the main protection):** no initiative may be classified **high impact** while scoring **low on Abrangência (1–2)**, except when it is **mandatory** for a documented regulatory or strategic obligation, critical security, or retention of **material recurring revenue** (a large deal/renewal provably at risk). *Material* is the limit in the ruler configuration, never a number invented in the session.
- **d) Allowed exceptions (lock override):** only the three cases in (c). Every exception is logged with an owner, a one-sentence rationale, and the OKR/risk it protects. No log, no exception.
- **e) HIPO does not replace the lock:** leadership can signal conviction through HIPO, but that **does not** disable the lock nor waive the exception log. An item with Abrangência 1–2 raised to High stays flagged as "check the exception".
- **f) When to treat it as customization:** if **Abrangência = 1–2 and there is no valid exception**, the item **does not enter the product roadmap**. Three paths: **parametrize** (turn it into config that serves everyone, raising Abrangência), **deliver it as a paid service/project** (outside the roadmap), or **decline** with a clear reason.

## Light governance

Keep the model alive without bureaucracy.

- **Review cadence:** every PI/quarter, in a short 20-minute retro — not a new meeting.
- **Scores:** only recalibrate an old score with relevant new evidence (do not revisit the past for sport).
- **Thresholds (bands):** adjust only if, in practice, nearly everything lands in the same band (the ruler is not separating well).
- **Dimensions:** the three change only when the OKRs change. What D1 and D3 serve is written in the ruler configuration; change it there, then reread the anchors.
- **Factors (confidence and HIPO):** keep the values for at least 2 cycles before touching them.
- **Watch the HIPO:** count how many items depended on a non-Neutral HIPO in the cycle. Many means the ruler is being worked around; investigate why.
- **Watch the lock exceptions:** if the lock is overridden often, re-examine the ruler.
- **Model owner:** Product maintains the Régua Comum, the exception log and the HIPO log.
