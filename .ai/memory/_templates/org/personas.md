# Personas

> Shared org layer, read by any skill when the task needs company context. Not a project file: project facts live under `projects/<slug>/`, and for a project's own decisions the project files win; when project evidence contradicts this file, record the divergence in that project's `decisions.md` (what this file says, what the evidence says, who decides) and change this file only when the evidence holds beyond one project, logging it with `memory.py log`. Personal-data rule, checked rather than assumed: roles, archetypes and organisations only, never a named individual, e-mail or phone number; `memory.py doctor` warns on e-mail and phone patterns, a name is a review rule no pattern catches, and pseudonymisation lowers but does not remove re-identification risk, so people notes stay in `people/` (manual, gitignored). Versioned in a fork; the upstream toolkit ships only this template.

A persona is a job and a context, never a real person. Link evidence by locator (`<slug>/<topic>/P<NN>`), never by name. Add a persona only when discovery evidence from at least one project supports it; retire the ones the evidence stops supporting.

- **Last reviewed**: {{date}}
- **Owner role**: [Fill in]

## Persona: [Archetype, e.g. Approver in a mid-size finance team]

- **Segment**: [company size, industry, plan]
- **Job to be done**: When [situation], I want to [motivation], so I can [outcome].
- **Pains**: [pain, with locator]
- **Gains**: [what good looks like for them]
- **Buys vs uses**: [buyer, user, admin, or a mix]
- **Evidence strength**: [N participants, most recent date]
- **Last updated**: {{date}} from `<slug>`
