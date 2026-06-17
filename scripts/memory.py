#!/usr/bin/env python3
"""
memory.py — policy layer for .ai/memory: caps, rotation, park/activate ritual.

Usage:
    python3 scripts/memory.py log <slug>|repo "<entry text>" [--title "..."]
    python3 scripts/memory.py park <slug>
    python3 scripts/memory.py activate <slug> [--stage <stage>] [--name "Project Name"]
    python3 scripts/memory.py distill <slug>
    python3 scripts/memory.py doctor

Layers (see CLAUDE.md "Memory rules"): active-context.md is a pointer capped at
POINTER_CAP; per-project changelog.md keeps CHANGELOG_KEEP entries (older ones
rotate into changelog-archive.md, verbatim); session history lives in
projects/<slug>/state.md. Rotation never deletes content and never touches
PII paths (raw-evidence/, people/, **/data).
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEM = ROOT / ".ai" / "memory"
POINTER = MEM / "active-context.md"
CONTEXT_EVENTS = MEM / "context-events.jsonl"  # read by scripts/context_watch.py
ROOT_CHANGELOG = ROOT / ".ai" / "changelog.md"
PROJECTS = MEM / "projects"

POINTER_CAP = 2048          # bytes
CHANGELOG_KEEP = 3          # entries kept in the active changelog
CHANGELOG_SOFT_CAP = 6144   # bytes; doctor warns above this even within KEEP
KICKOFF_SOFT_CAP = 4096     # bytes

ROTATION_NOTE = "> Active log keeps the most recent entries; older entries in `{name}`.\n\n"


def fail(msg):
    print(f"memory.py: {msg}", file=sys.stderr)
    sys.exit(1)


def log_context_event(slug):
    """Append a context transition (slug=None on park) for time tracking."""
    ts = datetime.now().astimezone().isoformat(timespec="seconds")
    with CONTEXT_EVENTS.open("a") as f:
        f.write(json.dumps({"ts": ts, "slug": slug}) + "\n")


def split_entries(text):
    """Return (preamble, [entries]) splitting on '## ' headers."""
    parts = re.split(r"(?m)^(?=## )", text)
    return parts[0], parts[1:]


def entry_date(entry):
    m = re.search(r"\d{4}-\d{2}-\d{2}", entry.splitlines()[0])
    return m.group(0) if m else "0000-00-00"


def rotate(changelog: Path, keep=CHANGELOG_KEEP, quiet=False):
    if not changelog.exists():
        return
    text = changelog.read_text()
    text = re.sub(r"(?m)^> Active log keeps the .+\n\n", "", text)
    preamble, entries = split_entries(text)
    archive = changelog.with_name("changelog-archive.md")
    if len(entries) > keep:
        order = sorted(range(len(entries)), key=lambda i: entry_date(entries[i]), reverse=True)
        keep_idx, arch_idx = sorted(order[:keep]), sorted(order[keep:])
        header = "" if archive.exists() else (
            f"# Changelog archive\n\n> Rotated out of `{changelog.name}`. Full entries, verbatim.\n\n"
        )
        with archive.open("a") as f:
            f.write(header + "".join(entries[i] for i in arch_idx))
        entries = [entries[i] for i in keep_idx]
        if not quiet:
            print(f"rotated {len(arch_idx)} entr{'y' if len(arch_idx)==1 else 'ies'} -> {archive.relative_to(ROOT)}")
    note = ROTATION_NOTE.format(name=archive.name) if archive.exists() else ""
    changelog.write_text(preamble.rstrip() + "\n\n" + note + "".join(entries))


def project_dir(slug):
    d = PROJECTS / slug
    if not d.is_dir():
        fail(f"unknown project slug '{slug}' (no {d.relative_to(ROOT)}/)")
    return d


def cmd_log(args):
    if args.slug == "repo":
        changelog = ROOT_CHANGELOG
    else:
        changelog = project_dir(args.slug) / "changelog.md"
    today = date.today().isoformat()
    title = args.title or "session log"
    entry = f"## {today}: {title}\n\n{args.entry.rstrip()}\n\n"
    if changelog.exists():
        text = changelog.read_text()
        text = re.sub(r"(?m)^> Active log keeps the .+\n\n", "", text)
        preamble, entries = split_entries(text)
        changelog.write_text(preamble.rstrip() + "\n\n" + entry + "".join(entries))
    else:
        name = "Changelog" if args.slug == "repo" else f"Changelog: {args.slug}"
        changelog.write_text(f"# {name}\n\n{entry}")
    rotate(changelog)
    print(f"logged to {changelog.relative_to(ROOT)}")


def read_pointer():
    if not POINTER.exists():
        fail("active-context.md missing")
    return POINTER.read_text()


def active_slug(text):
    m = re.search(r"(?m)^## ACTIVE: `([a-z0-9\-]+)`", text)
    return m.group(1) if m else None


def active_block(text):
    m = re.search(r"(?ms)^## ACTIVE: .*?(?=^## |\Z)", text)
    return m.group(0) if m else None


def cmd_park(args):
    text = read_pointer()
    slug = active_slug(text)
    if slug is None:
        fail("no ACTIVE block in pointer")
    if args.slug != slug:
        fail(f"active project is '{slug}', not '{args.slug}'")
    block = active_block(text)
    today = date.today().isoformat()

    # 1. session block -> state.md (newest first, after the header/blockquote)
    state = project_dir(slug) / "state.md"
    body = re.sub(r"(?m)^## ACTIVE: .*$", f"## Parked {today}", block).rstrip() + "\n\n"
    if state.exists():
        stext = state.read_text()
        m = re.search(r"(?m)^## ", stext)
        pos = m.start() if m else len(stext)
        state.write_text(stext[:pos] + body + stext[pos:])
    else:
        state.write_text(f"# State — {slug}\n\n{body}")

    # 2. stage for the parked one-liner
    stg = re.search(r"(?m)Current\s+stage\*{0,2}\s*:\s*(\S+)", block)
    stage = stg.group(1) if stg else "unknown"

    # 3. rewrite pointer: ACTIVE -> none, add parked line on top of the list
    text = text.replace(block, f"## ACTIVE: (none)\n\n- Parked `{slug}` {today}. Pick next with `memory.py activate <slug>`.\n\n")
    text = re.sub(
        r"(?m)^(## Parked / closed.*\n\n)",
        rf"\1- `{slug}`: {stage}; parked {today}; see `projects/{slug}/state.md`\n",
        text,
    )
    POINTER.write_text(text)
    log_context_event(None)
    rotate(project_dir(slug) / "changelog.md", quiet=True)
    print(f"parked {slug}; state -> {state.relative_to(ROOT)}")
    check_pointer_cap()


def cmd_activate(args):
    text = read_pointer()
    current = active_slug(text)
    if current == args.slug:
        print(f"{args.slug} already active")
        return
    if current is not None:
        fail(f"'{current}' is still active — run: memory.py park {current}")
    project_dir(args.slug)
    today = date.today().isoformat()

    # pull the parked one-liner (if any) to recover stage
    line_re = re.compile(rf"(?m)^- `{re.escape(args.slug)}`: ([^;\n]+);.*\n")
    m = line_re.search(text)
    stage = args.stage or (m.group(1).strip().split()[0].lower() if m else "discovery")
    if m:
        text = line_re.sub("", text)

    name = args.name or args.slug.replace("-", " ").title()
    block = (
        f"## ACTIVE: `{args.slug}` (set {today})\n\n"
        f"- **Project**: {name}\n"
        f"- **Slug**: `{args.slug}`\n"
        f"- **Current stage**: {stage}\n"
        f"- Read FIRST on resume: `projects/{args.slug}/state.md`, then `session-kickoff.md`\n\n"
    )
    if re.search(r"(?m)^## ACTIVE: \(none\)", text):
        text = re.sub(r"(?ms)^## ACTIVE: \(none\).*?(?=^## )", block, text)
    else:
        text = re.sub(r"(?m)^(## Parked / closed)", block + r"\1", text)
    POINTER.write_text(text)
    log_context_event(args.slug)
    print(f"activated {args.slug} (stage: {stage})")
    check_pointer_cap()


def cmd_distill(args):
    d = project_dir(args.slug)
    over = []
    for name, cap in [("changelog.md", CHANGELOG_SOFT_CAP), ("session-kickoff.md", KICKOFF_SOFT_CAP),
                      ("state.md", 16384), ("profile.md", 12288)]:
        f = d / name
        if f.exists() and f.stat().st_size > cap:
            over.append((f, cap))
    if not over:
        print(f"{args.slug}: all files within caps, nothing to distill")
        return
    print(f"{args.slug}: files over cap (model-assisted distill needed):")
    for f, cap in over:
        print(f"  {f.relative_to(ROOT)}  {f.stat().st_size} B (cap {cap})")
    print(
        "\nDistill protocol: fold the oldest blocks into a short synthesis at the top\n"
        "of the same file (decisions kept, narration dropped); move the folded raw\n"
        "blocks verbatim into changelog-archive.md or a dated archive section in\n"
        "state.md. Never touch raw-evidence/, people/, or data paths."
    )
    sys.exit(2)


def check_pointer_cap():
    size = POINTER.stat().st_size
    if size > POINTER_CAP:
        print(f"WARN pointer {size} B > cap {POINTER_CAP} B — trim parked lines or park less prose", file=sys.stderr)
        return False
    return True


def cmd_doctor(_args):
    errors, warns = [], []
    text = read_pointer()

    if POINTER.stat().st_size > POINTER_CAP:
        errors.append(f"pointer {POINTER.stat().st_size} B > cap {POINTER_CAP} B")
    blocks = re.findall(r"(?m)^## ACTIVE: ", text)
    if len(blocks) != 1:
        errors.append(f"pointer has {len(blocks)} ACTIVE blocks (want exactly 1)")
    slug = active_slug(text)
    if slug and not (PROJECTS / slug).is_dir():
        errors.append(f"ACTIVE slug '{slug}' has no projects/ dir")
    if slug and not re.search(r"(?m)Current\s+stage\*{0,2}\s*:", text):
        errors.append("ACTIVE block missing 'Current stage:' (stage_context.py will go blind)")

    for line_slug in re.findall(r"(?m)^- `([a-z0-9\-]+)`:", text):
        if not (PROJECTS / line_slug).is_dir():
            errors.append(f"parked line for '{line_slug}' but no projects/ dir")
        elif not (PROJECTS / line_slug / "state.md").exists():
            warns.append(f"'{line_slug}' parked without state.md")

    for changelog in [ROOT_CHANGELOG, *PROJECTS.glob("*/changelog.md")]:
        if not changelog.exists():
            continue
        size = changelog.stat().st_size
        _, entries = split_entries(changelog.read_text())
        if len(entries) > CHANGELOG_KEEP:
            errors.append(f"{changelog.relative_to(ROOT)}: {len(entries)} entries > keep {CHANGELOG_KEEP} — run memory.py log/rotate")
        if size > CHANGELOG_SOFT_CAP:
            warns.append(f"{changelog.relative_to(ROOT)}: {size} B > {CHANGELOG_SOFT_CAP} B — candidate for memory.py distill")

    for w in warns:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if not errors and not warns:
        print("doctor: all green")
    sys.exit(1 if errors else 0)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("log", help="append a changelog entry (auto-rotates)")
    s.add_argument("slug", help="project slug, or 'repo' for .ai/changelog.md")
    s.add_argument("entry", help="entry body (markdown)")
    s.add_argument("--title", help="entry title after the date")
    s.set_defaults(func=cmd_log)

    s = sub.add_parser("park", help="park the active project (block -> state.md, pointer rewritten)")
    s.add_argument("slug")
    s.set_defaults(func=cmd_park)

    s = sub.add_parser("activate", help="make a project active (auto-fails if another is active)")
    s.add_argument("slug")
    s.add_argument("--stage", help="workflow stage (default: from parked line, else discovery)")
    s.add_argument("--name", help="display name (default: titleized slug)")
    s.set_defaults(func=cmd_activate)

    s = sub.add_parser("distill", help="report files over caps + print the distill protocol")
    s.add_argument("slug")
    s.set_defaults(func=cmd_distill)

    s = sub.add_parser("doctor", help="cap + structure checks (exit 1 on errors)")
    s.set_defaults(func=cmd_doctor)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
