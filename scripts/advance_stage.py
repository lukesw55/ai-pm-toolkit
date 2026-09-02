#!/usr/bin/env python3
"""
advance_stage.py — Update the current workflow stage in .ai/memory/active-context.md.

Usage:
    python3 scripts/advance_stage.py <stage-slug>
    python3 scripts/advance_stage.py --next
    python3 scripts/advance_stage.py --list

Valid stages (in default order):
    discovery-prioritization → impact-brief → discovery → one-pager
    → product-prioritization → prd → tech-kickoff → delivery
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

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

# Legacy slugs that map onto a canonical stage above.
STAGE_ALIASES = {
    "discover": "discovery",
}


def read_current_stage(text: str) -> str | None:
    match = re.search(
        r"^(\s*-?\s*\*{0,2}Current\s+stage\*{0,2}\s*:\s*)([A-Za-z0-9\-_]+)",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    if not match:
        return None
    stage = match.group(2).strip().lower()
    return STAGE_ALIASES.get(stage, stage)


def set_stage(text: str, stage: str) -> str:
    today = date.today().isoformat()
    updated = re.sub(
        r"^(\s*-?\s*\*{0,2}Current\s+stage\*{0,2}\s*:\s*).+$",
        rf"\g<1>{stage}",
        text,
        count=1,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    if updated == text:
        # "Current stage" field missing — try to replace legacy "Current phase"
        updated = re.sub(
            r"^(\s*-?\s*\*{0,2}Current\s+)phase(\*{0,2}\s*:\s*).+$",
            rf"\g<1>stage\g<2>{stage}",
            text,
            count=1,
            flags=re.MULTILINE | re.IGNORECASE,
        )

    if updated == text:
        # Still no replacement — append at the top of the body
        inject = f"- **Current stage**: {stage}\n"
        lines = text.splitlines(keepends=True)
        if lines and lines[0].startswith("#"):
            insert_at = 1
            while insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            lines.insert(insert_at, inject)
            updated = "".join(lines)
        else:
            updated = inject + text

    # Bump "Last updated" date if present
    updated = re.sub(
        r"(\*{0,2}Last updated( by)?\*{0,2}\s*:\s*).*$",
        rf"\g<1>advance_stage.py on {today}",
        updated,
        count=1,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    updated = re.sub(
        r"(\*{0,2}Date\*{0,2}\s*:\s*).*$",
        rf"\g<1>{today}",
        updated,
        count=1,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Advance the workflow stage.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("stage", nargs="?", help="Stage slug to set")
    group.add_argument("--next", action="store_true", help="Advance to the next stage in sequence")
    group.add_argument("--list", action="store_true", help="List valid stages and exit")
    args = parser.parse_args()

    if args.list:
        print("Valid stages (in default order):")
        for i, stage in enumerate(STAGES, 1):
            print(f"  {i}. {stage}")
        return 0

    repo_root = Path(__file__).resolve().parent.parent
    ctx_path = repo_root / ".ai" / "memory" / "active-context.md"
    if not ctx_path.exists():
        print(f"error: {ctx_path} not found", file=sys.stderr)
        return 2
    text = ctx_path.read_text(encoding="utf-8")

    current = read_current_stage(text)

    if args.next:
        if current is None:
            target = STAGES[0]
        elif current not in STAGES:
            print(f"error: current stage '{current}' not in known list; set explicitly", file=sys.stderr)
            return 2
        else:
            idx = STAGES.index(current)
            if idx == len(STAGES) - 1:
                print(f"already at final stage: {current}")
                return 0
            target = STAGES[idx + 1]
    else:
        target = args.stage.strip().lower()
        target = STAGE_ALIASES.get(target, target)
        if target not in STAGES:
            print(
                f"error: '{target}' is not a valid stage. Run --list to see the valid set.",
                file=sys.stderr,
            )
            return 2

    new_text = set_stage(text, target)
    if new_text == text:
        print(f"no change — stage already {target}")
        return 0
    ctx_path.write_text(new_text, encoding="utf-8")

    print(f"stage: {current or '(unset)'} → {target}")
    print(f"updated: {ctx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
