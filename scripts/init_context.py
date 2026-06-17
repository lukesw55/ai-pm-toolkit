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
                f"- **Project**: {title}",
                f"- **Slug**: `{slug}`",
                "- **Current stage**: discovery",
                "- **Current wedge**: [Fill this in]",
                "- **Primary metric**: [Fill this in]",
                "- **Last updated by**: init_context.py",
                f"- **Date**: {date.today().isoformat()}",
                "",
                "## Immediate next actions",
                "",
                "1. Fill in the project profile.",
                "2. Capture discovery notes.",
                "3. Define the first testable wedge.",
                "",
                f"Project folder: `.ai/memory/projects/{slug}/`",
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
