# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: Artefact anchors and punctuation-variant regression for the six new blocks

Round 3 of PR #21, finding 1: the six new assertion blocks now require artefacts a keyword list cannot supply (a URL, HogQL text or insight id as the source; an analytics/<file>.md path for persistence; at least two of the weekly numbers; the behaviour-split query with its cohorts; the evidence gap phrased as a question with an owner role; a lens name next to its no-objection verdict with a reason that never crosses a semicolon; the PRD as the object of the kickoff decision; a participant plus a verb in the counter-evidence and saturation checks; role, verb and object for who builds what). test_grade_evals derives four punctuation variants (semicolon, comma, newline, and) of every keyword-only fixture and requires each at or below 0.34; the owner's semicolon variant of the adoption fixture drops from 6/7 to 2/7. Validation: test_grade_evals 118 fixtures, 24 variants, 6 strict pairs, 42/42 covered; full REPO_HEALTH battery green.

## 2026-09-11: Round 2 closing: review section, B40 candidate, recounts

Round 2 of PR #21 closed: backlog gained the 'Revisão da PR #21' section mapping the owner's seven points to the follow-up commits, the B40 candidate (54 of 79 pre-batch assertion blocks pass a keyword-only reply; the six new blocks were rewritten, the old ones are next), recounted totals (85 evals, 32 pairs with 6 strict, 118 fixtures, 42/42 covered, mirrors 138, suites hooks 33, contract 9, memory 48, context 11, recorder 6, runner 12, labels 12, validator 54, frontmatter 5); tasks updated; README describes the strict fixture pairs. Validation: validate_repo both parsers, doctor, git diff --check.

## 2026-09-11: Review panel selects lenses by risk and names the ones not run

B36 revised after the owner's review of PR #21: the review panel selects lenses by the exposure the artefact touches (exposure-to-lens table in review-panel.md) instead of running five as a ritual, every lens not run is named in the report with a one-line reason, an author's request to skip a lens because it might object is the reason to run it, and a 'ritual panel' anti-pattern was added; sub-skill 4, the WORKFLOW shadow-gate sentence, the progressive-loading row, root SKILL and README blurbs and the backlog say risk-selected instead of five-lens. The adversarial eval (M3) already requires the commercial objection to name the omitted 62% discount exposure. Validation: validate_repo both parsers, test_grade_evals 118, mirrors synced; full REPO_HEALTH battery green.

