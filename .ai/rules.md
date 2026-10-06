# Instructions

This repository is Umberto, a reusable toolkit for product and engineering work across projects. Its canonical skills and shared hooks live at the repository root; Claude Code and Codex use generated skill mirrors.

## Context and sources

- Project-specific context lives under `.ai/memory/projects/<slug>/` and is selected by `.ai/memory/active-context.md`.
- Resolve the active slug before reading project files. Read app, design, tasks, decisions, and state only as relevant. Unfilled fields are unknown.
- `.ai/app.md` and `.ai/design.md` are legacy migration guides, not current project definitions. Use `docs/memory/MEMORY_SYSTEM.md` for non-destructive migration or bootstrap when the task requires project memory.
- `.ai/backlog.md` tracks toolkit implementation status; `.ai/changelog.md` records toolkit changes. Project tasks and changelogs belong under that project's memory.
- Before substantial toolkit work, read the relevant changelog/backlog entries and `docs/DECISIONS.md`; project work uses that project's relevant memory instead.
- This repo also contains GitHub Copilot-style agents under `.github/agents/`.

## Working rules

- Identify a Double Diamond stage for product work when it helps choose the next step; do not force stages onto simple answers or clear maintenance.
- Test material premises. Verify uncertain facts with available sources before asking the user. State low-risk, reversible assumptions and proceed when they stay inside the request.
- Ask when materially different outcomes remain, an essential unknown blocks the work, constraints conflict, or the next action needs authorization not already given.
- Keep user reports, preferences, evidence, assumptions, and verified facts distinct when the difference matters. User approval accepts an action or risk; it does not establish an external fact.
- Prefer the smallest reversible move that can produce evidence. Add abstractions or platform work for a demonstrated requirement, including security, capacity, or operational needs; a second use case is a reuse signal, not an absolute prerequisite.
- Use verification-first thinking proportionate to task risk. Run the narrowest useful check after a meaningful change.
- When touching user-facing UX, follow the project's design guidance when present and use clear, recovery-oriented error copy.
- Update project memory when durable project context changes. Update toolkit backlog/changelog for toolkit work when its status or history changes. A read-only answer with no durable change needs no log.
- Keep changes small and reviewable. State material trade-offs; do not create process artefacts just to show activity.
- Use Lean by default; use Standard when nuance matters and Caveman only when requested or clearly useful.
