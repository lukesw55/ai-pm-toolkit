# Eval design for product outputs

## What it is

The acceptance criteria of an AI feature, written down before the feature ships and re-run every time the prompt, the model or the retrieval changes. An eval is a scenario, a short list of good-answer rules, a set of graded cases and a decision rule that says what ships and what blocks. The PM owns the scenario, the rules, the hazard list, the numeric limits and the decision rule; engineering wires the harness that runs them. These are the product's evals, kept under `.ai/memory/projects/<slug>/evals/`. They are not the toolkit's own `evals/evals.json`, which grades skills, not products.

## Why it matters

Probabilistic features look finished in a demo and fail on the traffic the demo never saw. Without a written threshold nobody can say whether a change made the feature better, so every prompt tweak turns into an argument. An eval with numbers ends the argument; an eval without a threshold is an opinion with a spreadsheet attached. "The demo looked great" is the first anti-pattern this lens names, and this reference is the method that replaces it.

## The chain

Scenario → good-answer rules → test cases → responses → human labels (good / weak / fail, with a reason) → failure patterns → reference responses → product decisions. Judgement comes first and tooling later: twenty rows graded by two people teach more than a dashboard nobody trusts. Automate the checks that can be automated (a citation is present, a number has a formula, the answer is in the user's language) and keep the verdict human until a judge has been verified against humans.

## Ready-to-use template — Scenario sheet

```markdown
# Eval scenario — <feature>

- **Task**: what the feature does, in one sentence, for whom
- **User**: who reads the output and what they do with it without checking
- **Good-answer rules** (4 to 6, each testable):
  1. ...
- **Hazard list** (sized to the task and the segments it serves; about four failure modes is a usual start, one line each, sayable in a meeting):
  1. ...
- **Limits block** (the numbers the task needs, usually three to five, each with a one-line rationale, written before any scoring dimension and before the run):
  - at least NN % of golden rows graded good — because <what breaks below it>
  - zero rows in <blocking hazard> — because <what one such row costs>
  - 100 % of outputs carry <required element> — because <who depends on it>
  - at most NN % of outputs <undesired behaviour> — because <what the user cannot do then>
- **Decision rule**: ship when every limit holds; a single row in <blocking hazard> blocks release regardless of the pass rate, because a critical failure is never offset by a high average
- **Versions**: prompt <id/date>, eval file <id/date>, model <id>; the three change together
```

## Ready-to-use template — Golden-set sheet

```markdown
| id | source | input locator | expected behaviour | label | reason | handle | grader | last graded |
|---|---|---|---|---|---|---|---|---|
| 001 | real trace | ticket 48213 | summary cites the refund line, promises nothing | fail | invented a refund the ticket never made | hallucination | <role> | <date> |
```

Rules for the sheet:

- Size the set to the task and write the reason in the sheet: enough rows to cover every language, segment and input shape in proportion to traffic. About twenty is a workable start for one language and one segment, not a rule; grow it from production failures.
- At least one row is a real failure the team has already seen. A set with no failure in it is a scrapbook, not a test.
- Cover every language, segment and input shape the feature serves, in proportion to traffic.
- Real traces first; synthetic rows are practice material for a team that has no traces yet.
- Labels are `good` (usable as delivered), `weak` (usable after a material fix) and `fail` (wrong, harmful or unusable), with one line of reason per row.
- Handles name the pattern, not the row: golden, approved, reference, exemplar, broken logic, hallucination, bad UX, review needed, edge case. Rename them when the product needs other words; keep them few.

## Failure taxonomy for product outputs

| Failure | What it looks like | Detection | Default severity | Counts as a failure when |
|---|---|---|---|---|
| Hallucination | an invented fact, commitment, amount or citation stated with confidence | reference check against the source | blocking for commitments and citations | always for facts; for commitments and citations whenever the contract forbids inventing them (a summariser's does) |
| Broken logic | steps that contradict each other, or a conclusion the steps do not support | human read; arithmetic check | fail | always |
| Asked instead of answered | the feature stalls on a question the user expected it to resolve | pattern check on the output | weak; fail above the limit | the contract expects a resolved answer (a single-shot summary an agent acts on); a clarifying question is correct where the contract allows a dialogue |
| Missing evidence | a claim with no source, a number with no formula | automated presence check | weak | the contract requires traceability (here, agents act without opening the ticket); optional where the reader checks the source anyway |
| Unsupported numbers | round figures with no basis | human read | fail | always |
| Incomplete | part of the task done, the rest silently dropped | checklist against the task | weak | always, in proportion to what was dropped |
| Bad UX | correct content nobody can use: a wall of text, a buried answer, the wrong language | human read | weak | the audience cannot use it as delivered |

Severity is a product decision and lives in the scenario sheet, and so is the contract: asking a question or omitting a citation counts against an output only where the task requires the opposite, which is why the scenario sheet names the user and what they do with the output without checking. Invented commitments and invented citations default to blocking because they are the failures a PM cannot defend in front of a customer or an executive.

## Limits before dimensions

Write the numbers the task needs before adding a single scoring dimension; three to five is usual, and each carries a one-line rationale so the threshold can be defended before the run instead of adjusted after it. Dimensions without numbers feel rigorous and decide nothing. A limits block for a support summariser:

- at least 80 % of golden rows graded good, because below that agents stop trusting the summary and reopen the ticket
- zero hallucinated commitments, because one honoured refund costs more than the feature saves
- 100 % of summaries cite the ticket line they act on, because agents act without opening the ticket
- at most 5 % of outputs ask the agent a question instead of summarising, because the agent has no way to answer

If a fifth dimension appears before one of these numbers is written down, the team is expressing anxiety, not measuring quality. A critical failure is never offset by a high average: the block rule sits above the pass rate, whatever the mean says.

## Validation and verification

Validation happens once, before the first release decision: run the worst incident the feature has produced through the rubric. If the rubric passes it, the rubric is wrong; tighten a rule or add a hazard until the incident fails.

Verification is ongoing and applies to any automated judge, rubric-based or model-based. Take a sample the judge has scored (about thirty is a workable start; more when the task serves many segments), have two people re-grade it blind, and count the disagreements against a threshold you set before the run and wrote down with its rationale; one in ten is a common starting point, not a guarantee of sufficiency. A rate above the threshold is a signal to investigate the judge, the rubric or the sample before trusting recent scores; call it drift only when the rate rose against the previous verification. Repeat verification whenever the prompt, the model or the retrieval index changes.

Synthetic rows are for practice: they teach a team what good and bad look like before real traffic exists. A release decision rests on real traces.

## Release-gate integration

- The limits block becomes rows in the launch-gate criteria of `pm-phase-deliver/references/metric-quality-guardrails.md`; the release gate reads pass rate and hazard rows, not a demo.
- The scenario sheet is linked from the Success metrics section of the PRD and the hazard list from its Risks (`pm-phase-develop/references/prd-writing.md`).
- Instrumentation records the events the eval needs after launch: inference called, source cited, fallback triggered, user rating (`pm-phase-develop/references/tracking-plan-design.md`).
- Every production failure becomes a new golden row before the fix ships; the set grows with the product.
- The iteration loop in `SKILL.md` re-runs the golden set on every prompt or model change and re-verifies the judge.

## Common anti-patterns

- **Threshold-less eval.** Dimensions and scores with no number that decides ship or hold.
- **Dataset with no failure.** A set of happy paths proves the harness runs, not that the product is safe.
- **Numbers copied as rules.** Four hazards, twenty rows, thirty cases, one in ten: starting points from a worked example treated as guarantees of sufficiency.
- **A fifth dimension before one number.** Taxonomy standing in for a decision.
- **Demo as evidence.** Twelve hand-picked examples standing in for traffic.
- **Synthetic-only release.** Practice rows deciding a launch.
- **Judge trusted blind.** A model or a rubric scoring thousands of rows that no human has re-graded since the last prompt change.
- **Eval file not versioned with the prompt.** A pass rate nobody can reproduce because the rules moved.

## Source

Method adapted from Dean Peters, *Evals for Product Managers* (https://github.com/deanpeters/evals-for-product-managers, CC BY-NC-SA 4.0). This file is original text: it paraphrases the approach, uses this repository's own templates and reproduces none of that repository's wording.

## Files

Scenario sheet → `.ai/memory/projects/<slug>/evals/<feature>/scenario.md`. Golden set → `.ai/memory/projects/<slug>/evals/<feature>/golden-set.csv`, or a shared sheet linked from there. Decision rule → also in `decisions.md`. Hazard changes → logged with `memory.py log`.
