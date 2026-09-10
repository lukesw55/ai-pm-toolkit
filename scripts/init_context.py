#!/usr/bin/env python3
from __future__ import annotations

import argparse
from context_paths import project_path, pointer_slug

import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / ".ai" / "memory"
PROJECTS = MEMORY / "projects"
TEMPLATES = MEMORY / "_templates"


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a project without overwriting its state.")
    parser.add_argument("--migrate-legacy", action="store_true", help="copy legacy app/design/tasks into missing project files; keep sources")
    parser.add_argument("name", nargs="+")
    args = parser.parse_args()
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

    project_dir.mkdir(parents=True, exist_ok=True)

    files = {
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
    }

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
