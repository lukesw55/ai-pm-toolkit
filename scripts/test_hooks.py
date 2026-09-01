#!/usr/bin/env python3
"""
test_hooks.py — synthetic-payload smoke suite for the shared gates and the
Codex apply_patch adapter.

Every case sends a fake tool-call payload to the real hook script over
stdin and checks the exit code (and, where it matters, that a per-content
sentinel actually unlocks a previously-blocked call). Nothing here talks
to a live Claude Code or Codex session — it exercises exactly what those
harnesses would pipe into these scripts.

Usage: python3 scripts/test_hooks.py
Exits 0 if every case matches its expected outcome, 1 otherwise (with a
per-case PASS/FAIL report on stdout).
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS = ROOT / "hooks"
CODEX_ADAPTER = ROOT / ".codex" / "adapters" / "pretooluse.py"


def run(cmd: list[str], stdin_text: str, cwd: Path = ROOT) -> tuple[int, str, str]:
    res = subprocess.run(cmd, input=stdin_text.encode(), capture_output=True, cwd=cwd)
    return res.returncode, res.stdout.decode(errors="replace"), res.stderr.decode(errors="replace")


def payload(**kwargs) -> str:
    return json.dumps(kwargs)


def pretool_block(adapter: Path, command_fragment: str) -> dict:
    data = json.loads(adapter.read_text(encoding="utf-8"))
    return next(
        block for block in data["hooks"]["PreToolUse"]
        if any(command_fragment in hook.get("command", "") for hook in block.get("hooks", []))
    )


CASES: list[tuple[str, list[str], str, int]] = []


def case(name: str, cmd: list[str], stdin_text: str, expect_exit: int) -> None:
    CASES.append((name, cmd, stdin_text, expect_exit))


# -- anti-slop-gate.sh ---------------------------------------------------
case(
    "anti-slop: forbidden basename on Write blocks",
    ["bash", str(HOOKS / "anti-slop-gate.sh")],
    payload(tool_name="Write", tool_input={"file_path": "/tmp/x/NOTES.md", "content": "unmarked forbidden-basename test content 4471"}),
    2,
)
case(
    "anti-slop: clean Write passes",
    ["bash", str(HOOKS / "anti-slop-gate.sh")],
    payload(tool_name="Write", tool_input={"file_path": "/tmp/x/clean-unique-9182.md", "content": "nothing wrong here"}),
    0,
)

# -- inference-discipline-gate.sh ----------------------------------------
_marker = f"[{'UNVERIFIED'}: launch date]"  # built at runtime so this file itself never carries the literal
case(
    "inference-discipline: unresolved marker blocks",
    ["bash", str(HOOKS / "inference-discipline-gate.sh")],
    payload(tool_name="Write", tool_input={"file_path": "/tmp/x/doc.md", "content": f"claim {_marker}"}),
    2,
)
# B1: MCP tool-name case arms match by suffix now, so both the bare prefix
# (mcp__<Server>__<tool>) and the claude_ai_-prefixed one must be recognised
# — the matcher in settings.json/hooks.json decides *whether* this hook runs
# at all; these two cases confirm the content-scanning logic itself doesn't
# silently go inert on either prefix once it does.
case(
    "inference-discipline: bare-prefix MCP tool name recognised",
    ["bash", str(HOOKS / "inference-discipline-gate.sh")],
    payload(tool_name="mcp__Atlassian_Rovo__createConfluencePage", tool_input={"title": "t", "body": f"claim {_marker}"}),
    2,
)
case(
    "inference-discipline: claude_ai_-prefixed MCP tool name recognised",
    ["bash", str(HOOKS / "inference-discipline-gate.sh")],
    payload(tool_name="mcp__claude_ai_Atlassian_Rovo__createConfluencePage", tool_input={"title": "t", "body": f"claim {_marker}"}),
    2,
)
case(
    "inference-discipline: skip-path for shared hooks/*.sh",
    ["bash", str(HOOKS / "inference-discipline-gate.sh")],
    payload(tool_name="Write", tool_input={"file_path": str(HOOKS / "foo.sh"), "content": f"claim {_marker}"}),
    0,
)

# -- humanize-gate.sh ------------------------------------------------------
_humanize_body = "a prose body long enough to be the sentinel target for this test case"
case(
    "humanize-gate: unmarked publish blocks",
    ["bash", str(HOOKS / "humanize-gate.sh")],
    payload(tool_name="mcp__claude_ai_Slack__slack_send_message", tool_input={"channel": "C1", "text": _humanize_body}),
    2,
)
case(
    "humanize-gate: bare-prefix unmarked publish blocks",
    ["bash", str(HOOKS / "humanize-gate.sh")],
    payload(tool_name="mcp__Slack__slack_send_message", tool_input={"channel": "C1", "text": _humanize_body}),
    2,
)

# -- scope-bloat-gate.sh: both harness input shapes -----------------------
case(
    "scope-bloat: Codex last_assistant_message shape, clean reply passes",
    ["bash", str(HOOKS / "scope-bloat-gate.sh")],
    json.dumps({"stop_hook_active": False, "last_assistant_message": "Short, direct reply."}),
    0,
)
case(
    "scope-bloat: Codex shape, label-colon bullet run blocks",
    ["bash", str(HOOKS / "scope-bloat-gate.sh")],
    json.dumps({
        "stop_hook_active": False,
        "last_assistant_message": "padding " * 60 + "\n" + "\n".join(f"- **Item {i}**: description of item {i}" for i in range(1, 6)),
    }),
    2,
)

# -- .codex/adapters/pretooluse.py: apply_patch normalization -------------
_ADD_CLEAN = "*** Begin Patch\n*** Add File: /tmp/x/added-9182.md\n+clean content\n*** End Patch"
_ADD_FORBIDDEN = "*** Begin Patch\n*** Add File: /tmp/x/PLAN.md\n+plan content\n*** End Patch"
_UPDATE_MARKER = f"*** Begin Patch\n*** Update File: /tmp/x/doc.md\n@@\n context line\n-old line\n+claim {_marker}\n*** End Patch"
_DELETE = "*** Begin Patch\n*** Delete File: /tmp/x/gone.md\n*** End Patch"
_MALFORMED = "this is not a patch at all"

case(
    "codex adapter: clean Add File passes",
    ["python3", str(CODEX_ADAPTER)],
    payload(tool_name="apply_patch", tool_input={"command": _ADD_CLEAN}),
    0,
)
case(
    "codex adapter: Add File with forbidden basename blocks",
    ["python3", str(CODEX_ADAPTER)],
    payload(tool_name="apply_patch", tool_input={"command": _ADD_FORBIDDEN}),
    2,
)
case(
    "codex adapter: Update File introducing an inference marker blocks",
    ["python3", str(CODEX_ADAPTER)],
    payload(tool_name="apply_patch", tool_input={"command": _UPDATE_MARKER}),
    2,
)
case(
    "codex adapter: Delete File has nothing to scan, passes",
    ["python3", str(CODEX_ADAPTER)],
    payload(tool_name="apply_patch", tool_input={"command": _DELETE}),
    0,
)
case(
    "codex adapter: unparseable patch fails closed (never silently allowed)",
    ["python3", str(CODEX_ADAPTER)],
    payload(tool_name="apply_patch", tool_input={"command": _MALFORMED}),
    2,
)
case(
    "codex adapter: out-of-scope tool_name is a defensive no-op",
    ["python3", str(CODEX_ADAPTER)],
    payload(tool_name="Bash", tool_input={"command": "ls"}),
    0,
)


def run_cases() -> int:
    failures = 0
    for name, cmd, stdin_text, expect in CASES:
        code, _out, err = run(cmd, stdin_text)
        ok = code == expect
        print(f"{'PASS' if ok else 'FAIL'}  {name}  (exit {code}, expected {expect})")
        if not ok:
            failures += 1
            if err:
                print("  stderr:", err.strip().splitlines()[0] if err.strip() else "(empty)")

    # Sentinel round-trip: block, mark, confirm unlock — exercises the
    # override mechanism the gates document, not just the block path.
    unique_content = "sentinel round-trip content for test_hooks.py"
    code, _, _ = run(
        ["bash", str(HOOKS / "anti-slop-gate.sh")],
        payload(tool_name="Write", tool_input={"file_path": "/tmp/x/PLAN.md", "content": unique_content}),
    )
    blocked_first = code == 2
    subprocess.run(["bash", str(HOOKS / "anti-slop-mark.sh"), unique_content], capture_output=True, cwd=ROOT)
    code, _, _ = run(
        ["bash", str(HOOKS / "anti-slop-gate.sh")],
        payload(tool_name="Write", tool_input={"file_path": "/tmp/x/PLAN.md", "content": unique_content}),
    )
    unlocked = code == 0
    ok = blocked_first and unlocked
    print(f"{'PASS' if ok else 'FAIL'}  sentinel round-trip: block -> mark -> unlock via .ai/gates/")
    if not ok:
        failures += 1
    flag_dir = ROOT / ".ai" / "gates" / "anti-slop"
    flag_path = flag_dir / f"{hashlib.sha256(unique_content.encode()).hexdigest()}.flag"
    if flag_path.exists():
        flag_path.unlink()

    # B1: both adapters must use the exact same publish matcher. Prove that
    # it accepts both supported prefixes and excludes an unrelated tool.
    try:
        claude_publish = pretool_block(ROOT / ".claude" / "settings.json", "humanize-gate.sh")["matcher"]
        codex_publish = pretool_block(ROOT / ".codex" / "hooks.json", "humanize-gate.sh")["matcher"]
        representative_tools = [
            "mcp__Atlassian_Rovo__createConfluencePage",
            "mcp__claude_ai_Atlassian_Rovo__createConfluencePage",
            "mcp__Slack__slack_send_message",
            "mcp__claude_ai_Slack__slack_send_message",
        ]
        ok = (
            claude_publish == codex_publish
            and all(re.fullmatch(claude_publish, tool) for tool in representative_tools)
            and re.fullmatch(claude_publish, "mcp__GitHub__create_pull_request") is None
        )
        print(f"{'PASS' if ok else 'FAIL'}  publish matchers are identical, dual-prefix, and scoped")
        if not ok:
            failures += 1
    except (KeyError, StopIteration, json.JSONDecodeError, re.error) as exc:
        failures += 1
        print(f"FAIL  publish matcher wiring could not be inspected: {exc}")

    # Amendment 4: execute the actual Codex adapter command from hooks.json
    # from a nested cwd, not a lookalike command assembled inside this test.
    nested = ROOT / "skills" / "anti-slop"
    if nested.is_dir():
        try:
            codex_write = pretool_block(ROOT / ".codex" / "hooks.json", "pretooluse.py")
            command = codex_write["hooks"][0]["command"]
            code, _out, err = run(
                ["bash", "-c", command],
                payload(tool_name="apply_patch", tool_input={"command": _ADD_CLEAN}),
                cwd=nested,
            )
            ok = code == 0
            print(f"{'PASS' if ok else 'FAIL'}  actual Codex adapter command resolves from a nested cwd (amendment 4)")
            if not ok:
                failures += 1
                print("  stderr:", err.strip())
        except (KeyError, IndexError, StopIteration, json.JSONDecodeError) as exc:
            failures += 1
            print(f"FAIL  nested-cwd Codex command could not be inspected: {exc}")
    else:
        print("SKIP  nested-cwd test: skills/anti-slop/ not found")

    return failures


def main() -> int:
    failures = run_cases()
    total = len(CASES) + 3  # + sentinel round-trip + matcher parity + nested-cwd
    if failures:
        print(f"\ntest_hooks: {failures}/{total} case(s) failed")
        return 1
    print(f"\ntest_hooks: all {total} case(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
