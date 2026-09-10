# Changelog archive

> Rotated out of `changelog.md`. Full entries, verbatim.

Index (one line per archived block, file order; grep here before opening a block):
- 2026-09-08 session log
- 2026-09-08 session log
- 2026-09-08 session log

## 2026-09-08: session log

B21: validate hook routes and configuration shapes; block malformed Codex writes and gate process errors. Verified on Python 3.11 under WSL: six contract regressions and existing validator, hook, grader, memory and schema suites passed. Live harness integration not yet verified.

## 2026-09-08: session log

B23 in progress: portable typed frontmatter and invalid-result propagation implemented locally. Three new local tests and 31 existing fallback schema cases pass; cross-parser test skipped because PyYAML is unavailable in the Windows runtime. Full Linux validation is blocked by automatic approval review: workspace out of credits. B21 merged as PR #16; remaining batches and the live pilot are not complete.

## 2026-09-08: session log

B23: completed portable typed frontmatter, invalid-result propagation and explicit optional-dependency test skips. Linux validation resumed: 4 frontmatter tests, 54 schema cases and structural validation with and without PyYAML passed.

