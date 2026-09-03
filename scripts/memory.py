#!/usr/bin/env python3
"""
memory.py — policy layer for .ai/memory: caps, rotation, park/activate ritual,
and model-assisted consolidation (distill).

Usage:
    python3 scripts/memory.py log <slug>|repo "<entry text>" [--title "..."]
    python3 scripts/memory.py park <slug>
    python3 scripts/memory.py activate <slug> [--stage <stage>] [--name "Project Name"]
    python3 scripts/memory.py distill <slug>                        # report files over caps
    python3 scripts/memory.py distill <slug> --prepare [--file changelog|state|decisions]
    python3 scripts/memory.py distill <slug> --apply [PATH]
    python3 scripts/memory.py index <slug>|repo
    python3 scripts/memory.py doctor

Layers (see CLAUDE.md "Memory rules"): active-context.md is a pointer capped at
POINTER_CAP; per-project changelog.md keeps CHANGELOG_KEEP entries (older ones
rotate into changelog-archive.md, verbatim); session history lives in
projects/<slug>/state.md. Warm files carry soft caps (DISTILL_CAPS). When one
is over, `distill --prepare` extracts the oldest dated blocks into a package
the model summarises, and `distill --apply` moves those blocks verbatim into
the sibling *-archive.md and puts the synthesis in their place. Nothing is
ever deleted. Every *-archive.md carries an index block (one line per
archived block), regenerated on each append and rebuilt by `index`, so the
cold layer is retrieved grep-first and never read wholesale.
PII paths (raw-evidence/, people/, **/data) are refused in code
(PII_DENY): never rotated, distilled, logged, or parked.
"""

import argparse
import hashlib
import json
import os
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
SYNTHESIS_TEMPLATE = MEM / "_templates" / "distill-synthesis.md"

POINTER_CAP = 2048          # bytes
CHANGELOG_KEEP = 3          # entries kept in the active changelog
CHANGELOG_SOFT_CAP = 6144   # bytes; doctor warns above this even within KEEP
KICKOFF_SOFT_CAP = 4096     # bytes
STATE_SOFT_CAP = 16384      # bytes
PROFILE_SOFT_CAP = 12288    # bytes
DECISIONS_SOFT_CAP = 12288  # bytes

# Warm files the doctor and `distill` measure. Only the three block logs below
# in DISTILL_FILES are foldable; kickoff and profile are prose the model
# rewrites by hand when the report flags them.
DISTILL_CAPS = {
    "changelog.md": CHANGELOG_SOFT_CAP,
    "session-kickoff.md": KICKOFF_SOFT_CAP,
    "state.md": STATE_SOFT_CAP,
    "profile.md": PROFILE_SOFT_CAP,
    "decisions.md": DECISIONS_SOFT_CAP,
}
# stem -> (source, archive, archive title, block order inside the source)
DISTILL_FILES = {
    "changelog": ("changelog.md", "changelog-archive.md", "Changelog", "newest-first"),
    "state": ("state.md", "state-archive.md", "State", "newest-first"),
    "decisions": ("decisions.md", "decisions-archive.md", "Decisions", "oldest-first"),
}
DISTILL_DIR = ".distill"
FOLDED_MARKER = "Folded blocks (verbatim in"
INDEX_MARKER = "Index (one line per archived block"
INDEX_HEADER = INDEX_MARKER + ", file order; grep here before opening a block):"

# Any path segment on this list, relative to the repo root, is PII territory:
# the scripts refuse to read, write, rotate, or fold it. The guarantee used to
# hold only because every target was a hard-coded filename; now it is checked.
PII_DENY = ("raw-evidence", "people", "data")

ROTATION_NOTE = "> Active log keeps the most recent entries; older entries in `{name}`.\n\n"
UNDATED = "0000-00-00"


def fail(msg):
    print(f"memory.py: {msg}", file=sys.stderr)
    sys.exit(1)


def display(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def is_pii(path: Path) -> bool:
    """True when any segment of the path, relative to the repo root, is on PII_DENY."""
    try:
        parts = path.resolve().relative_to(ROOT.resolve()).parts
    except ValueError:
        parts = path.parts
    return any(part in PII_DENY for part in parts)


def guard(path: Path) -> Path:
    if is_pii(path):
        fail(f"refusing to touch PII path {display(path)} (denylist: {', '.join(PII_DENY)})")
    return path


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def log_context_event(slug):
    """Append a context transition (slug=None on park) for time tracking."""
    ts = datetime.now().astimezone().isoformat(timespec="seconds")
    with CONTEXT_EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": ts, "slug": slug}) + "\n")


def split_entries(text):
    """Return (preamble, [entries]) splitting on '## ' headers."""
    parts = re.split(r"(?m)^(?=## )", text)
    return parts[0], parts[1:]


def entry_date(entry):
    m = re.search(r"\d{4}-\d{2}-\d{2}", entry.splitlines()[0])
    return m.group(0) if m else UNDATED


def entry_heading(entry):
    return entry.splitlines()[0].lstrip("#").strip()


def archive_header(source_name: str, title: str) -> str:
    return f"# {title} archive\n\n> Rotated out of `{source_name}`. Full entries, verbatim.\n\n"


def index_line(entry_date_str: str, heading: str) -> str:
    """One index line: '- <date> <heading without its own date>'."""
    text = re.sub(r"\d{4}-\d{2}-\d{2}:?\s*", "", heading, count=1).strip()
    return f"- {entry_date_str} {text}".rstrip()


def index_state(text: str):
    """(blocks, index lines) for an archive, for staleness checks."""
    preamble, entries = split_entries(text)
    lines, counting = 0, False
    for line in preamble.splitlines():
        if line.startswith(INDEX_MARKER):
            counting = True
        elif counting and line.startswith("- "):
            lines += 1
        else:
            counting = False
    return len(entries), lines


def strip_index(preamble: str) -> str:
    """Drop a previous index block: the marker line and the '- ' lines directly
    under it, and nothing else. Line-based on purpose — a block left without
    its trailing blank line is still removed, and no other prose is ever
    consumed on the way."""
    kept, dropping = [], False
    for line in preamble.splitlines(keepends=True):
        if line.startswith(INDEX_MARKER):
            dropping = True
            continue
        if dropping and line.startswith("- "):
            continue
        dropping = False
        kept.append(line)
    return "".join(kept)


def with_index(text: str) -> str:
    """Archive text with its index block regenerated from the block headings.
    The block sits in the preamble, before the first '## ', so split_entries
    and entry_date never see it. Idempotent: the index is a function of the
    headings and the preamble is normalised."""
    preamble, entries = split_entries(text)
    if not entries:
        return text
    head = strip_index(preamble).rstrip()
    lines = "\n".join(index_line(entry_date(e), entry_heading(e)) for e in entries)
    prefix = f"{head}\n\n" if head else ""
    return f"{prefix}{INDEX_HEADER}\n{lines}\n\n" + "".join(entries)


def verify_rebuild(old_text: str, new_text: str, appended) -> bool:
    """True when the rebuilt archive holds exactly the old blocks followed by
    the appended ones, byte for byte and in order, with one index line each."""
    _, old_entries = split_entries(old_text)
    _, new_entries = split_entries(new_text)
    if new_entries != list(old_entries) + list(appended):
        return False
    if not new_entries:
        return True
    blocks, lines = index_state(new_text)
    return blocks == lines


def discard_staged(path: Path) -> None:
    """Drop a staged temporary file, tolerating whatever sits in its place."""
    try:
        path.unlink()
    except OSError:
        pass


def rebuild_archive(archive: Path, header: str, appended) -> bool:
    """Rewrite the archive with `appended` added and the index regenerated.
    The live archive is never opened for writing: the full content is staged in
    a sibling .tmp, read back, and verified block by block, and only then does
    os.replace swap it in. Contract: any failure before the replace leaves the
    archive byte for byte intact, and the replace itself yields atomically
    either the old content or the new one. The read-back after the replace
    detects a swap that did not land; it cannot restore the old content, which
    the replace has already dropped. Returns True when the file changed."""
    guard(archive)
    current = archive.read_text(encoding="utf-8") if archive.exists() else None
    if current is None and not appended:
        return False
    old = current if current is not None else header
    new = with_index(old + "".join(appended))
    if new == current:
        return False
    tmp = archive.with_name(archive.name + ".tmp")
    try:
        tmp.write_text(new, encoding="utf-8")
        staged = tmp.read_text(encoding="utf-8")
    except OSError as exc:
        discard_staged(tmp)
        fail(f"could not stage the archive rebuild at {display(tmp)} ({exc}); {display(archive)} left intact")
    if staged != new or not verify_rebuild(old, staged, appended):
        discard_staged(tmp)
        fail(f"refusing to replace {display(archive)}: the staged rebuild at {display(tmp)} does not hold "
             f"every block and one index line each; {display(archive)} left intact")
    try:
        os.replace(tmp, archive)
    except OSError as exc:
        discard_staged(tmp)
        fail(f"could not replace {display(archive)} ({exc}); it was left intact")
    if archive.read_text(encoding="utf-8") != staged:
        fail(f"{display(archive)} does not match the staged rebuild that was verified and swapped in")
    return True


def append_archive(archive: Path, source_name: str, title: str, blocks) -> bool:
    """Add blocks verbatim to the sibling archive and regenerate its index
    block; header written once, on creation. Goes through rebuild_archive, so
    the archive is replaced atomically or not at all."""
    return rebuild_archive(archive, archive_header(source_name, title), blocks)


def rotate(changelog: Path, keep=CHANGELOG_KEEP, quiet=False):
    if not changelog.exists():
        return
    guard(changelog)
    text = changelog.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^> Active log keeps the .+\n\n", "", text)
    preamble, entries = split_entries(text)
    archive = changelog.with_name("changelog-archive.md")
    if len(entries) > keep:
        order = sorted(range(len(entries)), key=lambda i: entry_date(entries[i]), reverse=True)
        keep_idx, arch_idx = sorted(order[:keep]), sorted(order[keep:])
        append_archive(archive, changelog.name, "Changelog", [entries[i] for i in arch_idx])
        entries = [entries[i] for i in keep_idx]
        if not quiet:
            print(f"rotated {len(arch_idx)} entr{'y' if len(arch_idx)==1 else 'ies'} -> {archive.relative_to(ROOT)}")
    note = ROTATION_NOTE.format(name=archive.name) if archive.exists() else ""
    changelog.write_text(preamble.rstrip() + "\n\n" + note + "".join(entries), encoding="utf-8")


def project_dir(slug):
    d = PROJECTS / slug
    guard(d)
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
        text = changelog.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^> Active log keeps the .+\n\n", "", text)
        preamble, entries = split_entries(text)
        changelog.write_text(preamble.rstrip() + "\n\n" + entry + "".join(entries), encoding="utf-8")
    else:
        name = "Changelog" if args.slug == "repo" else f"Changelog: {args.slug}"
        changelog.write_text(f"# {name}\n\n{entry}", encoding="utf-8")
    rotate(changelog)
    print(f"logged to {changelog.relative_to(ROOT)}")


def read_pointer():
    if not POINTER.exists():
        fail("active-context.md missing")
    return POINTER.read_text(encoding="utf-8")


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
    state = guard(project_dir(slug) / "state.md")
    body = re.sub(r"(?m)^## ACTIVE: .*$", f"## Parked {today}", block).rstrip() + "\n\n"
    if state.exists():
        stext = state.read_text(encoding="utf-8")
        m = re.search(r"(?m)^## ", stext)
        pos = m.start() if m else len(stext)
        state.write_text(stext[:pos] + body + stext[pos:], encoding="utf-8")
    else:
        state.write_text(f"# State — {slug}\n\n{body}", encoding="utf-8")

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
    POINTER.write_text(text, encoding="utf-8")
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
    POINTER.write_text(text, encoding="utf-8")
    log_context_event(args.slug)
    print(f"activated {args.slug} (stage: {stage})")
    check_pointer_cap()


# -- distill ---------------------------------------------------------------

def dated_blocks(entries, order):
    """[(index, date)] of dated blocks, oldest first. Undated blocks (the
    template's example block, fixed sections) are never candidates. Same-date
    ties follow the file's own convention: in a newest-first file a later
    block is older; in an oldest-first file an earlier one is."""
    dated = [(i, entry_date(e)) for i, e in enumerate(entries) if entry_date(e) != UNDATED]
    key = (lambda x: (x[1], -x[0])) if order == "newest-first" else (lambda x: (x[1], x[0]))
    return sorted(dated, key=key)


def fold_plan(text, order, cap, force_one):
    """Indices (file order) of the blocks to fold, or None when fewer than two
    dated blocks exist. The newest dated block is never folded. Over cap: fold
    from the oldest until the remainder leaves a quarter of the cap free for
    the synthesis. Under cap with an explicit --file: fold exactly one."""
    _, entries = split_entries(text)
    dated = dated_blocks(entries, order)
    if len(dated) < 2:
        return None
    candidates = dated[:-1]
    if force_one:
        return [candidates[0][0]]
    remaining = len(text.encode("utf-8"))
    chosen = []
    for i, _ in candidates:
        if remaining + cap // 4 <= cap:
            break
        chosen.append(i)
        remaining -= len(entries[i].encode("utf-8"))
    return sorted(chosen)


def render_template(path: Path, **keys) -> str:
    if not path.exists():
        fail(f"missing template {display(path)}")
    text = path.read_text(encoding="utf-8")
    for k, v in keys.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def load_manifest(pkg: Path):
    manifest = pkg / "manifest.json"
    if not manifest.exists():
        return None
    return json.loads(manifest.read_text(encoding="utf-8"))


def distill_report(slug, d):
    over = []
    for name, cap in DISTILL_CAPS.items():
        f = d / name
        if f.exists() and f.stat().st_size > cap:
            over.append((f, cap))
    if not over:
        print(f"{slug}: all files within caps, nothing to distill")
        return
    print(f"{slug}: files over cap (model-assisted distill needed):")
    for f, cap in over:
        print(f"  {f.relative_to(ROOT)}  {f.stat().st_size} B (cap {cap})")
    print(
        f"\nDistill protocol: `memory.py distill {slug} --prepare [--file changelog|state|decisions]`\n"
        f"writes projects/{slug}/{DISTILL_DIR}/ (manifest.json, blocks.md, synthesis.md). Fill in\n"
        "synthesis.md (decisions kept, narration dropped), then `--apply` moves the folded\n"
        "blocks verbatim into the sibling *-archive.md and puts the synthesis in their\n"
        "place. session-kickoff.md and profile.md are prose: rewrite them by hand.\n"
        "Never touch raw-evidence/, people/, or data paths (refused in code)."
    )
    sys.exit(2)


def distill_prepare(slug, d, file_stem):
    pkg = d / DISTILL_DIR
    guard(pkg)
    if file_stem is None:
        over = [stem for stem, (src, _a, _t, _o) in DISTILL_FILES.items()
                if (d / src).exists() and (d / src).stat().st_size > DISTILL_CAPS[src]]
        if not over:
            print(f"{slug}: no foldable file over its cap; pass --file to fold one block anyway")
            return
        if len(over) > 1:
            fail(f"several files over cap ({', '.join(over)}); pick one with --file")
        file_stem = over[0]
    src_name, archive_name, _title, order = DISTILL_FILES[file_stem]
    src = guard(d / src_name)
    if not src.exists():
        fail(f"{display(src)} does not exist")
    text = src.read_text(encoding="utf-8")
    cap = DISTILL_CAPS[src_name]

    pending = load_manifest(pkg)
    if pending and not pending.get("applied") and pending.get("source_sha") == sha256(
        (d / pending["source"]).read_text(encoding="utf-8") if (d / pending["source"]).exists() else ""
    ):
        fail(f"pending package in {display(pkg)} still matches its source; run --apply or delete it first")

    force_one = len(text.encode("utf-8")) <= cap
    chosen = fold_plan(text, order, cap, force_one)
    if not chosen:
        fail(f"{display(src)} needs at least two dated '## ' blocks to fold one and keep the newest")
    _, entries = split_entries(text)
    blocks = [entries[i] for i in chosen]
    picked = set(chosen)
    oldest_first = [i for i, _ in dated_blocks(entries, order) if i in picked]
    newest_date = max(entry_date(entries[i]) for i in chosen)
    index = "\n".join(index_line(entry_date(entries[i]), entry_heading(entries[i])) for i in oldest_first)

    synthesis = render_template(
        SYNTHESIS_TEMPLATE, date=newest_date, count=len(chosen),
        source=src_name, archive=archive_name, index=index,
    )
    manifest = {
        "slug": slug,
        "source": src_name,
        "archive": archive_name,
        "order": order,
        "cap": cap,
        "source_sha": sha256(text),
        "prepared_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "applied": False,
        "blocks": [
            {"index": i, "date": entry_date(entries[i]), "heading": entry_heading(entries[i]),
             "sha": sha256(entries[i])}
            for i in oldest_first
        ],
    }
    pkg.mkdir(exist_ok=True)
    (pkg / "blocks.md").write_text("".join(blocks), encoding="utf-8")
    (pkg / "synthesis.md").write_text(synthesis, encoding="utf-8")
    (pkg / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"prepared {len(chosen)} block(s) from {display(src)} -> {display(pkg)}/")
    print(f"next: fill in {display(pkg / 'synthesis.md')} (replace the [Fill in ...] line), then\n"
          f"      python3 scripts/memory.py distill {slug} --apply")


def distill_apply(slug, d, pkg_arg):
    pkg = guard(Path(pkg_arg) if pkg_arg else d / DISTILL_DIR)
    manifest = load_manifest(pkg)
    if manifest is None:
        fail(f"no package at {display(pkg)}; run --prepare first")
    if manifest.get("applied"):
        fail(f"package {display(pkg)} was already applied on {manifest.get('applied_at')}")
    try:
        stem = next(stem for stem, v in DISTILL_FILES.items() if v[0] == manifest.get("source"))
    except StopIteration:
        fail(f"package {display(pkg)} names an unsupported source")
    src_name, archive_name, title, order = DISTILL_FILES[stem]
    expected_cap = DISTILL_CAPS[src_name]
    if manifest.get("slug") != slug:
        fail(f"package {display(pkg)} belongs to project '{manifest.get('slug')}', not '{slug}'")
    if (manifest.get("archive") != archive_name or manifest.get("order") != order
            or manifest.get("cap") != expected_cap):
        fail(f"package {display(pkg)} metadata does not match the canonical contract for {src_name}")
    manifest_blocks = manifest.get("blocks")
    if not isinstance(manifest_blocks, list) or not manifest_blocks:
        fail(f"package {display(pkg)} has no fold blocks")
    src = guard(d / src_name)
    archive = guard(d / archive_name)
    cap = expected_cap

    text = src.read_text(encoding="utf-8")
    if sha256(text) != manifest["source_sha"]:
        fail(f"{display(src)} changed since --prepare; run --prepare again")
    preamble, entries = split_entries(text)
    blocks_md = (pkg / "blocks.md").read_text(encoding="utf-8")
    chosen = []
    for b in manifest_blocks:
        i = b.get("index") if isinstance(b, dict) else None
        heading = b.get("heading", "<invalid>") if isinstance(b, dict) else "<invalid>"
        if not isinstance(i, int) or i < 0 or i >= len(entries) or sha256(entries[i]) != b.get("sha"):
            fail(f"block '{heading}' no longer matches the source; run --prepare again")
        chosen.append(i)
    if len(set(chosen)) != len(chosen):
        fail(f"package {display(pkg)} repeats a fold block")
    chosen = sorted(chosen)
    if blocks_md != "".join(entries[i] for i in chosen):
        fail("blocks.md does not exactly match the manifest blocks; package is corrupt")

    synthesis = (pkg / "synthesis.md").read_text(encoding="utf-8")
    body = synthesis.split(FOLDED_MARKER)[0].rstrip()
    if "[Fill in" in body or "{{" in body:
        fail("synthesis.md still carries the template placeholder; write the synthesis first")
    if not re.match(r"## .*\d{4}-\d{2}-\d{2}", body.lstrip("\n").splitlines()[0]):
        fail("synthesis.md must open with a '## ' heading (dated, so entry_date keeps working)")
    index = "\n".join(index_line(b["date"], b["heading"]) for b in manifest["blocks"])
    synthesis = f"{body.lstrip(chr(10))}\n\n{FOLDED_MARKER} `{archive_name}`):\n{index}\n\n"

    folded = [entries[i] for i in chosen]
    kept = [e for i, e in enumerate(entries) if i not in chosen]
    kept.insert(chosen[0], synthesis)
    new_text = preamble + "".join(kept)
    projected = len(new_text.encode("utf-8"))
    if projected > cap:
        print(f"memory.py: synthesis too long: {display(src)} would be {projected} B > cap {cap} B; "
              f"shorten synthesis.md and re-run --apply (nothing written)", file=sys.stderr)
        sys.exit(2)

    # Nothing above this line wrote anything. Archive first, verify, then rewrite.
    append_archive(archive, src_name, title, folded)
    archived = archive.read_text(encoding="utf-8")
    for block in folded:
        if block not in archived:
            fail(f"archive verification failed for '{entry_heading(block)}'; {display(src)} left intact")
    src.write_text(new_text, encoding="utf-8")
    manifest["applied"] = True
    manifest["applied_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    (pkg / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"applied: {len(folded)} block(s) -> {display(archive)}; {display(src)} now {projected} B (cap {cap})")


def cmd_distill(args):
    d = project_dir(args.slug)
    if args.file and not args.prepare:
        fail("--file only applies with --prepare")
    if args.apply is not None:
        return distill_apply(args.slug, d, args.apply or None)
    if args.prepare:
        return distill_prepare(args.slug, d, args.file)
    distill_report(args.slug, d)


def cmd_index(args):
    """Rebuild and list the cold-layer index: what the archives hold, one line
    per block, without opening a single block."""
    if args.slug == "repo":
        targets = [(ROOT_CHANGELOG.with_name("changelog-archive.md"), "changelog.md", "Changelog")]
    else:
        d = project_dir(args.slug)
        targets = [(d / archive, src, title) for src, archive, title, _order in DISTILL_FILES.values()]
    found = False
    try:
        for archive, src_name, title in targets:
            if not archive.exists():
                continue
            found = True
            rebuilt = rebuild_archive(archive, archive_header(src_name, title), [])
            _, entries = split_entries(archive.read_text(encoding="utf-8"))
            note = " (index rebuilt)" if rebuilt else ""
            print(f"{display(archive)}: {len(entries)} block(s){note}")
            for e in entries:
                print(f"  {index_line(entry_date(e), entry_heading(e))}")
        if not found:
            print(f"{args.slug}: no archives yet; nothing has rotated or folded into the cold layer")
    except BrokenPipeError:
        # the listing is built to be piped (grep, head): a reader that closes
        # early is the normal case, not a failure
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())


def stale_index_warning(path: Path, slug: str):
    """WARN string when the archive's index no longer matches its blocks."""
    text = path.read_text(encoding="utf-8")
    if with_index(text) == text:
        return None
    blocks, lines = index_state(text)
    return (f"{path.relative_to(ROOT)}: archive index stale ({blocks} block(s), {lines} index line(s))"
            f" — run memory.py index {slug}")


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

    if ROOT_CHANGELOG.exists():
        _, entries = split_entries(ROOT_CHANGELOG.read_text(encoding="utf-8"))
        if len(entries) > CHANGELOG_KEEP:
            errors.append(f"{ROOT_CHANGELOG.relative_to(ROOT)}: {len(entries)} entries > keep {CHANGELOG_KEEP} — run memory.py log/rotate")
        if ROOT_CHANGELOG.stat().st_size > CHANGELOG_SOFT_CAP:
            warns.append(f"{ROOT_CHANGELOG.relative_to(ROOT)}: {ROOT_CHANGELOG.stat().st_size} B > {CHANGELOG_SOFT_CAP} B")

    root_archive = ROOT_CHANGELOG.with_name("changelog-archive.md")
    if root_archive.exists():
        stale = stale_index_warning(root_archive, "repo")
        if stale:
            warns.append(stale)

    for proj in sorted(p for p in PROJECTS.glob("*") if p.is_dir()) if PROJECTS.is_dir() else []:
        rel = proj.relative_to(ROOT)
        if is_pii(proj):
            warns.append(f"{rel}/: PII path, skipped (never rotated or distilled)")
            continue
        changelog = proj / "changelog.md"
        if changelog.exists():
            _, entries = split_entries(changelog.read_text(encoding="utf-8"))
            if len(entries) > CHANGELOG_KEEP:
                errors.append(f"{rel}/changelog.md: {len(entries)} entries > keep {CHANGELOG_KEEP} — run memory.py log/rotate")
        for name, cap in DISTILL_CAPS.items():
            f = proj / name
            if f.exists() and f.stat().st_size > cap:
                warns.append(f"{rel}/{name}: {f.stat().st_size} B > {cap} B — candidate for memory.py distill")
        for _src, archive_name, _title, _order in DISTILL_FILES.values():
            archive = proj / archive_name
            if archive.exists():
                stale = stale_index_warning(archive, proj.name)
                if stale:
                    warns.append(stale)
        pending = load_manifest(proj / DISTILL_DIR)
        if pending and not pending.get("applied"):
            warns.append(f"{rel}/{DISTILL_DIR}/: pending distill package — fill synthesis.md, then memory.py distill {proj.name} --apply")

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

    s = sub.add_parser("distill", help="report files over caps; --prepare/--apply run the fold")
    s.add_argument("slug")
    mode = s.add_mutually_exclusive_group()
    mode.add_argument("--prepare", action="store_true", help=f"write the fold package to projects/<slug>/{DISTILL_DIR}/")
    mode.add_argument("--apply", nargs="?", const="", metavar="PATH", help="apply a prepared package (default: the project's own)")
    s.add_argument("--file", choices=sorted(DISTILL_FILES), help="which block log to fold (with --prepare)")
    s.set_defaults(func=cmd_distill)

    s = sub.add_parser("index", help="rebuild and list the cold-layer archive index (grep-first entry point)")
    s.add_argument("slug", help="project slug, or 'repo' for .ai/changelog-archive.md")
    s.set_defaults(func=cmd_index)

    s = sub.add_parser("doctor", help="cap + structure checks (exit 1 on errors)")
    s.set_defaults(func=cmd_doctor)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
