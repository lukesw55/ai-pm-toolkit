# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: B31 matcher review correction

PR #20 review: separate Claude exact-name/list matcher semantics from Codex regex semantics. Pass the harness through contract validation and test partial names, comma lists, alternation and anchors.

## 2026-09-10: B31 pontas soltas da execução consolidada

B31: pontas soltas da execução consolidada (PRs #16 a #19). Actions fixadas por SHA completo; cobertura de fixtures NC/adversarial derivada dos manifests, com 7 fixtures novas (39/39 blocos cobertos, 94 fixtures); código morto removido e semântica de matcher dos harnesses no validador; name do SKILL.md igual ao diretório; regressões novas no contrato de hooks e no frontmatter; README, REPO_HEALTH e AGENTS.md alinhados com as suítes reais; travessão literal no adapter Codex; título default do log derivado da entrada. Validação local em Python 3.11: preflight, py_compile, bash -n por hook, 132 espelhos, validador verde com e sem PyYAML, hooks 33, contrato 8, grader 94, memória 41, contexto 8, gravador 5, validador 54, frontmatter 5, smoke do grader exit 0, doctor verde.

## 2026-09-10: Remaining backlog implementation

Implemented B24, B22, B28, B26, B27 and B30 in one consolidated change. Added B25 recorder and protocol; the real 60-output pilot remains pending because authenticated Claude Code and Codex runners are unavailable. B21 and B23 recorded as already integrated. Validation results are recorded in the PR; binding decisions are in docs/DECISIONS.md.

