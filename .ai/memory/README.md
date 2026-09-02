# Memory

This folder stores durable context that should survive chat sessions and project switching.

## Rule of thumb

- raw notes can go to `inbox.md` (manual scratch; no script reads or writes it)
- durable context goes into project memory under `projects/<slug>/`; stakeholder notes default to `projects/<slug>/stakeholders.md`
- active focus is always reflected in `active-context.md`

Use `python3 scripts/init_context.py <project-name>` to create a new project memory folder.
