#!/usr/bin/env python3
"""
pretooluse.py — Codex-only PreToolUse adapter for the shared write gates.

Normalizes Codex's apply_patch tool call into the Write/Edit-shaped stdin
that hooks/anti-slop-gate.sh and hooks/inference-discipline-gate.sh already
consume (documented Codex contract: tool_name is literally "apply_patch",
the patch text is in tool_input.command, exit code 2 blocks the call — see
.codex/hooks.json). This is the ONLY Codex-specific execution adapter in
the repo; MCP publish tool calls already carry tool_name/tool_input in the
same shape Claude Code uses, so .codex/hooks.json invokes the shared gates
for those directly, with no adapter in between.

apply_patch uses the documented V4A patch format:

    *** Begin Patch
    *** Add File: <path>
    +<line>
    *** Update File: <path>
    @@ <optional hunk context>
     <context line>
    -<removed line>
    +<added line>
    *** Delete File: <path>
    *** End Patch

Per file section this script builds a synthetic Write payload (Add File) or
Edit payload (Update File) — old_string/new_string reconstructed from the
hunk — and runs it through both shared gates. Delete File sections have no
new content to scan and are skipped. A patch that fails to parse against
this documented shape is NOT silently allowed through: normalization
failure fails closed, with an actionable stderr message, per the project's
explicit "never fail-open on an unknown shape" rule.

Usage: reads a Codex PreToolUse JSON envelope on stdin, exits 0 to allow
the call or 2 (with the offending gate's stderr) to block it.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GATES = [ROOT / "hooks" / "anti-slop-gate.sh", ROOT / "hooks" / "inference-discipline-gate.sh"]

HEADER_RE = re.compile(r"^\*\*\* (Add File|Update File|Delete File): (.+)$")
ACTION_WORDS = {"Add File": "add", "Update File": "update", "Delete File": "delete"}


class PatchParseError(ValueError):
    pass


def parse_apply_patch(patch_text: str) -> list[dict]:
    """Parse the V4A apply_patch format into per-file sections. Raises
    PatchParseError on anything that doesn't match the documented shape —
    the caller must fail closed on this, never pass the content through
    unchecked."""
    lines = patch_text.splitlines()
    if not lines or lines[0].strip() != "*** Begin Patch":
        raise PatchParseError("missing '*** Begin Patch' sentinel")
    if lines[-1].strip() != "*** End Patch":
        raise PatchParseError("missing '*** End Patch' sentinel")

    body = lines[1:-1]
    sections = []
    i = 0
    while i < len(body):
        m = HEADER_RE.match(body[i])
        if not m:
            raise PatchParseError(f"unrecognized patch line at body index {i}: {body[i]!r}")
        action = ACTION_WORDS[m.group(1)]
        path = m.group(2).strip()
        i += 1
        old_lines: list[str] = []
        new_lines: list[str] = []
        while i < len(body) and not HEADER_RE.match(body[i]):
            line = body[i]
            if line.startswith("*** Move to:") or line.startswith("@@"):
                i += 1
                continue
            if action == "add":
                if not line.startswith("+"):
                    raise PatchParseError(f"Add File {path!r}: non-'+' line {line!r}")
                new_lines.append(line[1:])
            elif action == "update":
                if line.startswith("+"):
                    new_lines.append(line[1:])
                elif line.startswith("-"):
                    old_lines.append(line[1:])
                elif line.startswith(" ") or line == "":
                    context = line[1:] if line.startswith(" ") else line
                    old_lines.append(context)
                    new_lines.append(context)
                else:
                    raise PatchParseError(f"Update File {path!r}: unrecognized hunk line {line!r}")
            # Delete File: body carries no content lines to collect.
            i += 1
        sections.append({
            "path": path,
            "action": action,
            "old_string": "\n".join(old_lines),
            "new_string": "\n".join(new_lines),
        })

    if not sections:
        raise PatchParseError("patch has no file sections")
    return sections


def run_gates(payload: dict) -> tuple[int, str]:
    """Run both shared gates against one synthetic Claude-shape payload.
    Returns (exit_code, combined_stderr) — exit_code 2 on the first gate
    that blocks, 0 if both pass."""
    stdin_bytes = json.dumps(payload).encode()
    for gate in GATES:
        res = subprocess.run(["bash", str(gate)], input=stdin_bytes, capture_output=True)
        if res.returncode != 0:
            return res.returncode, res.stderr.decode(errors="replace")
    return 0, ""


def gate_section(section: dict) -> tuple[int, str]:
    if section["action"] == "delete":
        return 0, ""  # nothing new to scan
    if section["action"] == "add":
        payload = {"tool_name": "Write", "tool_input": {"file_path": section["path"], "content": section["new_string"]}}
    else:
        payload = {
            "tool_name": "Edit",
            "tool_input": {"file_path": section["path"], "old_string": section["old_string"], "new_string": section["new_string"]},
        }
    return run_gates(payload)


def main() -> int:
    raw = sys.stdin.read()
    try:
        envelope = json.loads(raw)
    except Exception as exc:
        print(f"pretooluse adapter: could not parse Codex PreToolUse JSON: {exc}", file=sys.stderr)
        return 2

    tool_name = envelope.get("tool_name", "")
    tool_input = envelope.get("tool_input", {})

    if tool_name in ("Write", "Edit", "NotebookEdit"):
        # Already Claude-shaped (documented as possible in some Codex
        # configurations) — pass straight through, no normalization needed.
        code, stderr = run_gates(envelope)
        if code != 0:
            sys.stderr.write(stderr)
        return code

    if tool_name != "apply_patch":
        # Not a write-shaped tool this adapter knows how to gate — allow
        # (the matcher in .codex/hooks.json should not route anything else
        # here; this is a defensive default, not a silent bypass of a
        # write we failed to recognize).
        return 0

    patch_text = tool_input.get("command", "")
    try:
        sections = parse_apply_patch(patch_text)
    except PatchParseError as exc:
        # D4 / owner amendment 1: normalization failure fails CLOSED with
        # an actionable message — never silently let an unparsed patch
        # through the write gates.
        print(
            "pretooluse adapter: BLOCKED — apply_patch content did not match the "
            f"documented V4A format ({exc}). This normalizer cannot verify the "
            "patch against anti-slop / inference-discipline without a parse. "
            "Split the change into a patch apply_patch actually generates, or "
            "report this shape mismatch so the adapter can be extended.",
            file=sys.stderr,
        )
        return 2

    for section in sections:
        code, stderr = gate_section(section)
        if code != 0:
            sys.stderr.write(f"[{section['path']}] ")
            sys.stderr.write(stderr)
            return code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
