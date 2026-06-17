#!/usr/bin/env python3
"""
validate_context.py — Check that .ai/memory/active-context.md carries the minimum
schema the scripts and hooks rely on.

Read-only. Prints a per-field report and exits non-zero if anything required is
missing or malformed, so it can gate before stage-aware work.

Required fields:
    Project        — surfaced by stage_context.py
    Slug           — matched by check-project-isolation.sh to scope memory edits
    Current stage  — must be a canonical stage (or the legacy alias `discover`)

See .ai/memory/active-context.example.md for the schema contract.
"""

import re
import sys
from pathlib import Path

# Keep in sync with scripts/advance_stage.py.
STAGES = [
    "discovery-prioritization",
    "impact-brief",
    "discovery",
    "one-pager",
    "product-prioritization",
    "prd",
    "tech-kickoff",
    "delivery",
]
STAGE_ALIASES = {"discover": "discovery"}


def field(text: str, name: str) -> str | None:
    match = re.search(
        rf"^\s*-?\s*\*{{0,2}}{name}\*{{0,2}}\s*:\s*`?([^`\n]+?)`?\s*$",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    ctx_path = repo_root / ".ai" / "memory" / "active-context.md"
    if not ctx_path.exists():
        print(f"FAIL: {ctx_path} not found", file=sys.stderr)
        return 2

    text = ctx_path.read_text(encoding="utf-8", errors="replace")
    problems = []

    project = field(text, "Project")
    print(f"  Project: {project or 'MISSING'}")
    if not project:
        problems.append("Project field missing (stage_context.py can't name the active project)")

    slug = field(text, "Slug")
    print(f"  Slug: {slug or 'MISSING'}")
    if not slug:
        problems.append("Slug field missing (check-project-isolation.sh can't scope edits)")

    stage_raw = field(text, "Current stage")
    stage = STAGE_ALIASES.get(stage_raw.lower(), stage_raw.lower()) if stage_raw else None
    print(f"  Current stage: {stage_raw or 'MISSING'}" + (f" (-> {stage})" if stage_raw and stage != stage_raw.lower() else ""))
    if not stage_raw:
        problems.append("Current stage field missing")
    elif stage not in STAGES:
        problems.append(f"Current stage '{stage_raw}' is not a canonical stage; run advance_stage.py --list")

    if problems:
        print("\nactive-context.md schema problems:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print("\nactive-context.md schema OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
