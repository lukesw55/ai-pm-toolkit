#!/usr/bin/env python3
"""
sync_skills.py — regenerate the two harness-discovery mirrors from the
canonical skill tree.

Canonical source: skills/ (skill directories + WORKFLOW.md + DOCTRINE.md).
Mirrors (generated, committed, never hand-edited):
    .claude/skills/   — Claude Code skill discovery
    .agents/skills/    — Codex skill discovery

Both mirrors are deterministic byte-for-byte copies of the canonical tree,
excluding local/regenerable artefacts (workspace/, __pycache__/). Because
the mirrors are committed, a fresh clone works in both harnesses with no
bootstrap step.

Usage:
    python3 scripts/sync_skills.py            # regenerate both mirrors
    python3 scripts/sync_skills.py --check     # read-only drift check;
                                                # exit 0 clean, exit 1 stale
"""

from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "skills"
MIRRORS = [ROOT / ".claude" / "skills", ROOT / ".agents" / "skills"]

EXCLUDED_DIR_NAMES = {"workspace", "__pycache__"}


def canonical_files() -> dict[str, Path]:
    """Relative path -> absolute path, for every file under skills/ that
    should be mirrored (excludes workspace/ and __pycache__ anywhere in the
    tree)."""
    out: dict[str, Path] = {}
    for p in CANONICAL.rglob("*"):
        if p.is_dir():
            continue
        if any(part in EXCLUDED_DIR_NAMES for part in p.relative_to(CANONICAL).parts):
            continue
        out[str(p.relative_to(CANONICAL))] = p
    return out


def sync(mirror: Path, files: dict[str, Path]) -> list[str]:
    """Make mirror byte-identical to the canonical file set. Returns a list
    of change descriptions (empty if nothing changed)."""
    changes = []
    mirror.mkdir(parents=True, exist_ok=True)

    # Write/update every canonical file.
    for rel, src in files.items():
        dst = mirror / rel
        if dst.exists() and filecmp.cmp(src, dst, shallow=False):
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        changes.append(f"wrote {dst.relative_to(ROOT)}")

    # Remove anything in the mirror that isn't canonical anymore.
    canonical_rels = set(files)
    for p in sorted(mirror.rglob("*"), reverse=True):
        rel = str(p.relative_to(mirror))
        if p.is_dir():
            if not any(f.startswith(rel + "/") for f in canonical_rels) and rel not in canonical_rels:
                try:
                    p.rmdir()
                except OSError:
                    pass
            continue
        if rel not in canonical_rels:
            p.unlink()
            changes.append(f"removed {p.relative_to(ROOT)}")

    return changes


def check(mirror: Path, files: dict[str, Path]) -> list[str]:
    """Read-only: report every way `mirror` differs from the canonical file
    set. Empty list means identical."""
    problems = []
    canonical_rels = set(files)
    mirror_rels = set()
    if mirror.exists():
        for p in mirror.rglob("*"):
            if p.is_file():
                mirror_rels.add(str(p.relative_to(mirror)))

    for rel in sorted(canonical_rels - mirror_rels):
        problems.append(f"MISSING in {mirror.relative_to(ROOT)}: {rel}")
    for rel in sorted(mirror_rels - canonical_rels):
        problems.append(f"EXTRA in {mirror.relative_to(ROOT)}: {rel}")
    for rel in sorted(canonical_rels & mirror_rels):
        if not filecmp.cmp(files[rel], mirror / rel, shallow=False):
            problems.append(f"DIFFERS: {rel} (canonical vs {mirror.relative_to(ROOT)})")
    return problems


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    files = canonical_files()
    if not files:
        print("sync_skills: no canonical files found under skills/ — nothing to do", file=sys.stderr)
        return 1

    if check_only:
        problems = []
        for mirror in MIRRORS:
            problems.extend(check(mirror, files))
        if problems:
            for p in problems:
                print(p)
            print(f"\nsync_skills --check: {len(problems)} drift issue(s) — run `python3 scripts/sync_skills.py`")
            return 1
        print(f"sync_skills --check: {len(MIRRORS)} mirror(s) match canonical ({len(files)} files)")
        return 0

    total_changes = 0
    for mirror in MIRRORS:
        changes = sync(mirror, files)
        total_changes += len(changes)
        for c in changes:
            print(c)
    if total_changes == 0:
        print(f"sync_skills: {len(MIRRORS)} mirror(s) already up to date ({len(files)} files)")
    else:
        print(f"sync_skills: {total_changes} change(s) applied across {len(MIRRORS)} mirror(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
