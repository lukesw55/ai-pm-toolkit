# Report Template

Use estes templates para comunicação final.

## Executive Analytical Report

```markdown
# [Analysis Title]

## Executive Summary

- **Decision answer:** [clear recommendation or answer]
- **Most important evidence:** [metric/statistic/check]
- **Impact:** [business/product/operational implication]
- **Confidence:** [High/Medium/Low] because [reason]

## Key Findings

| Finding | Evidence | Impact | Confidence |
|---|---|---|---|
| [Finding 1] | [Metric, chart, query or test] | [Why it matters] | [High/Medium/Low] |

## Data Used

| Source | Rows | Columns | Time window | Grain | Notes |
|---|---:|---:|---|---|---|

## Data Quality

| Issue | Severity | Impact | Recommended fix |
|---|---|---|---|

## Method

[Short explanation of the approach, filters, assumptions and validation.]

## Limitations

- [Limitation that could affect the conclusion]
- [Missing data / bias / measurement issue]

## Recommended Next Steps

1. [Highest leverage next action]
2. [Validation or follow-up analysis]
3. [Operational or product action]
```

## EDA Report

```markdown
# Exploratory Data Analysis: [Dataset]

## Objective

[What question this EDA supports.]

## Dataset Overview

| Metric | Value |
|---|---:|
| Rows | [n] |
| Columns | [n] |
| Time range | [start–end] |
| Unit of analysis | [grain] |
| Primary key | [key] |

## Data Quality Summary

| Issue | Severity | Evidence | Action |
|---|---|---|---|

## Main Patterns

| Pattern | Evidence | Hypothesis | Next validation |
|---|---|---|---|

## Charts

- `[path/to/chart.png]` — [takeaway]
- `[path/to/chart.png]` — [takeaway]

## Limitations and Open Questions

- [Question]
```

## ML Model Card

```markdown
# Model Card: [Model Name]

## Intended Use

[What the model is for and who uses it.]

## Not Intended For

[Use cases that are unsafe or unsupported.]

## Data

| Split | Rows | Time window | Notes |
|---|---:|---|---|

## Target

- Target column: `[target]`
- Prediction moment: `[when prediction is made]`
- Positive class / label definition: `[definition]`

## Features

| Feature group | Description | Leakage risk |
|---|---|---|

## Training Procedure

- Split method: [random/time/group]
- Preprocessing: [summary]
- Model: [algorithm]
- Baseline: [baseline]

## Evaluation

| Metric | Baseline | Model | Notes |
|---|---:|---:|---|

## Segment Performance

| Segment | Metric | Notes |
|---|---:|---|

## Error Analysis

| Error type | Example | Potential fix |
|---|---|---|

## Risks and Limitations

- [Risk]
- [Limitation]

## Monitoring

- Data drift checks
- Performance by segment
- Calibration
- Retraining trigger
```

## Experiment Report

```markdown
# Experiment Analysis: [Experiment Name]

## Decision

[Ship / do not ship / continue / inconclusive]

## Experiment Design

| Item | Value |
|---|---|
| Hypothesis | [hypothesis] |
| Unit of randomization | [unit] |
| Unit of analysis | [unit] |
| Start/end | [dates] |
| Primary metric | [metric] |
| Variants | [control/treatment] |

## Validity Checks

| Check | Result | Notes |
|---|---|---|
| Sample ratio mismatch | [pass/fail] | [details] |
| Pre-period balance | [pass/fail/n.a.] | [details] |
| Missing data | [pass/fail] | [details] |

## Results

| Metric | Control | Treatment | Absolute effect | Relative effect | 95% CI | p-value |
|---|---:|---:|---:|---:|---|---:|

## Interpretation

[Separate statistical significance, practical significance and risk.]

## Limitations

- [Limitation]

## Recommendation

[Action]
```
