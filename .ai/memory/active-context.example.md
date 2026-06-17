# Active Context

> Pointer only (cap 2 KB). Full state per project: `projects/<slug>/state.md`. History: `projects/<slug>/changelog.md` (+ `changelog-archive.md`). Never paste session history here; use `scripts/memory.py park|activate|log`.

## ACTIVE: `example-initiative` (set 2026-01-01)

- **Project**: Example Initiative
- **Slug**: `example-initiative`
- **Current stage**: discovery
- Read FIRST on resume: `projects/example-initiative/state.md`, then `session-kickoff.md`
- Next: [the one next action for the session]

## Parked / closed (1 line each; detail in `projects/<slug>/state.md`)

- `another-project`: develop; parked 2026-01-01; one-line hook on where it stopped

<!--
Schema contract (read by scripts/ and .claude/hooks/):
- `Current stage` must be a canonical slug from scripts/advance_stage.py STAGES
  (discovery-prioritization, impact-brief, discovery, one-pager,
  product-prioritization, prd, tech-kickoff, delivery). Legacy alias `discover`
  is accepted and normalised to `discovery`.
- `Slug` is matched by .claude/hooks/check-project-isolation.sh to scope edits to
  the active project's memory.
- `Project` is surfaced by scripts/stage_context.py on every turn.
- The whole file is capped at 2 KB (scripts/memory.py doctor enforces); session
  history goes to projects/<slug>/state.md via `memory.py park`, never here.
The real active-context.md is gitignored (it carries live customer/project context).
This redacted example is the versioned skeleton a fresh clone bootstraps from.
-->
