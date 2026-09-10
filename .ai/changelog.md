# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: session log

B31: added scripts/run_eval_pilot.py (pilot runner: builds the without_skill and with_skill payloads from docs/benchmarks/pilot-deps.json with sha256 per loaded file, runs the harness CLI in a fresh directory outside the repo with the payload on stdin, randomises the config order per eval from a printed seed, parses the Claude Code JSON envelope and the Codex event stream, refuses empty output, mixed harness, dirty tree and already-recorded runs, records through record_eval_run.record() and writes a provenance.json sidecar), the dependency manifest, and scripts/test_run_eval_pilot.py with a fake harness (9 tests: 30 recorded runs graded end to end, seeded order, empty output, mixed harness, resume, dirty tree, dry run, codex stream, bad envelopes). Claude Code flags confirmed against claude -p --help 2.1.267; Codex template to be verified on the pilot machine. Validation: tests, dry run, validate_repo both parsers.

## 2026-09-10: session log

B37: added skills/pm-transversal-analysis/references/batch-interview-synthesis.md (shared codebook first, one excerpt log per transcript, fan-out where the harness offers subagents with a sequential fallback, merge by participants with counter-evidence, saturation and recency checks, PII kept in raw-evidence) and references/connector-task-recipes.md (recipe contract plus launch retro from Jira tickets, feature adoption from analytics, behaviour-split retention; numbers only from tool results, source links, persistence with query text, TBD rules), sub-skills 5 and 6, load and persist steps and the MCP integration bullet in the SKILL.md, two progressive-loading rows, root SKILL and README blurbs, the AGENTS known-degradation note, and evals 3 (standard batch synthesis) and 4 (skill-functional-adversarial: refuse the 2x retention claim no tool returned) with assertions and fixture pairs. Validation: validate_repo both parsers, test_grade_evals 99 fixtures, test_frontmatter, mirrors synced.

## 2026-09-10: session log

B36: added skills/pm-transversal-stakeholder/references/review-panel.md (five stakeholder lenses with cards, the rule that no objection is a valid output and a manufactured one is a doctrine-7 failure, panel report template, sequential default with subagent fan-out where available, consolidation into the dissent protocol and the assumption map, never a gate), sub-skill 4 and persist path in the SKILL.md, progressive-loading row, one sentence in the WORKFLOW shadow-gate paragraph, an AGENTS known-degradation note for Codex, root SKILL and README blurbs, and evals 3 (skill-functional-adversarial: hidden discount-revenue exposure) and 4 (negative-control: clean PRD cleared without an invented objection) with assertions and fixture pairs. Validation: validate_repo both parsers, test_grade_evals 95 fixtures, mirrors synced.

