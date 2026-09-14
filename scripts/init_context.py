#!/usr/bin/env python3
from __future__ import annotations

import argparse
from context_paths import ORG_DIR_NAME, ORG_FILES, project_path, pointer_slug

import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / ".ai" / "memory"
PROJECTS = MEMORY / "projects"
TEMPLATES = MEMORY / "_templates"
ORG = MEMORY / ORG_DIR_NAME
ORG_TEMPLATES = TEMPLATES / "org"

# destination -> template under _templates/; tests derive the expected file set from this map
PROJECT_FILES = {
    "app.md": "app.md",
    "design.md": "design.md",
    "tasks.md": "tasks.md",
    "profile.md": "context-profile.md",
    "decisions.md": "decision-log.md",
    "experiments.md": "experiment-log.md",
    "glossary.md": "glossary.md",
    "retrospective.md": "retrospective.md",
    "state.md": "state.md",
    "session-kickoff.md": "session-kickoff.md",
    "insights.md": "insights.md",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("Context name must contain at least one letter or number.")
    return slug


def render_template(name: str, slug: str, title: str) -> str:
    text = (TEMPLATES / name).read_text(encoding="utf-8")
    return (
        text.replace("{{slug}}", slug)
        .replace("{{title}}", title)
        .replace("{{date}}", date.today().isoformat())
    )


def append_if_missing(path: Path, line: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if line not in existing:
        with path.open("a", encoding="utf-8") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write(line + "\n")


def init_org() -> int:
    """Create the shared org layer from _templates/org/ without overwriting anything."""
    # Confinement before anything is created: a symlinked ancestor would send the four
    # files outside the repository while org/ itself does not exist yet, so the check
    # cannot wait for ORG.exists(). Same policy as context_paths.project_path.
    for path in (MEMORY, ORG):
        if path.is_symlink() or path.resolve() != path.absolute():
            print(f"init_context.py: {path.relative_to(ROOT).as_posix()} must not be, or sit behind, a symlink", file=sys.stderr)
            return 1
    missing = [name for name in ORG_FILES if not (ORG_TEMPLATES / name).is_file()]
    if missing:
        print(f"init_context.py: missing template .ai/memory/_templates/org/{missing[0]}", file=sys.stderr)
        return 1
    ORG.mkdir(parents=True, exist_ok=True)
    created, kept = [], []
    for name in ORG_FILES:
        target = ORG / name
        if target.is_symlink():
            print(f"init_context.py: {target.relative_to(ROOT).as_posix()} must not be a symlink", file=sys.stderr)
            return 1
        if target.exists():
            kept.append(name)
            continue
        target.write_text(render_template(f"org/{name}", ORG_DIR_NAME, "Shared org context"), encoding="utf-8")
        created.append(name)
    print(f"Initialized org context at {ORG.relative_to(ROOT).as_posix()} "
          f"(created: {', '.join(created) or 'none'}; kept: {', '.join(kept) or 'none'})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a project, or the shared org layer, without overwriting state.")
    parser.add_argument("--migrate-legacy", action="store_true", help="copy legacy app/design/tasks into missing project files; keep sources")
    parser.add_argument("--org", action="store_true", help="create the shared org layer .ai/memory/org/ from _templates/org/ without overwriting")
    parser.add_argument("name", nargs="*")
    args = parser.parse_args()
    if args.org:
        code = init_org()
        if code or not args.name:
            return code
    if not args.name:
        parser.error("a project name is required unless --org is given")
    title = " ".join(args.name).strip()
    try:
        slug = slugify(title)
        project_dir = project_path(PROJECTS, slug)
    except ValueError as exc:
        print(f"init_context.py: {exc}", file=sys.stderr)
        return 1

    # Guard the hot pointer: memory.py activate refuses to switch while a
    # project is ACTIVE, and init must not clobber what activate protects —
    # the ACTIVE block and the parked/closed list would be lost.
    active_context = MEMORY / "active-context.md"
    if active_context.exists():
        pointer = active_context.read_text(encoding="utf-8", errors="replace")
        try:
            current = pointer_slug(pointer)
        except ValueError as exc:
            print(f"init_context.py: {exc}", file=sys.stderr)
            return 1
        if current and current != slug:
            print(f"Refusing to overwrite active-context.md: '{current}' is still active; park it first", file=sys.stderr)
            return 2

    missing = [t for t in PROJECT_FILES.values() if not (TEMPLATES / t).is_file()]
    if missing:
        print(f"init_context.py: missing template .ai/memory/_templates/{missing[0]}", file=sys.stderr)
        return 1

    project_dir.mkdir(parents=True, exist_ok=True)

    files = PROJECT_FILES

    # Validate all destinations before creating files, including symlink targets.
    try:
        for output_name in (*files, "changelog.md"):
            project_path(PROJECTS, slug, output_name)
    except ValueError as exc:
        print(f"init_context.py: {exc}", file=sys.stderr)
        return 1
    for output_name, template_name in files.items():
        output_path = project_dir / output_name
        if not output_path.exists():
            legacy = ROOT / ".ai" / output_name
            content = render_template(template_name, slug, title)
            if args.migrate_legacy and output_name in ("app.md", "design.md", "tasks.md") and legacy.is_file():
                legacy_content = legacy.read_text(encoding="utf-8")
                if not legacy_content.startswith(("# Legacy ", "# Toolkit tasks")):
                    content = legacy_content
            output_path.write_text(
                content,
                encoding="utf-8",
            )

    # Warm-layer seed: memory.py log creates this on first entry, but the
    # pointer tells readers to open it on resume, so it must exist from day 0.
    changelog = project_dir / "changelog.md"
    if not changelog.exists():
        changelog.write_text(f"# {title}\n\n", encoding="utf-8")

    if not active_context.exists():
        active_context.write_text(
            "\n".join(
                [
                    "# Active Context",
                    "",
                    "> Pointer only (cap 2 KB). Full state per project: `projects/<slug>/state.md`. History: `projects/<slug>/changelog.md` (+ `changelog-archive.md`). Never paste session history here; use `scripts/memory.py park|activate|log`.",
                    "",
                    f"## ACTIVE: `{slug}` (set {date.today().isoformat()})",
                    "",
                    f"- **Project**: {title}",
                    f"- **Slug**: `{slug}`",
                    "- **Current stage**: discovery",
                    f"- Read FIRST on resume: `projects/{slug}/state.md`, then `projects/{slug}/session-kickoff.md`",
                    "- Next: Fill in the project profile, capture discovery notes, and define the first testable wedge.",
                    "",
                    "## Parked / closed (1 line each; detail in `projects/<slug>/state.md`)",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    elif pointer_slug(active_context.read_text(encoding="utf-8")) is None:
        from memory import cmd_activate
        cmd_activate(argparse.Namespace(slug=slug, stage=None, name=title))

    index = MEMORY / "index.md"
    append_if_missing(index, f"- `{slug}` — {title} (`.ai/memory/projects/{slug}/`)")

    print(f"Initialized context '{title}' at {project_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
