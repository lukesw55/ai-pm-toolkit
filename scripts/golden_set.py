#!/usr/bin/env python3
"""Create, append to and check a product golden set inside a project's memory.

The golden set is the PM-owned test set for an AI feature, described in
skills/pm-archetype-ai/references/eval-design.md: real traces first, at least one failure
the team has already seen, and a new row for every production failure before the fix ships.
This script writes the two files that reference already publishes, and nothing else:

    .ai/memory/projects/<slug>/evals/<feature>/scenario.md
    .ai/memory/projects/<slug>/evals/<feature>/golden-set.csv

Every field of a row comes from a flag a person typed. The script never reads a model's
output and never fills a cell on its own: a golden row whose expected behaviour was copied
from what the model produced makes the set agree with the model, which is the same failure
the toolkit's own grader guards against one layer up.

Project memory is gitignored, so these files stay on the machine that wrote them unless a
fork versions them deliberately.

Usage:
    python3 scripts/golden_set.py init <slug> --feature ticket-summariser
    python3 scripts/golden_set.py add <slug> --feature ticket-summariser --source real-trace \\
        --locator "ticket 48213" --expected "summary cites the refund line, promises nothing" \\
        --label fail --reason "invented a refund the ticket never made" --handle hallucination \\
        --grader "support lead"
    python3 scripts/golden_set.py show <slug> --feature ticket-summariser
    python3 scripts/golden_set.py check <slug> --feature ticket-summariser
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
import io
import os
from pathlib import Path
import re
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))

from context_paths import project_path  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / ".ai" / "memory" / "projects"
TEMPLATES = ROOT / ".ai" / "memory" / "_templates" / "evals"
EVALS_DIR = "evals"
SHEET = "golden-set.csv"
SCENARIO = "scenario.md"
# The reference publishes these column names, spaces and all. A PM opens this file in a
# spreadsheet, so the header matches the sheet that reference describes rather than a
# code-friendly spelling.
HEADER = ("id", "source", "input locator", "expected behaviour", "label", "reason", "handle", "grader", "last graded")
LABELS = ("good", "weak", "fail")
SOURCES = ("real trace", "synthetic")
# Handles name the pattern, not the row. The reference says to rename them when the product
# needs other words and to keep them few, so an unknown handle is a warning, never a refusal.
HANDLES = ("golden", "approved", "reference", "exemplar", "broken logic", "hallucination",
           "bad UX", "review needed", "edge case")
FEATURE_RE = re.compile(r"[a-z0-9][a-z0-9-]*")


def feature_dir(root: Path, slug: str, feature: str) -> Path:
    """Confinement is context_paths' job: it refuses a PII slug or segment, a path that
    escapes the project, and a projects root behind a symlink."""
    if not FEATURE_RE.fullmatch(feature or ""):
        raise ValueError("feature must be lowercase letters, digits and hyphens")
    return project_path(root / ".ai" / "memory" / "projects", slug, EVALS_DIR, feature)


def sheet_path(root: Path, slug: str, feature: str) -> Path:
    return feature_dir(root, slug, feature) / SHEET


def scenario_path(root: Path, slug: str, feature: str) -> Path:
    return feature_dir(root, slug, feature) / SCENARIO


def read_sheet(path: Path) -> tuple[list[str], list[list[str]]]:
    """Validates the shape before anything is appended, so a sheet a person edited by hand
    is never half-written. Raises with path:line so the message names where to look."""
    if not path.is_file():
        raise OSError(f"no golden set at {path}; run golden_set.py init first")
    rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8"))))
    if not rows:
        raise ValueError(f"{path}:1: the file is empty; it needs the header row")
    header = rows[0]
    if tuple(header) != HEADER:
        raise ValueError(f"{path}:1: header is {header}, expected {list(HEADER)}")
    body = [row for row in rows[1:] if row]
    for number, row in enumerate(body, start=2):
        if len(row) != len(HEADER):
            raise ValueError(f"{path}:{number}: {len(row)} fields, expected {len(HEADER)}")
    seen: dict[str, int] = {}
    for number, row in enumerate(body, start=2):
        if row[0] in seen:
            raise ValueError(f"{path}:{number}: id {row[0]!r} already used on line {seen[row[0]]}")
        seen[row[0]] = number
    return header, body


def write_sheet(path: Path, header: tuple[str, ...], rows: list[list[str]]) -> None:
    """Atomic: a temp file in the same directory, then os.replace. A crash mid-write must
    not leave a half-written sheet where a full one was."""
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=path.parent, delete=False)
    try:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
        handle.close()
        os.replace(handle.name, path)
    except BaseException:
        handle.close()
        Path(handle.name).unlink(missing_ok=True)
        raise


def next_id(rows: list[list[str]]) -> str:
    numbers = []
    for row in rows:
        if not row[0].isdigit():
            raise ValueError(f"id {row[0]!r} is not a number; pass --id to say which one this row takes")
        numbers.append(int(row[0]))
    return f"{max(numbers) + 1 if numbers else 1:03d}"


def counts(rows: list[list[str]]) -> dict[str, dict[str, int]]:
    tallies: dict[str, dict[str, int]] = {"label": {}, "handle": {}, "source": {}}
    for row in rows:
        for field, position in (("label", 4), ("handle", 6), ("source", 1)):
            tallies[field][row[position]] = tallies[field].get(row[position], 0) + 1
    return tallies


def normalise_source(value: str) -> str:
    """The CLI spells it real-trace; the sheet stores the reference's words."""
    cleaned = (value or "").replace("-", " ").strip().lower()
    if cleaned not in SOURCES:
        raise ValueError(f"source must be one of {', '.join(s.replace(' ', '-') for s in SOURCES)}")
    return cleaned


def cmd_init(args, root: Path = ROOT) -> int:
    directory = feature_dir(root, args.slug, args.feature)
    project = directory.parent.parent
    if not project.is_dir():
        print(f"golden_set: unknown project slug '{args.slug}' (no {project.relative_to(root).as_posix()}/)", file=sys.stderr)
        return 1
    templates = root / ".ai" / "memory" / "_templates" / EVALS_DIR
    missing = [name for name in (SCENARIO, SHEET) if not (templates / name).is_file()]
    if missing:
        print(f"golden_set: missing template(s) {', '.join(missing)} under {templates.relative_to(root).as_posix()}/", file=sys.stderr)
        return 1
    directory.mkdir(parents=True, exist_ok=True)
    for name in (SCENARIO, SHEET):
        target = directory / name
        if target.exists():
            print(f"kept {target.relative_to(root).as_posix()}")
            continue
        text = (templates / name).read_text(encoding="utf-8")
        text = text.replace("{{slug}}", args.slug).replace("{{title}}", args.feature).replace("{{date}}", date.today().isoformat())
        target.write_text(text, encoding="utf-8")
        print(f"created {target.relative_to(root).as_posix()}")
    return 0


def cmd_add(args, root: Path = ROOT) -> int:
    path = sheet_path(root, args.slug, args.feature)
    header, rows = read_sheet(path)
    source = normalise_source(args.source)
    if args.label not in LABELS:
        raise ValueError(f"label must be one of {', '.join(LABELS)}")
    fields = {"locator": args.locator, "expected": args.expected, "reason": args.reason,
              "handle": args.handle, "grader": args.grader}
    for name, value in fields.items():
        if not (value or "").strip():
            raise ValueError(f"--{name} must not be empty")
        if "\n" in value or "\r" in value:
            raise ValueError(f"--{name} must be one line; a row that spans lines stops being greppable")
    if args.handle not in HANDLES:
        print(f"WARN handle {args.handle!r} is not one of the usual ones ({', '.join(HANDLES)}); "
              "the reference allows renaming them, so this is a note, not a refusal", file=sys.stderr)
    graded = args.last_graded or date.today().isoformat()
    try:
        date.fromisoformat(graded)
    except ValueError as exc:
        raise ValueError(f"--last-graded must be YYYY-MM-DD: {exc}") from exc
    row_id = args.id or next_id(rows)
    if any(row[0] == row_id for row in rows):
        raise ValueError(f"id {row_id!r} is already in the sheet")
    rows.append([row_id, source, args.locator.strip(), args.expected.strip(), args.label,
                 args.reason.strip(), args.handle.strip(), args.grader.strip(), graded])
    write_sheet(path, HEADER, rows)
    print(f"added row {row_id} to {path.relative_to(root).as_posix()} ({len(rows)} row(s))")
    return 0


def cmd_show(args, root: Path = ROOT) -> int:
    path = sheet_path(root, args.slug, args.feature)
    header, rows = read_sheet(path)
    tallies = counts(rows)
    print(f"{path.relative_to(root).as_posix()}: {len(rows)} row(s)")
    for field in ("label", "source", "handle"):
        if tallies[field]:
            print(f"  by {field}: " + ", ".join(f"{name} {n}" for name, n in sorted(tallies[field].items())))
    dates = sorted(row[8] for row in rows if row[8])
    if dates:
        print(f"  last graded: {dates[0]} to {dates[-1]}")
    if args.rows:
        print("")
        for row in rows:
            print(f"  {row[0]}  [{row[4]}] {row[2]} — {row[5]} ({row[1]}, {row[6]}, {row[7]}, {row[8]})")
    return 0


def cmd_list(args, root: Path = ROOT) -> int:
    directory = project_path(root / ".ai" / "memory" / "projects", args.slug, EVALS_DIR)
    if not directory.is_dir():
        print(f"golden_set: no {directory.relative_to(root).as_posix()}/ yet; run golden_set.py init", file=sys.stderr)
        return 1
    features = sorted(child.name for child in directory.iterdir() if child.is_dir())
    for feature in features:
        sheet = directory / feature / SHEET
        rows = len(read_sheet(sheet)[1]) if sheet.is_file() else 0
        print(f"{feature}: {rows} row(s)")
    if not features:
        print("no features yet")
    return 0


def cmd_check(args, root: Path = ROOT) -> int:
    """The rules from the reference that can be checked mechanically. memory.py doctor walks
    a fixed list of filenames and never sees this tree, by decision: these rules live in one
    place rather than two that drift."""
    path = sheet_path(root, args.slug, args.feature)
    errors: list[str] = []
    warns: list[str] = []
    try:
        _header, rows = read_sheet(path)
    except (ValueError, OSError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    for number, row in enumerate(rows, start=2):
        row_id, source, locator, _expected, label, reason, handle, _grader, graded = row
        if not row_id.strip():
            errors.append(f"{path}:{number}: the id is empty")
        if not reason.strip():
            errors.append(f"{path}:{number}: row {row_id} has no reason; every row carries one line on why")
        if label not in LABELS:
            errors.append(f"{path}:{number}: label {label!r} is not one of {', '.join(LABELS)}")
        if source not in SOURCES:
            errors.append(f"{path}:{number}: source {source!r} is not one of {', '.join(SOURCES)}")
        if handle and handle not in HANDLES:
            warns.append(f"{path}:{number}: handle {handle!r} is not one of the usual ones")
        try:
            when = date.fromisoformat(graded)
            if when > date.today():
                errors.append(f"{path}:{number}: last graded {graded} is in the future")
            elif args.stale_after and graded < args.stale_after:
                warns.append(f"{path}:{number}: row {row_id} was last graded {graded}, before {args.stale_after}")
        except ValueError:
            errors.append(f"{path}:{number}: last graded {graded!r} is not a date")
    locators: dict[str, str] = {}
    for row in rows:
        key = row[2].strip().lower()
        if key in locators:
            warns.append(f"{path}: rows {locators[key]} and {row[0]} share the input locator {row[2]!r}")
        locators[key] = row[0]
    real_failures = [row for row in rows if row[4] in ("weak", "fail") and row[1] == "real trace"]
    if rows and not real_failures:
        has_failure = any(row[4] in ("weak", "fail") for row in rows)
        has_real = any(row[1] == "real trace" for row in rows)
        missing = "a failure" if not has_failure else "a real trace behind the failures"
        errors.append(f"{path}: no row is both a real trace and a failure ({missing} is missing); "
                      "a set with no failure in it is a scrapbook, not a test")
    if not rows:
        warns.append(f"{path}: no rows yet")
    elif not any(row[1] == "real trace" for row in rows):
        warns.append(f"{path}: every row is synthetic; practice rows do not decide a release")
    scenario = scenario_path(root, args.slug, args.feature)
    if not scenario.is_file():
        warns.append(f"{scenario.relative_to(root).as_posix()} is missing; the limits and the block rule live there")
    for message in warns:
        print(f"WARN {message}")
    for message in errors:
        print(f"ERROR {message}", file=sys.stderr)
    print(f"{path.relative_to(root).as_posix()}: {len(rows)} row(s), {len(errors)} error(s), {len(warns)} warning(s)")
    if errors:
        return 1
    return 1 if (warns and args.strict) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def with_feature(name, help_text):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("slug")
        p.add_argument("--feature", required=True)
        return p

    with_feature("init", "create the scenario sheet and an empty golden set").set_defaults(func=cmd_init)

    p = with_feature("add", "append one row a person wrote")
    p.add_argument("--source", required=True, help="real-trace or synthetic")
    p.add_argument("--locator", required=True, help="where the input lives: a ticket id, a thread, a file")
    p.add_argument("--expected", required=True, help="the behaviour a good answer shows")
    p.add_argument("--label", required=True, choices=LABELS)
    p.add_argument("--reason", required=True, help="one line on why it has that label")
    p.add_argument("--handle", required=True, help=f"the pattern, not the row: {', '.join(HANDLES)}")
    p.add_argument("--grader", required=True, help="who graded it, by role")
    p.add_argument("--id", help="row id; defaults to the next number")
    p.add_argument("--last-graded", help="YYYY-MM-DD; defaults to today")
    p.set_defaults(func=cmd_add)

    p = with_feature("show", "counts by label, source and handle")
    p.add_argument("--rows", action="store_true", help="print the rows too")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("list", help="the features that have a golden set")
    p.add_argument("slug")
    p.set_defaults(func=cmd_list)

    p = with_feature("check", "the reference's rules that can be checked mechanically")
    p.add_argument("--stale-after", help="YYYY-MM-DD; warn about rows last graded before it")
    p.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    p.set_defaults(func=cmd_check)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"golden_set: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
