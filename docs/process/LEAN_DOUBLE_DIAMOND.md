# Lean Double Diamond

This process adapts the classic Double Diamond to startup-speed product work.

## Why this version exists

Classic discovery models are useful, but teams often fail in one of two ways:

- they skip discovery and build the wrong thing fast
- they overdo discovery and never place a real bet

Lean Double Diamond keeps the shape of the model while forcing every phase to end in a **small, testable next move**.

## The four phases

## 1. Discover — Doing the right things

### Intent
Understand the terrain before choosing the problem.

### Questions
- Who is feeling pain?
- What job are they trying to get done?
- What evidence already exists?
- What constraints shape the solution space?
- What do we only think is true?

### Outputs
- user and stakeholder map
- pains and friction moments
- assumptions list
- evidence inventory
- opportunity list
- context dependencies

### Exit criteria
You can explain the situation without jumping to one favored solution.

## 2. Define — Still doing the right things

### Intent
Narrow the field and pick the best wedge.

### Questions
- Which problem is worth solving now?
- For which user?
- What metric tells us we improved things?
- What are we deliberately not solving?
- What is the smallest testable wedge?

### Outputs
- problem statement
- target user
- success metrics
- non-goals
- "How might we" question
- wedge definition
- experiment card

### Exit criteria
There is a clear wedge, a measurable signal, and a stop/continue rule.

## 3. Develop — Doing things right

### Intent
Explore a few credible ways to attack the wedge.

### Questions
- What are 2–4 viable approaches?
- Which one gets us evidence fastest?
- Which one is most reversible?
- What are the key technical or design risks?
- What prototype is enough?

### Outputs
- option comparison
- chosen direction and rationale
- prototype or spike plan
- risk list
- validation plan

### Exit criteria
The team has chosen a direction for clear reasons and knows how it will be tested.

## 4. Deliver — Still doing things right

### Intent
Ship the smallest useful slice and learn.

### Questions
- What is the minimum viable increment?
- What do we need to instrument or observe?
- What does release versus iterate depend on?
- What must be remembered for the next cycle?

### Outputs
- implementation slice
- verification evidence
- release decision
- learning summary
- updated memory and backlog

### Exit criteria
A validated increment is shipped or the team knowingly returns to an earlier phase.

## The lean loop inside Develop and Deliver

Run this when uncertainty is non-trivial:

1. **Hypothesis** — what do we believe?
2. **Probe** — what is the smallest thing that can test it?
3. **Test** — how will we gather evidence?
4. **Learn** — what happened?
5. **Decide** — continue, pivot, stop, or deepen
6. **Log** — record it in memory

## Artifacts to maintain

At minimum, each active project should keep:

- profile
- decisions
- experiments
- glossary
- changelog
- current tasks

## Smells that mean you skipped a phase

### Discover smell
"Users probably want..."

### Define smell
"Let's just build something and see."

### Develop smell
"We picked the first idea and stopped thinking."

### Deliver smell
"It shipped, but we do not know whether it helped."

## Good defaults

- prefer direct observation over internal opinions
- prefer reversible moves over foundational rewrites
- prefer clear metrics over vague optimism
- prefer one meaningful wedge over many half-built ideas
