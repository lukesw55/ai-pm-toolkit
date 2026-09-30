# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-30: Restored both README diagrams in PR #28 at the owner requ...

Restored both README diagrams in PR #28 at the owner request. Preserved the eight-stage pipeline and evidence feedback loops; revised the interaction flow to place PreToolUse checks before configured tool operations and Stop checks at reply completion. Memory logging remains agent-driven and its reminder nonblocking. Both Mermaid diagrams rendered in a local Chrome preview. The full 20-command CONTRIBUTING.md battery passed on Ubuntu/WSL Python 3.12.3. No runtime code or hook configuration changed.

## 2026-09-30: Reviewed PR #28 against main 415b246 and reproduced its C...

Reviewed PR #28 against main 415b246 and reproduced its CI failure at dbb9e8f: the README cited a generic reference path as a real file. Replaced it with a link to the discovery reference map, keeping all validation checks intact. The 20-command CONTRIBUTING.md battery passed on Ubuntu/WSL with Python 3.12.3, including 93 validator cases. Native Windows/Python 3.13.14 ran the validator regression suite with eight failures involving backslash path messages; no live harness session was tested. Formal approval requires another account because the authenticated account is the PR author.

## 2026-09-30: README entry point and validation contract

Applied the owner-approved README (1,277 words, down from 4,568). Revised its validation contract: title and essential local documentation links required; inventories and contents optional; recognised numeric claims still match the tree; README Markdown heading anchors checked. Updated the regressions, contribution and health documentation, and recorded the policy superseding B43. The full CONTRIBUTING.md battery passed locally on Python 3.12.14, including both validator modes, 93 validator regressions, hook and memory checks, grader fixtures and the pilot dry run. No live Claude Code/Codex session was tested. No commit, PR or publication.

