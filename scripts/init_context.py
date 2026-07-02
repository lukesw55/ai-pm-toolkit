#!/usr/bin/env python3
from __future__ import annotations

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
    if len(sys.argv) < 2:
        print("Usage: python scripts/init_context.py <project-name>")
        return 1

    title = " ".join(sys.argv[1:]).strip()
    slug = slugify(title)
    project_dir = PROJECTS / slug
    project_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "profile.md": "context-profile.md",
        "decisions.md": "decision-log.md",
        "experiments.md": "experiment-log.md",
        "glossary.md": "glossary.md",
        "retrospective.md": "retrospective.md",
    }

    for output_name, template_name in files.items():
        output_path = project_dir / output_name
        if not output_path.exists():
            output_path.write_text(
                render_template(template_name, slug, title),
                encoding="utf-8",
            )

    active_context = MEMORY / "active-context.md"
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
                f"- Read FIRST on resume: `projects/{slug}/state.md`, then `session-kickoff.md`",
                "- Next: Fill in the project profile, capture discovery notes, and define the first testable wedge.",
                "",
                "## Parked / closed (1 line each; detail in `projects/<slug>/state.md`)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    index = MEMORY / "index.md"
    append_if_missing(index, f"- `{slug}` — {title} (`.ai/memory/projects/{slug}/`)")

    print(f"Initialized context '{title}' at {project_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
