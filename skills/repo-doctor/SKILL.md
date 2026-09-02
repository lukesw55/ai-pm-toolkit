---
name: repo-doctor
description: Read-only health check for this workspace. Use before committing changes under skills/, hooks/, .claude/, or .codex/, when validating skills/hooks/memory consistency, or when the user asks "valida o repo", "checa as skills", "tem ref quebrada?", "algum binário grande?", "repo lint", "repo-doctor". Verifies stage aliases, memory skeleton, real path references, large files (working tree + git history), hooks cited in docs, skill frontmatter, and tracked-vs-ignored local artifacts. Reports findings only — never edits, deletes, or touches the remote.
---

# repo-doctor

Read-only consistency check for this PM workspace. Run the checks below, then emit the findings table. Never edit, delete, or run anything that touches the git remote.

## Checks

Run each from the repo root. Treat any surprising result as a finding.

1. **Stage schema** — `python3 scripts/validate_context.py` (exit 0 = ok) and `python3 scripts/advance_stage.py --list`. Confirm `active-context.md` resolves to a canonical stage; flag a raw `discover` that is not being aliased to `discovery`.
1b. **Memory caps** — `python3 scripts/memory.py doctor` (exit 0 = ok). Flags: pointer over 2 KB, more or fewer than one ACTIVE block, missing `Current stage:`, parked slugs without a `projects/` dir or `state.md`, changelogs holding more than 3 entries, warm files (`changelog.md`, `session-kickoff.md`, `state.md`, `profile.md`, `decisions.md`) over their soft caps (distill candidates), pending `.distill/` packages, and PII-named project dirs the scripts skip.
2. **Memory skeleton versioned** — `git status --short --ignored .ai/memory` should show `_templates/*` and `active-context.example.md` as versionable while real memory stays ignored. Confirm with `git check-ignore -v .ai/memory/active-context.md .ai/memory/projects .ai/memory/inbox.md .ai/memory/index.md` (no real memory leaking into git).
3. **Real path references** — for each `references/...md` or sibling-relative `../<skill>/...md` path mentioned in any `SKILL.md` under `skills/`, confirm the target file exists relative to the file that cites it (not a fixed depth — a `SKILL.md` and a `references/*.md` file resolve `../` differently). Resolve the path before flagging (a sibling skill's `references/` dir is valid). This is the corrected check: do not flag a skill just because its own folder lacks a `references/` dir. `python3 scripts/validate_repo.py` automates the backtick and markdown-link forms of this check (`check_backtick_paths`, `check_markdown_links`); the manual pass here covers what the regex skips — bare filenames and paths embedded in prose.
4. **Large files** — working tree: `find . -type f -size +5M -not -path './.git/*'`. History: `git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' | awk '/^blob/{print $2,$3}' | sort -rn | head`. Flag big blobs and note whether they are in the working tree, history, or both.
5. **Hooks cited vs present** — for every `*.sh` named in `CLAUDE.md`, `AGENTS.md`, `.claude/settings*.json`, and `.codex/hooks.json`, confirm the file exists under `hooks/`.
6. **Skill frontmatter** — every `skills/*/SKILL.md` has a YAML frontmatter block with `name` and `description`.
7. **Local artifacts ignored** — `git status --short` shows no large untracked junk; `git check-ignore` covers `*.deb`, `**/node_modules/`, and `.ai/memory/projects/**/.browser-profile/`.
8. **Mirror parity** — `python3 scripts/sync_skills.py --check` exits 0; `skills/`, `.claude/skills/`, and `.agents/skills/` are byte-identical (excluding `workspace/`).

## Guardrails

- Read-only. Never `Edit`/`Write`/`rm`, never `git push`/`filter-repo`/`rebase`, never delete memory.
- Cite a `path` or the exact command output for every finding.
- Suggest a fix; do not apply it.

## Output contract

```
| Severity | Area | Finding | Path / command | Suggested fix |
|----------|------|---------|----------------|---------------|
```

Severity = Alta / Média / Baixa. End with a one-line verdict: clean, or N findings (M Alta).
