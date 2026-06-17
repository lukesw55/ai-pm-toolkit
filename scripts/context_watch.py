#!/usr/bin/env python3
"""
context_watch.py — live CLI view of the active context plus time spent per context.

Usage:
    python3 scripts/context_watch.py            # watch: live line, refreshes every 1s
    python3 scripts/context_watch.py status     # one-shot line (scriptable / statusline)
    python3 scripts/context_watch.py report     # accumulated time per context

Reads the pointer (.ai/memory/active-context.md) and the transition log
(.ai/memory/context-events.jsonl). memory.py park/activate append exact-time
events; the watcher also records changes it observes while running (covers
manual pointer edits). Time is wall-clock between activate and the next
park/activate — it measures "context held", including idle hours.
"""

import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POINTER = ROOT / ".ai" / "memory" / "active-context.md"
EVENTS = ROOT / ".ai" / "memory" / "context-events.jsonl"


def read_pointer():
    if not POINTER.exists():
        sys.exit("context_watch.py: active-context.md missing")
    text = POINTER.read_text()
    m = re.search(r"(?m)^## ACTIVE: `([a-z0-9\-]+)` \(set (\d{4}-\d{2}-\d{2})\)", text)
    if not m:
        return None, None, None
    stage = re.search(r"(?m)Current\s+stage\*{0,2}\s*:\s*(\S+)", text)
    return m.group(1), stage.group(1) if stage else "?", m.group(2)


def load_events():
    if not EVENTS.exists():
        return []
    return [json.loads(line) for line in EVENTS.read_text().splitlines() if line.strip()]


def append_event(slug, ts=None):
    ts = ts or datetime.now().astimezone().isoformat(timespec="seconds")
    with EVENTS.open("a") as f:
        f.write(json.dumps({"ts": ts, "slug": slug}) + "\n")


def sync_log(slug, set_date):
    """Make the log's tail agree with the pointer. Empty log gets seeded with the
    pointer's set-date at 00:00 (best info available); otherwise the change is
    stamped now."""
    events = load_events()
    if events and events[-1]["slug"] == slug:
        return events
    if not events and slug and set_date:
        seed = datetime.fromisoformat(f"{set_date}T00:00:00").astimezone()
        append_event(slug, seed.isoformat(timespec="seconds"))
    else:
        append_event(slug)
    return load_events()


def totals(events, now):
    """Per-slug seconds: each event owns the interval until the next one."""
    acc = {}
    closes = events[1:] + [{"ts": now.isoformat(timespec="seconds"), "slug": None}]
    for ev, nxt in zip(events, closes):
        if ev["slug"]:
            secs = (datetime.fromisoformat(nxt["ts"]) - datetime.fromisoformat(ev["ts"])).total_seconds()
            acc[ev["slug"]] = acc.get(ev["slug"], 0) + max(secs, 0)
    return acc


def fmt(secs):
    secs = int(secs)
    days, rest = divmod(secs, 86400)
    h, rest = divmod(rest, 3600)
    m, s = divmod(rest, 60)
    return (f"{days}d " if days else "") + f"{h:02d}:{m:02d}:{s:02d}"


def render(slug, stage, events, now):
    if slug is None:
        return "○ nenhum contexto ativo"
    since = datetime.fromisoformat(events[-1]["ts"])
    total = totals(events, now).get(slug, 0)
    return f"● {slug} [{stage}]  ativo {fmt((now - since).total_seconds())}  |  total {fmt(total)}"


def cmd_watch():
    slug, stage, set_date = read_pointer()
    events = sync_log(slug, set_date)
    try:
        while True:
            cur, stage, set_date = read_pointer()
            if cur != slug:
                append_event(cur)
                slug = cur
                events = load_events()
            print(f"\r\033[K{render(slug, stage, events, datetime.now().astimezone())}", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print()


def cmd_status():
    slug, stage, set_date = read_pointer()
    events = sync_log(slug, set_date)
    print(render(slug, stage, events, datetime.now().astimezone()))


def cmd_report():
    slug, _, set_date = read_pointer()
    events = sync_log(slug, set_date)
    now = datetime.now().astimezone()
    for s, secs in sorted(totals(events, now).items(), key=lambda kv: -kv[1]):
        mark = "  ← ativo" if s == slug else ""
        print(f"{s:50s} {fmt(secs):>12s}{mark}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "watch"
    {"watch": cmd_watch, "status": cmd_status, "report": cmd_report}.get(
        cmd, lambda: sys.exit(f"context_watch.py: unknown command '{cmd}' (watch|status|report)")
    )()
