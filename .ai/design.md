# Legacy design location

Project-specific design now lives in `.ai/memory/projects/<slug>/design.md`, resolved from the active pointer. New projects use the template in `.ai/memory/_templates/design.md`.

Existing users: explicitly copy legacy content into the correct project with `python3 scripts/init_context.py --migrate-legacy <project-name>`. Sources are retained and existing destinations are never overwritten.
