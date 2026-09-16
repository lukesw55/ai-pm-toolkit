# Eval scenario — {{title}}

> The PM-owned half of an AI feature's quality contract, per `skills/pm-archetype-ai/references/eval-design.md`. The golden set beside this file is the other half. Written before the feature ships and re-read every time the prompt, the model or the retrieval changes, because all three change the answer.

- **Slug**: `{{slug}}`
- **Created**: {{date}}

## Task

[What the feature does, in one sentence, for whom.]

## User

[Who reads the output and what they do with it without checking it first. That last part is what sets the hazards.]

## Good-answer rules

[4 to 6, each testable by someone who did not write them.]

1. [...]
2. [...]

## Hazard list

[Sized to the task and the segments it serves; about four failure modes is a usual start, one line each, sayable in a meeting. At least one has to be a failure this feature has already produced, or the list is a guess.]

1. [...]
2. [...]

## Limits block

[The numbers the task needs, usually three to five, each with a one-line rationale, written before any scoring dimension and before the run.]

- at least [NN] % of golden rows graded good — because [what breaks below it]
- zero rows in [blocking hazard] — because [what one such row costs]
- 100 % of outputs carry [required element] — because [who depends on it]
- at most [NN] % of outputs [undesired behaviour] — because [what the user cannot do then]

## Decision rule

Ship when every limit holds. A single row in [blocking hazard] blocks the release regardless of the pass rate, because a critical failure is never offset by a high average.

[Record the same rule in `decisions.md`, where the rest of this project's decisions live.]

## Versions

- prompt: [id or date]
- eval file: [id or date]
- model: [id]

[The three change together. When any of them moves, re-run the golden set and verify the judge again.]
