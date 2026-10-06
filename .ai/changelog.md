# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-10-06: Finalize response and memory guidance

Finalized proportional response and memory guidance; synchronized skill mirrors and completed required validation.

## 2026-10-06: Evidence-aware autonomy and calibrated memory use

Aligned instructions, agents and memory references with evidence-aware autonomy; expanded inference evals with routine-edit positive control. Validation passed: full docs/REPO_HEALTH suite, 86 evals/713 fixtures, mirror parity, validator and hook tests. Pilot dry-run planned 30 calls and executed none; no live model benchmark.

## 2026-09-30: Restored both README diagrams in PR #28 at the owner requ...

Restored both README diagrams in PR #28 at the owner request. Preserved the eight-stage pipeline and evidence feedback loops; revised the interaction flow to place PreToolUse checks before configured tool operations and Stop checks at reply completion. Memory logging remains agent-driven and its reminder nonblocking. Both Mermaid diagrams rendered in a local Chrome preview. The full 20-command CONTRIBUTING.md battery passed on Ubuntu/WSL Python 3.12.3. No runtime code or hook configuration changed.

