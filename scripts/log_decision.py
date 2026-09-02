#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / ".ai" / "memory"
ACTIVE = MEMORY / "active-context.md"


def extract_slug() -> str:
    text = ACTIVE.read_text(encoding="utf-8")
    match = re.search(r"- \*\*Slug\*\*: `([^`]+)`", text)
    if not match:
        raise RuntimeError("Could not find active context slug in .ai/memory/active-context.md")
    return match.group(1)


def main() -> int:
    if len(sys.argv) < 3:
        print('Usage: python3 scripts/log_decision.py "<title>" "<choice>" [status]')
        return 1

    title = sys.argv[1].strip()
    choice = sys.argv[2].strip()
    status = sys.argv[3].strip() if len(sys.argv) > 3 else "accepted"

    slug = extract_slug()
    decisions = MEMORY / "projects" / slug / "decisions.md"
    decisions.parent.mkdir(parents=True, exist_ok=True)

    entry = f"""## {date.today().isoformat()} — {title}

- **Status**: {status}
- **Context**: [Why this decision was needed]
- **Choice**: {choice}
- **Tradeoffs**: [Speed vs quality, simplicity vs flexibility, etc.]
- **Follow-up**: [What to verify next]

"""

    with decisions.open("a", encoding="utf-8") as handle:
        if decisions.exists() and decisions.stat().st_size > 0:
            handle.write("\n")
        handle.write(entry)

    print(f"Appended decision to {decisions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
