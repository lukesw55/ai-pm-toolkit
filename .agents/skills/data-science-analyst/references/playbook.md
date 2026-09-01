# Data Analysis Playbook

Detailed workflows behind the modes in `SKILL.md`. Use these checklists when running an audit, cleaning, EDA, SQL analytics, experiment analysis, or ML baseline.

## 1. Intake checklist

Before analysing:

- What decision will this analysis support?
- What is the unit of analysis?
- What is the time window?
- Which is the load-bearing metric?
- Does the data contain PII or regulated fields? (A churn-analysis project may hold CRM PII at a local path. Aggregate before crossing the workspace boundary.)
- Is there a data dictionary?
- If supervised: what is the target, and at what moment does it become known? (Leakage anchor.)
- Is there enough history?
- Risk of seasonality, selection bias, or external shocks?
- Expected output type: notebook, script, query, report, dashboard scaffold, or model?

## 2. Dataset audit checklist

| Check | Question | Red flag |
|---|---|---|
| Shape | rows × columns | far from expected |
| Grain | what does one row represent? | multiple grains in one file |
| Keys | unique ID present? | unexplained duplicates |
| Missingness | random or structured? | critical columns with high nulls |
| Types | match meaning? | dates as text; numbers with symbols |
| Ranges | values plausible? | negative ages; infinite revenue |
| Categories | standardised? | multiple spellings of same value |
| Dates | window + timezone clear? | gaps; future dates; mixed timezones |
| Joins | cardinality preserved? | row explosion |
| Target | distribution healthy? | extreme imbalance |
| Leakage | features known only later? | target encoded into future fields |
| PII | sensitive columns present? | email, phone, address, device UUID |

## 3. Cleaning workflow

1. Copy raw → `data/interim/` or `data/processed/`. Never overwrite.
2. Standardise column names (snake_case).
3. Fix types.
4. Remove duplicates only with a documented rule.
5. Handle missingness with a justified strategy (drop, impute, flag, or model).
6. Standardise categories.
7. Validate ranges and business rules.
8. Validate joins (row count + key uniqueness).
9. Save data dictionary.
10. Record transformations in README or report.

### Minimum data dictionary

```markdown
| Column | Type | Description | Allowed values/range | Missing rule | Source |
|---|---|---|---|---|---|
```

## 4. EDA workflow

1. Initial profile (use `scripts/profile_dataset.py` for CSV/TSV).
2. Data quality table.
3. Univariate distributions.
4. Bivariate relationships against the load-bearing metric.
5. Relevant segmentations.
6. Temporal analysis if a date exists.
7. Outliers and edge cases.
8. Hypotheses + findings.
9. Limitations.
10. Next analyses.

### Chart rules

- One chart, one question.
- Title carries the insight, not the variable name.
- No 3D, no excess categories.
- Time series: state window + granularity.
- Distributions: show n, missing, and outliers when relevant.

## 5. SQL analytics workflow

1. Write the metric definition in plain language first.
2. Define final grain.
3. Define filters.
4. Build query with named CTEs.
5. Validate row counts at each step.
6. Validate key duplication.
7. Compare totals against canonical source.
8. Document edge cases (null, duplicate, timezone, late-arriving).

## 6. Experiment / A-B test workflow

1. Pre-declare hypothesis and primary metric.
2. Confirm unit of randomisation.
3. Confirm start/end and exposure logic.
4. Sample-ratio mismatch check (SRM).
5. Pre-treatment balance check when feasible.
6. Pick test or interval matching the metric type (proportion, mean, ratio, count).
7. Report absolute effect, relative effect, 95% CI.
8. Report practical significance (vs business threshold).
9. Declare or correct multiple comparisons.
10. End with a recommendation: ship / hold / iterate / kill.

## 7. Machine learning workflow

1. Define the business objective.
2. Define target and prediction moment.
3. Define temporal horizon.
4. Audit data and leakage candidates explicitly.
5. Split train/validation/test (random only if independent; temporal/group otherwise).
6. Build a baseline (constant, majority class, or simple heuristic) before any model.
7. Build preprocessing pipeline; fit only on training fold.
8. Train an interpretable model first.
9. Evaluate with metrics matched to the problem.
10. Error analysis — by segment, not just overall.
11. Check segment performance (fairness, key cohorts).
12. Save artefacts + metrics + model card.
13. Document risks and limitations.

### Metric selection

| Problem | Preferred metrics | Notes |
|---|---|---|
| Binary classification | ROC AUC, PR AUC, F1, recall, precision, calibration | PR AUC under heavy imbalance |
| Multiclass | macro/micro F1, balanced accuracy, confusion matrix | inspect minority classes |
| Regression | MAE, RMSE, MAPE/SMAPE if appropriate | careful with zeros in MAPE |
| Forecasting | MAE/RMSE per horizon, backtesting | compare to naive / seasonal naive |
| Ranking | NDCG, MAP, precision@k, recall@k | align with UX |
| Clustering | silhouette + stability + interpretability | never internal-metric only |

## 8. Reporting workflow

Every final delivery answers:

- What did we find?
- How do we know?
- How much does it matter?
- What could be wrong?
- What do we do now?

Use `references/report-templates.md` for the templates.
