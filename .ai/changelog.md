# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-16: B42: backlog, decision and tasks

The backlog entry states the diagnosis rather than the feature: the signal existed since B32 and the rule since B33, and what was missing was the path between the signal and the change. It records what the two scripts do, the five categories and their precedence, the three files nothing in the loop writes, why the candidate is a slot replacement, the asymmetry between negative and positive fixtures, and the decision to leave memory.py doctor blind to the new tree with its narrow follow-up scope. Three entries join the rejected-frameworks list, because what was deliberately not built is the load-bearing part here: automatic insertion of a proposed fixture, a staging state inside the fixtures file, and an LLM judging the toolkit's own evals. The DECISIONS row is the one a future session has to read before automating any of this.

## 2026-09-16: B42: the validator skips generated proposals, not the tree they live in

A proposal quotes a recorded model output verbatim, and that text can carry a backticked path that never existed, or one under skills/*/workspace/, which is gitignored and absent on every other clone. Both documentation checks would then fail for everyone on a dated record of one run. GENERATED_RECORDS scopes the skip to docs/benchmarks/<iteration>/proposals/ only; a report.md or a labels file in the same tree stays checked, because those are live contracts. The generator already keeps workspace paths out of backticks, so this is the second layer rather than the first: the first is that the proposal writes the path bare and inside a fenced block. Five cases in test_validate_repo.py pin the boundary, two inside the skip and three outside it.

## 2026-09-16: B42: the proposal loop in EVAL_PROTOCOL.md

A new section between Grade and report and the runbook: what propose reads, the five categories and what each one asks of a human, the rule that a proposal exists only because someone wrote a verdict and a reason, the three files nothing in the loop may write, why no regex is generated, why the candidate is a slot replacement rather than a second object, and the asymmetry that decides whether the loop hardens the grader or corrupts it. It also says what check reports and what a green run does and does not mean, why excerpts are bounded given that the workspace is gitignored and docs are tracked, and where the product-side golden set lives instead. It closes by saying no iteration has been recorded yet, so the loop has been exercised against synthetic runs only, in the same register the protocol already uses for the pilot.

