# Initiative evaluation template

## Ruler configuration (fill once per team, revisit when the OKRs change)

```
RULER CONFIGURATION

D1 Business impact  → the commercial OKR it serves:            ____________________
D3 Strategic & risk → the strategic/regulatory OKR it serves:  ____________________
Materiality limit for D1 (what counts as "material" here):     ____________________
                          (set from your own revenue base; never invented mid-session)
Owner of the configuration:                                    ____________________
```

D2 Abrangência is not configurable: it always asks whether the problem generalizes and the solution is reusable.

## Per-item block

Copy this block for each backlog item.

```
INITIATIVE: ____________________________________________

Demand origin:            [ Sales | Current customer | CS/Support | Security/Compliance | Discovery | Engineering/Product | Pipeline ]
Problem to solve:         ____________________________________________
Value hypothesis:         We believe [solution] will produce [outcome/OKR] for [whom]
Available evidence:       (sources and what each one says)
                          - ____________________________________________
                          - ____________________________________________

IMPACT SCORES (1–5)
  D1 Business impact ......... [ ]
  D2 Abrangência ............. [ ]
  D3 Strategic & risk ........ [ ]

  Raw impact = (D1+D2+D3) ÷ 3 = ______

WEIGHTERS
  Confidence: [ Low 0.70 | Medium 0.85 | High 1.00 ]   →  factor = ______
  HIPO:       [ Deprioritize 0.85 | Neutral 1.00 | Prioritize 1.15 ]   →  factor = ______
              (if ≠ Neutral, log:  who decided ______  why ______ )

  Final impact = raw × confidence factor × HIPO factor = ______   (max 5.00)
  Classification: [ Low | Medium | High ]

ABRANGÊNCIA LOCK:         Is D2 1–2 and the item classified High?  [ No ]
                          If Yes → valid exception? (documented regulatory or strategic
                          obligation / critical security / retention of material recurring revenue)
                          Exception logged by: __________  Rationale: __________

EFFORT:                   [ Low | Medium | High ]
MATRIX QUADRANT:          ____________________________________________

RECOMMENDED DECISION:     [ Do now | Plan (PI) | Evaluate trade-off | Backlog | Customization (service/parametrize) | Decline ]
NEXT STEPS / OWNER:       ____________________________________________
```

## Aggregate session output

- Filled matrix/sheet (Impact × Effort).
- Decision table: item → quadrant → decision → owner → next step.
- List of logged Abrangência lock exceptions (owner, rationale, OKR/risk protected).
- List of logged non-Neutral HIPOs (who decided, why).
