# Memory

This folder stores durable context that should survive chat sessions and project switching.

## Rule of thumb

- raw notes can go to `inbox.md` (manual scratch; no script reads or writes it)
- durable context goes into project memory under `projects/<slug>/`; stakeholder notes default to `projects/<slug>/stakeholders.md`; ranked research themes go to `projects/<slug>/insights.md` (locators only)
- company-wide context (what we sell, personas as archetypes, competitors, cycle goals) lives in the shared layer `org/`, created by `python3 scripts/init_context.py --org`; ignored upstream, versioned in a fork, never a named person
- active focus is always reflected in `active-context.md`
- rotated and folded blocks live in the sibling `*-archive.md` files; each one carries an index block, so `python3 scripts/memory.py index <slug>` lists what the cold layer holds before any of it is opened

Use `python3 scripts/init_context.py <project-name>` to create a new project memory folder.
