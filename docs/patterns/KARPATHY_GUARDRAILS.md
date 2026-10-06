# Karpathy Guardrails

Behavioral rules to reduce common LLM engineering mistakes.

## Core failures to avoid

- silent assumptions
- overcomplicated code and APIs
- speculative abstractions
- hidden tradeoffs
- vague success criteria
- changes wider than the task requires

## Operating rules

### Resolve material uncertainty
Check available sources first. If materially different outcomes remain, ask before the dependent change; state and proceed on low-risk reversible assumptions inside the request.

### Prefer the boring solution
Use the simplest approach that satisfies the requirement and fits the existing system.

### Do not optimize imaginary futures
Add flexibility for a demonstrated need. A second real use is a useful reuse signal, not a prerequisite for justified security, capacity, or operational requirements.

### Use explicit success criteria
Translate substantial work into outcomes that can be checked. Do this internally for clear, routine tasks; explain criteria when they affect a decision or review.

### Keep the diff surgical
Unrelated cleanup can wait unless it blocks the task.

### Show tradeoffs honestly
A good recommendation includes cost, benefit, and risk.

## Self-check before shipping

- Did I solve the asked problem?
- Did I add anything not requested?
- Could this be smaller?
- Did I verify it in reality?
- Did I document the decision that future-me will forget?
