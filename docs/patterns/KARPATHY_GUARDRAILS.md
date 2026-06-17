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

### Name uncertainty early
If something is ambiguous, say so before implementation.

### Prefer the boring solution
Use the simplest approach that satisfies the requirement and fits the existing system.

### Do not optimize imaginary futures
Only add flexibility when a second real need appears.

### Use explicit success criteria
Translate requests into outcomes that can be checked.

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
