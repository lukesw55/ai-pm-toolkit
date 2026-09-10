# Legacy app location

Project-specific app now lives in `.ai/memory/projects/<slug>/app.md`, resolved from the active pointer. New projects use the template in `.ai/memory/_templates/app.md`.

Existing users: explicitly copy legacy content into the correct project with `python3 scripts/init_context.py --migrate-legacy <project-name>`. Sources are retained and existing destinations are never overwritten.
