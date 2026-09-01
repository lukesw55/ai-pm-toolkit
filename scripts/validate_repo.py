#!/usr/bin/env python3
"""
validate_repo.py — fast structural validator for the ai-pm-toolkit repo.

Checks:
- SKILL.md YAML frontmatter.
- Local markdown links.
- WORKFLOW.md stage table parses into the canonical stage contract.
- .claude/settings.json hook shape for known Claude Code events.
- Hook shell syntax.
- Memory bootstrap contract: init_context.py creates an ACTIVE pointer that
  memory.py doctor and stage_context.py can read.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency in some installs
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".claude" / "skills"
HOOKS = ROOT / "hooks"
STAGES = {
    "discovery-prioritization",
    "impact-brief",
    "discovery",
    "one-pager",
    "product-prioritization",
    "prd",
    "tech-kickoff",
    "delivery",
}
CLAUDE_EVENTS_WITHOUT_MATCHER = {"SessionStart", "UserPromptSubmit", "Stop"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def err(errors: list[str], message: str) -> None:
    errors.append(message)


def warn(warnings: list[str], message: str) -> None:
    warnings.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        err(errors, f"{rel(path)}: missing YAML frontmatter")
        return {}
    raw = match.group(1)
    if yaml is not None:
        try:
            data = yaml.safe_load(raw) or {}
        except Exception as exc:
            err(errors, f"{rel(path)}: invalid YAML frontmatter: {exc}")
            return {}
    else:
        # Minimal fallback: enough to catch missing name/description.
        data = {}
        for line in raw.splitlines():
            m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if m:
                data[m.group(1)] = m.group(2)
    if not data.get("name"):
        err(errors, f"{rel(path)}: frontmatter missing name")
    if not data.get("description"):
        err(errors, f"{rel(path)}: frontmatter missing description")
    return data


def check_skill_frontmatter(errors: list[str]) -> None:
    for path in [ROOT / "SKILL.md", *SKILLS.glob("*/SKILL.md")]:
        parse_frontmatter(path, errors)


def check_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", "workspace"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            link = m.group(1).strip().split("#", 1)[0]
            if not link or link.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):
                continue
            target = (path.parent / link).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if not target.exists():
                err(errors, f"{rel(path)}: broken local link -> {link}")


def check_workflow_contract(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import stage_context  # type: ignore
    except Exception as exc:
        err(errors, f"scripts/stage_context.py: import failed: {exc}")
        return
    contract = stage_context.load_stage_contract(SKILLS / "WORKFLOW.md")
    missing = sorted(STAGES - set(contract))
    if missing:
        err(errors, f".claude/skills/WORKFLOW.md: stage table missing parsed stages: {', '.join(missing)}")
    for stage, row in contract.items():
        for key in ("pm", "reference", "artefact", "gate"):
            if not row.get(key):
                err(errors, f".claude/skills/WORKFLOW.md: {stage} missing {key}")


def check_settings(errors: list[str], warnings: list[str]) -> None:
    path = ROOT / ".claude" / "settings.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        err(errors, f"{rel(path)}: invalid JSON: {exc}")
        return
    hooks = data.get("hooks", {})
    for event, blocks in hooks.items():
        if event in CLAUDE_EVENTS_WITHOUT_MATCHER:
            for idx, block in enumerate(blocks):
                if "matcher" in block:
                    err(errors, f"{rel(path)}: {event}[{idx}] must not use matcher")
        for idx, block in enumerate(blocks):
            for hook in block.get("hooks", []):
                timeout = hook.get("timeout")
                if isinstance(timeout, (int, float)) and timeout > 120:
                    err(errors, f"{rel(path)}: timeout {timeout} on {event}[{idx}] looks like milliseconds; use seconds")
                command = hook.get("command", "")
                target = re.search(r"hooks/[\w.-]+\.sh", command)
                if target and not (ROOT / target.group(0)).exists():
                    err(errors, f"{rel(path)}: missing hook command target {target.group(0)}")


def check_hook_syntax(errors: list[str], warnings: list[str]) -> None:
    if shutil.which("bash") is None:
        warn(warnings, "bash not found; skipped hook syntax checks")
        return
    for path in sorted(HOOKS.glob("*.sh")):
        # Relative POSIX path: a native Windows path (C:\...) loses its
        # backslashes when Git Bash parses the argument.
        res = subprocess.run(
            ["bash", "-n", path.relative_to(ROOT).as_posix()],
            cwd=ROOT, text=True, capture_output=True,
        )
        if res.returncode != 0:
            err(errors, f"{rel(path)}: bash -n failed: {res.stderr.strip()}")


def check_memory_bootstrap(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="ai-pm-validate-") as td:
        tmp = Path(td) / ROOT.name
        # "memory" / "gates" exclude .ai/memory and .ai/gates: local session state
        # (an active project, sentinel flags) that must not leak into the
        # fresh-clone bootstrap simulation below.
        ignore = shutil.ignore_patterns(".git", "workspace", "memory", "gates")
        shutil.copytree(ROOT, tmp, ignore=ignore)
        py = sys.executable  # "python3" is not on PATH in every environment (e.g. Windows)
        cmds = [
            [py, "scripts/init_context.py", "Validation Demo"],
            [py, "scripts/memory.py", "doctor"],
            [py, "scripts/stage_context.py"],
        ]
        for cmd in cmds:
            res = subprocess.run(cmd, cwd=tmp, text=True, capture_output=True)
            if res.returncode != 0:
                err(errors, f"{' '.join(cmd)} failed: {res.stderr.strip() or res.stdout.strip()}")
                return
        out = subprocess.run([py, "scripts/stage_context.py"], cwd=tmp, text=True, capture_output=True).stdout
        if "## Inputs" not in out or "## Output / gate" not in out:
            err(errors, "scripts/stage_context.py: did not emit rich stage contract after init_context.py")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    check_skill_frontmatter(errors)
    check_markdown_links(errors)
    check_workflow_contract(errors)
    check_settings(errors, warnings)
    check_hook_syntax(errors, warnings)
    check_memory_bootstrap(errors)

    for item in warnings:
        print(f"WARN  {item}")
    for item in errors:
        print(f"ERROR {item}")

    if errors:
        print(f"\nvalidate_repo: failed ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"validate_repo: all green ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
