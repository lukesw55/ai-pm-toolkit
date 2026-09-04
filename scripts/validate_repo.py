#!/usr/bin/env python3
"""
validate_repo.py — fast structural validator for the ai-pm-toolkit repo.

Checks:
- SKILL.md YAML frontmatter (canonical skills/ only — mirrors are generated).
- Local markdown links (canonical + repo docs; mirrors excluded — they are
  byte copies, so a broken link there is the same broken link in canonical).
- Backtick-quoted file paths (`a/b.md`), resolved from the citing file's own
  directory, `skills/`, the citing skill's root, or the repo root.
- WORKFLOW.md stage table parses into the canonical stage contract.
- .claude/settings.json and .codex/hooks.json hook shape and command targets.
- Hook shell syntax, and that shared hooks/*.sh carry no harness-specific paths
  dependency (D4: shared enforcement logic must be harness-neutral).
- Mirror drift: .claude/skills/ and .agents/skills/ match skills/ exactly.
- GitHub custom agents in .github/agents/: frontmatter schema, tool aliases,
  delegation consistency, and one shared required-reading contract.
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
SKILLS = ROOT / "skills"
MIRRORS = [ROOT / ".claude" / "skills", ROOT / ".agents" / "skills"]
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
EVAL_CATEGORIES = {"standard", "doctrine-adversarial", "skill-functional-adversarial", "negative-control"}
AGENTS_DIR = ROOT / ".github" / "agents"
# Canonical tool aliases this repo allows. GitHub matches aliases
# case-insensitively and also accepts the compatible names below, so a
# non-canonical spelling is a policy finding here, never a claim that GitHub
# would reject it.
AGENT_TOOL_ALIASES = {"execute", "read", "edit", "search", "agent", "web", "todo"}
# Compatible names GitHub recognises, keyed lowercase, mapped to the canonical
# alias that must replace them (from the custom-agents configuration reference).
AGENT_TOOL_COMPATIBLE = {
    "shell": "execute",
    "bash": "execute",
    "powershell": "execute",
    "notebookread": "read",
    "multiedit": "edit",
    "write": "edit",
    "notebookedit": "edit",
    "grep": "search",
    "glob": "search",
    "custom-agent": "agent",
    "task": "agent",
    "websearch": "web",
    "webfetch": "web",
    "todowrite": "todo",
}
# MCP tools are `server/tool` or `server/*`; anything else with a slash is
# malformed rather than a namespace this validator does not know.
AGENT_MCP_TOOL = re.compile(r"^[A-Za-z0-9._-]+/([A-Za-z0-9._-]+|\*)$")
AGENT_READING_HEADING = "## Required reading"
AGENT_CORE_READING = (".ai/rules.md", ".ai/app.md", ".ai/memory/active-context.md")
# Project memory has to be named on its own: the core set already contains the
# string "memory" via active-context.md, so a substring test would never fire.
AGENT_PROJECT_MEMORY = re.compile(r"project memory|project's memory|\.ai/memory/projects/", re.I)
CLAUDE_EVENTS_WITHOUT_MATCHER = {"SessionStart", "UserPromptSubmit", "Stop"}
# Codex's SessionStart accepts a `source` matcher (startup|resume|clear|compact),
# unlike Claude Code's — only these two are confirmed matcher-less in Codex.
CODEX_EVENTS_WITHOUT_MATCHER = {"UserPromptSubmit", "Stop"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def err(errors: list[str], message: str) -> None:
    errors.append(message)


def warn(warnings: list[str], message: str) -> None:
    warnings.append(message)


class Unparsed:
    """A frontmatter value the no-PyYAML fallback could not interpret.

    Only the checks that actually validate a field turn this into a finding,
    so a tolerated nested mapping such as `metadata:` stays silent while a
    validated field in an unsupported form is reported once.
    """

    __slots__ = ("raw",)

    def __init__(self, raw: str) -> None:
        self.raw = raw

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return f"Unparsed({self.raw!r})"


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_inline_list(value: str):
    """`[a, b]` -> ["a", "b"], matching PyYAML on the forms this repo uses.

    A trailing comma is dropped, because YAML reads `[a, ]` as ["a"]. An empty
    item anywhere else, or an item opened with a quote it never closes, is
    Unparsed — both raise in PyYAML too, so the two modes agree.
    """
    inner = value[1:-1].strip()
    if not inner:
        return []
    items = [item.strip() for item in inner.split(",")]
    if items and items[-1] == "":
        items.pop()
    out = []
    for item in items:
        if not item:
            return Unparsed(value)
        if item[0] in "\"'" and (len(item) < 2 or item[-1] != item[0]):
            return Unparsed(value)
        out.append(unquote(item))
    return out


def fold_block_scalar(indicator: str, lines: list[str]) -> str:
    """Join the indented body of a `>`/`|` block scalar.

    Folded (`>`) joins lines with spaces and paragraph breaks with a newline;
    literal (`|`) keeps the line breaks. Chomping (`-`/`+`) only affects
    trailing newlines, which no validated field depends on, so the result is
    stripped either way.
    """
    if indicator.startswith("|"):
        return "\n".join(line.strip() for line in lines).strip()
    paragraphs: list[list[str]] = [[]]
    for line in lines:
        if line.strip():
            paragraphs[-1].append(line.strip())
        elif paragraphs[-1]:
            paragraphs.append([])
    return "\n".join(" ".join(par) for par in paragraphs if par).strip()


def fallback_frontmatter(raw: str) -> dict:
    """Parse the canonical frontmatter subset this repo uses, without PyYAML.

    Covers plain scalars, inline lists, booleans and block scalars. A nested
    mapping (`metadata:`) is recognised and kept as Unparsed rather than
    guessed at: nothing validates it, so tolerating it is explicit instead of
    accidental. This is not a YAML parser, and anything outside the subset
    becomes Unparsed so a validated field cannot pass unread.
    """
    data: dict = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        match = re.match(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$", lines[i])
        if not match:
            i += 1
            continue
        key, value = match.group(1), match.group(2).strip()
        i += 1
        if re.fullmatch(r"[>|][-+]?", value):
            body = []
            while i < len(lines) and (not lines[i].strip() or lines[i][:1] in " \t"):
                body.append(lines[i])
                i += 1
            data[key] = fold_block_scalar(value, body)
        elif value == "":
            nested = []
            while i < len(lines) and (not lines[i].strip() or lines[i][:1] in " \t"):
                nested.append(lines[i])
                i += 1
            data[key] = Unparsed("nested block") if any(l.strip() for l in nested) else ""
        elif value.startswith("[") and value.endswith("]"):
            data[key] = parse_inline_list(value)
        elif value.lower() in ("true", "false"):
            data[key] = value.lower() == "true"
        else:
            data[key] = unquote(value)
    return data


def load_frontmatter(path: Path, errors: list[str]) -> tuple[dict | None, str]:
    """Split and interpret YAML frontmatter — the one parsing routine.

    Returns the mapping and the body after the closing `---`. None means the
    frontmatter is missing or unparseable and the caller already has a finding.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        err(errors, f"{rel(path)}: missing YAML frontmatter")
        return None, text
    body = text[match.end():]
    if yaml is not None:
        try:
            data = yaml.safe_load(match.group(1)) or {}
        except Exception as exc:
            err(errors, f"{rel(path)}: invalid YAML frontmatter: {exc}")
            return None, body
    else:
        data = fallback_frontmatter(match.group(1))
    if not isinstance(data, dict):
        err(errors, f"{rel(path)}: frontmatter must be a mapping, got {type(data).__name__}")
        return None, body
    return data, body


def unsupported(errors: list[str], path: Path, key: str, value) -> bool:
    """Report a validated field the no-PyYAML fallback could not read.

    One finding per field, and the caller stops validating that field so the
    message does not stack with a type error about the same value.
    """
    if isinstance(value, Unparsed):
        err(
            errors,
            f"{rel(path)}: `{key}` is {value.raw}, outside the frontmatter subset the "
            f"no-PyYAML mode supports (scalars, inline lists, booleans, block scalars)",
        )
        return True
    return False


def parse_frontmatter(path: Path, errors: list[str]) -> dict:
    data, _ = load_frontmatter(path, errors)
    if data is None:
        return {}
    for key in ("name", "description"):
        value = data.get(key)
        if unsupported(errors, path, key, value):
            continue
        if not value:
            err(errors, f"{rel(path)}: frontmatter missing {key}")
    return data


def check_skill_frontmatter(errors: list[str]) -> None:
    for path in [ROOT / "SKILL.md", *SKILLS.glob("*/SKILL.md")]:
        parse_frontmatter(path, errors)


def check_markdown_links(errors: list[str]) -> None:
    mirror_prefixes = tuple(str(m) for m in MIRRORS)
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", "workspace"} for part in path.parts):
            continue
        if str(path).startswith(mirror_prefixes):
            continue  # generated byte copies of skills/; drift-checked separately
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


# Repo files cited in backticks (`a/b.md`) are far more common in this tree
# than [text](link) and are invisible to check_markdown_links (B14).
PATH_EXTS = ("md", "py", "sh", "json", "yml", "yaml", "jsonl", "txt")
BACKTICK_PATH = re.compile(r"`([^`\s]*/[^`\s]*?\.(?:" + "|".join(PATH_EXTS) + r"))(?:#[^`\s]*)?`")
PLACEHOLDER_CHARS = set("<>*~|\\{}")  # <slug>, globs, home dirs: shapes, not files
# Logs cite paths as they were when the entry was written; not a live contract.
HISTORICAL_DOCS = {".ai/backlog.md", ".ai/changelog.md"}
# Runtime memory and gate state are gitignored by design: absent on a fresh
# clone, present locally. A token pointing there must not change the verdict —
# except the tracked skeleton, which does exist on a fresh clone.
RUNTIME_PREFIXES = (".ai/memory/", ".ai/gates/")
TRACKED_MEMORY = (".ai/memory/_templates/", ".ai/memory/README.md", ".ai/memory/active-context.example.md")
# Per-skill conventional files cited generically ("every skill ships an
# evals/evals.json"), not as a path into one specific skill.
GENERIC_PATHS = {"evals/evals.json"}


def _path_bases(path: Path, token: str) -> list[Path]:
    """Explicitly relative tokens (./ ../) resolve only from the citing file's
    own directory, exactly like a markdown link. A bare token may instead be
    skills/-relative (`pm-phase-define/references/x.md`, the convention for
    cross-skill citations), skill-root-relative (`references/x.md` cited from
    within that same skill's references/ file), or repo-root-relative
    (`scripts/memory.py`) — the conventions the tree actually uses."""
    if token.startswith(("./", "../")):
        return [path.parent]
    bases = [path.parent, SKILLS, ROOT]
    try:
        parts = path.relative_to(SKILLS).parts
    except ValueError:
        return bases
    if len(parts) > 1:
        bases.insert(2, SKILLS / parts[0])
    return bases


def check_backtick_paths(errors: list[str]) -> None:
    """B14: a renamed or relocated reference goes stale silently when cited
    in backticks instead of a markdown link — check_markdown_links never
    sees it. Same file set as check_markdown_links, minus runtime memory
    (gitignored, absent on a fresh clone) and historical logs."""
    mirror_prefixes = tuple(str(m) for m in MIRRORS)
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", "workspace"} for part in path.parts) or str(path).startswith(mirror_prefixes):
            continue
        rel_path = path.relative_to(ROOT).as_posix()
        if rel_path in HISTORICAL_DOCS:
            continue
        if rel_path.startswith(".ai/memory/") and not rel_path.startswith(TRACKED_MEMORY):
            continue  # local memory content itself, not tracked
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in BACKTICK_PATH.finditer(text):
            token = m.group(1)
            if (PLACEHOLDER_CHARS & set(token) or "..." in token or token.startswith("/")
                    or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", token) or token in GENERIC_PATHS):
                continue
            if token.startswith(RUNTIME_PREFIXES) and not token.startswith(TRACKED_MEMORY):
                continue
            if not any((base / token).exists() for base in _path_bases(path, token)):
                line = text.count("\n", 0, m.start()) + 1
                err(errors, f"{rel_path}:{line}: backtick path not found -> {token}")


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
        err(errors, f"skills/WORKFLOW.md: stage table missing parsed stages: {', '.join(missing)}")
    for stage, row in contract.items():
        for key in ("pm", "reference", "artefact", "gate"):
            if not row.get(key):
                err(errors, f"skills/WORKFLOW.md: {stage} missing {key}")


def _check_hook_wiring(path: Path, events_without_matcher: set[str], errors: list[str]) -> None:
    """Shared shape checks for a harness's hook-wiring file (Claude Code's
    .claude/settings.json or Codex's .codex/hooks.json): valid JSON, no
    matcher on events that don't support one, sane timeouts, and every
    referenced hooks/*.sh or .codex/adapters/*.py command target exists."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        err(errors, f"{rel(path)}: invalid JSON: {exc}")
        return
    hooks = data.get("hooks", {})
    for event, blocks in hooks.items():
        if event in events_without_matcher:
            for idx, block in enumerate(blocks):
                if "matcher" in block:
                    err(errors, f"{rel(path)}: {event}[{idx}] must not use matcher")
        for idx, block in enumerate(blocks):
            for hook in block.get("hooks", []):
                timeout = hook.get("timeout")
                if isinstance(timeout, (int, float)) and timeout > 120:
                    err(errors, f"{rel(path)}: timeout {timeout} on {event}[{idx}] looks like milliseconds; use seconds")
                command = hook.get("command", "")
                target = re.search(r"(hooks/[\w.-]+\.sh|\.codex/adapters/[\w.-]+\.py)", command)
                if target and not (ROOT / target.group(0)).exists():
                    err(errors, f"{rel(path)}: missing hook command target {target.group(0)}")


def check_settings(errors: list[str], warnings: list[str]) -> None:
    _check_hook_wiring(ROOT / ".claude" / "settings.json", CLAUDE_EVENTS_WITHOUT_MATCHER, errors)


def check_codex_hooks(errors: list[str], warnings: list[str]) -> None:
    path = ROOT / ".codex" / "hooks.json"
    if not path.exists():
        err(errors, f"{rel(path)}: missing — every hook wired for Claude Code needs a Codex adapter entry (D4 parity)")
        return
    _check_hook_wiring(path, CODEX_EVENTS_WITHOUT_MATCHER, errors)


def check_mirror_drift(errors: list[str]) -> None:
    res = subprocess.run(
        [sys.executable, "scripts/sync_skills.py", "--check"],
        cwd=ROOT, text=True, capture_output=True,
    )
    if res.returncode != 0:
        err(errors, "mirror drift: " + (res.stdout.strip() or res.stderr.strip()).replace("\n", " | "))


def check_hooks_neutral(errors: list[str]) -> None:
    """D4: shared enforcement scripts in hooks/ must resolve their own root
    and never depend on harness-specific variables or paths. Those details
    belong in the thin lifecycle adapters, not shared enforcement."""
    forbidden = {
        "CLAUDE_PROJECT_DIR": "Claude-only environment variable",
        ".claude/": "Claude-specific path",
        ".codex/": "Codex-specific path",
        ".agents/": "Codex discovery-mirror path",
    }
    for path in sorted(HOOKS.glob("*.sh")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for token, reason in forbidden.items():
            if token in text:
                err(errors, f"{rel(path)}: shared hook contains {reason} ({token}); keep harness semantics in its adapter")


def _publish_matcher(path: Path) -> str | None:
    """Find the PreToolUse matcher on the block that wires humanize-gate.sh,
    in either adapter file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    for block in data.get("hooks", {}).get("PreToolUse", []):
        if any("humanize-gate.sh" in h.get("command", "") for h in block.get("hooks", [])):
            return block.get("matcher")
    return None


def _matcher_tool_suffixes(matcher: str) -> set[str]:
    """Extract every 'ServerName__toolName' suffix the dual-prefix publish
    matcher covers, independent of the optional (claude_ai_)? prefix group
    (skipped explicitly so it isn't mistaken for a server__(tools) group)."""
    suffixes = set()
    stripped = matcher.replace(r"(claude_ai_)?", "")
    # Anchored to the literal "mcp__" prefix so a non-greedy server-name
    # capture stops at the real server/tool-group boundary — an unanchored
    # \w+ would swallow "mcp__Atlassian_Rovo" as one token (both segments
    # are \w, including the double underscore between them).
    for server, alternation in re.findall(r"mcp__(\w+?)__\(([^)]+)\)", stripped):
        for tool in alternation.split("|"):
            suffixes.add(f"{server}__{tool}")
    return suffixes


def _gate_arm_suffixes(gate_path: Path) -> set[str]:
    """Extract every '*ServerName__toolName' case-arm pattern inference-
    discipline-gate.sh actually recognises. Scoped to real case-pattern
    lines (a run of '*Server__tool' alternatives ending in ')'), not prose
    that happens to mention the shape in a comment."""
    arm_line = re.compile(r"^\s*(\*\w+__\w+)(\|\*\w+__\w+)*\)\s*$")
    suffixes = set()
    for line in gate_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not arm_line.match(line):
            continue
        for server, tool in re.findall(r"\*(\w+)__(\w+)", line):
            suffixes.add(f"{server}__{tool}")
    return suffixes


def check_publish_scope(errors: list[str]) -> None:
    """B1: the publish matcher in each adapter decides *when* the gates run;
    inference-discipline-gate.sh's case arms decide whether it recognises the
    tool once routed there. If a tool is added to the matcher without a
    matching arm, the gate silently falls through to its `*) exit 0 ;;`
    default — this is exactly the failure mode that produced B1 in the first
    place, so keep the two in sync automatically rather than by discipline."""
    gate_arms = _gate_arm_suffixes(HOOKS / "inference-discipline-gate.sh")
    for adapter in [ROOT / ".claude" / "settings.json", ROOT / ".codex" / "hooks.json"]:
        matcher = _publish_matcher(adapter)
        if not matcher:
            continue  # check_settings / check_codex_hooks already flag a missing/malformed adapter
        for suffix in sorted(_matcher_tool_suffixes(matcher)):
            if suffix not in gate_arms:
                err(errors, f"{rel(adapter)}: publish matcher covers '{suffix}' but hooks/inference-discipline-gate.sh has no matching case arm")


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


ADVERSARIAL_CATEGORIES = {"doctrine-adversarial", "skill-functional-adversarial"}
DOCTRINE_SKILLS = {"pm-phase-discover", "pm-phase-define", "pm-phase-develop", "pm-phase-deliver", "inference-discipline"}
MIN_EVALS_PER_SKILL = 3


def check_eval_coverage(errors: list[str]) -> None:
    """B2 + B11: every canonical skill (discovered as skills/*/SKILL.md, never
    a fixed list, never the mirrors) ships an evals/evals.json that is graded
    rather than trusted. Identity: valid JSON, skill_name equal to the
    directory, evals a list, every eval with an int id, a non-empty name, a
    category from the 4-value taxonomy, and non-empty prompt/expected_output;
    ids and names unique within the skill (parity keys on (skill, name), so a
    duplicated name would count for the floor while sharing one block).
    Coverage: at least MIN_EVALS_PER_SKILL evals and one adversarial category
    per skill; the doctrine skills also carry a negative control. Parity with
    scripts/grade_evals.py ASSERTIONS in both directions: an eval without a
    block would grade 0/0, a block without an eval is orphan code."""
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import grade_evals  # noqa: WPS433 (runtime import of a sibling script)
    except Exception as exc:
        err(errors, f"scripts/grade_evals.py: cannot import to check eval parity ({exc})")
        return
    assertion_pairs = {(skill, name) for skill, blocks in grade_evals.ASSERTIONS.items() for name in blocks}
    manifest_pairs: set[tuple[str, str]] = set()

    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        skill = skill_md.parent.name
        path = skill_md.parent / "evals" / "evals.json"
        if not path.exists():
            err(errors, f"skills/{skill}: missing evals/evals.json (every skill is graded, not trusted)")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            err(errors, f"{rel(path)}: invalid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            err(errors, f"{rel(path)}: top-level JSON value must be an object")
            continue
        if data.get("skill_name") != skill:
            err(errors, f"{rel(path)}: skill_name {data.get('skill_name')!r} does not match directory {skill!r}")
        evals = data.get("evals")
        if not isinstance(evals, list):
            err(errors, f"{rel(path)}: 'evals' must be a list")
            continue
        if len(evals) < MIN_EVALS_PER_SKILL:
            err(errors, f"{rel(path)}: {len(evals)} eval(s), floor is {MIN_EVALS_PER_SKILL}")
        seen_ids: set = set()
        seen_names: set = set()
        categories: list = []
        for ev in evals:
            if not isinstance(ev, dict):
                err(errors, f"{rel(path)}: each eval must be an object, got {type(ev).__name__}")
                continue
            eid, name, category = ev.get("id"), ev.get("name"), ev.get("category")
            label = name if isinstance(name, str) and name else f"id {eid}"
            if not isinstance(eid, int) or isinstance(eid, bool):
                err(errors, f"{rel(path)}: eval '{label}' id must be an integer, got {eid!r}")
            if not isinstance(name, str) or not name.strip():
                err(errors, f"{rel(path)}: eval id {eid} has an empty or non-string name")
            # Valid JSON with an unexpected shape must produce a finding, never a
            # traceback: a list or object here is unhashable, so it cannot be
            # tested against the category set or collected for the coverage checks.
            if not isinstance(category, str):
                err(errors, f"{rel(path)}: eval '{label}' category must be a string, got {type(category).__name__}")
            elif category not in EVAL_CATEGORIES:
                err(errors, f"{rel(path)}: eval '{label}' has invalid category {category!r}; must be one of {sorted(EVAL_CATEGORIES)}")
            for field in ("prompt", "expected_output"):
                if not isinstance(ev.get(field), str) or not ev.get(field).strip():
                    err(errors, f"{rel(path)}: eval '{label}' has an empty or non-string {field}")
            if isinstance(eid, int) and not isinstance(eid, bool):
                if eid in seen_ids:
                    err(errors, f"{rel(path)}: duplicate eval id {eid} ({label})")
                seen_ids.add(eid)
            if isinstance(name, str) and name.strip():
                if name in seen_names:
                    err(errors, f"{rel(path)}: duplicate eval name {name!r} (parity keys on the name)")
                seen_names.add(name)
            if isinstance(category, str):
                categories.append(category)
            if isinstance(name, str) and name.strip():
                manifest_pairs.add((skill, name))
        if not any(c in ADVERSARIAL_CATEGORIES for c in categories):
            err(errors, f"{rel(path)}: no adversarial eval (need one of {sorted(ADVERSARIAL_CATEGORIES)})")
        if skill in DOCTRINE_SKILLS:
            if "doctrine-adversarial" not in categories:
                err(errors, f"{rel(path)}: doctrine skill without a doctrine-adversarial eval")
            if "negative-control" not in categories:
                err(errors, f"{rel(path)}: doctrine skill without a negative-control eval")

    for skill, name in sorted(manifest_pairs - assertion_pairs):
        err(errors, f"skills/{skill}/evals/evals.json: eval '{name}' has no ASSERTIONS block in scripts/grade_evals.py (would grade 0/0)")
    for skill, name in sorted(assertion_pairs - manifest_pairs):
        err(errors, f"scripts/grade_evals.py: ASSERTIONS[{skill!r}][{name!r}] has no matching eval in evals.json (orphan block)")


def check_memory_bootstrap(errors: list[str]) -> None:
    # Local session state (an active project under .ai/memory/, sentinel
    # flags under .ai/gates/) must not leak into the fresh-clone bootstrap
    # simulation below — but the tracked skeleton .ai/memory/_templates/,
    # README.md, and active-context.example.md are exactly what a fresh
    # clone ships and init_context.py depends on, so this excludes local
    # state by exact relative path rather than by directory basename.
    local_state = {".ai/memory/active-context.md", ".ai/memory/index.md", ".ai/memory/inbox.md",
                   ".ai/memory/context-events.jsonl", ".ai/memory/projects", ".ai/memory/people", ".ai/gates"}

    def ignore(dirpath: str, names: list[str]) -> set[str]:
        rel_dir = os.path.relpath(dirpath, ROOT)
        skip = {"workspace", "__pycache__"} if rel_dir != "." else {".git", "workspace", "__pycache__"}
        for name in names:
            rel_entry = name if rel_dir == "." else f"{rel_dir}/{name}"
            if rel_entry.replace(os.sep, "/") in local_state:
                skip.add(name)
        return skip

    with tempfile.TemporaryDirectory(prefix="ai-pm-validate-") as td:
        tmp = Path(td) / ROOT.name
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


def check_agents(errors: list[str]) -> None:
    """GitHub custom agents in .github/agents/.

    Schema rules come from GitHub's custom-agents configuration reference:
    `name` is optional (the filename is the identifier, unlike SKILL.md, which
    requires one), `model` is a string that inherits the default when unset,
    aliases are case-insensitive and have documented compatible spellings, and
    unrecognized tool names are ignored rather than rejected.

    Three rules here are repo policy, not schema, and say so in the message:
    `model` must be absent, so every agent inherits the default and no model
    identifier lives in the repository; `tools` must be an explicit non-empty
    list of canonical lowercase aliases, though GitHub also accepts a
    comma-separated string, `[]`, `["*"]` and omission; and `agents`, which
    GitHub does not document, is validated only for internal consistency --
    each name must resolve to a file, and a non-empty list needs the `agent`
    tool to act on it.
    """
    paths = sorted(AGENTS_DIR.glob("*.agent.md"))
    if not paths:
        err(errors, f"{rel(AGENTS_DIR)}: no *.agent.md files found")
        return
    known = {p.name[: -len(".agent.md")] for p in paths}

    for path in paths:
        name = rel(path)
        data, body = load_frontmatter(path, errors)
        if data is None:
            continue

        description = data.get("description")
        if not unsupported(errors, path, "description", description):
            if not isinstance(description, str) or not description.strip():
                err(errors, f"{name}: frontmatter needs a non-empty string description")

        if "model" in data:
            err(errors, f"{name}: repo policy is to omit `model` so the agent inherits the default model; remove it")

        tools = data.get("tools")
        if unsupported(errors, path, "tools", tools):
            tools = []
        elif not isinstance(tools, list) or not tools:
            err(
                errors,
                f"{name}: repo policy is an explicit non-empty YAML list for `tools`; GitHub also accepts "
                f'a comma-separated string, `[]` to disable all, `["*"]` for all, and omission to default '
                f"to all, but this repo requires a reviewable allowlist",
            )
            tools = []
        for tool in tools:
            if not isinstance(tool, str) or not tool.strip():
                err(errors, f"{name}: every `tools` entry must be a non-empty string")
                continue
            if "/" in tool:
                if not AGENT_MCP_TOOL.match(tool):
                    err(errors, f"{name}: malformed MCP tool {tool!r} — use `server/tool` or `server/*`")
                continue
            if tool == "*":
                err(errors, f'{name}: `["*"]` enables every tool on GitHub, but repo policy is an explicit allowlist')
                continue
            if tool in AGENT_TOOL_ALIASES:
                continue
            lowered = tool.lower()
            if lowered in AGENT_TOOL_ALIASES:
                err(
                    errors,
                    f"{name}: tool {tool!r} works on GitHub, where aliases are case-insensitive, but repo "
                    f"policy is the lowercase form {lowered!r}",
                )
            elif lowered in AGENT_TOOL_COMPATIBLE:
                err(
                    errors,
                    f"{name}: tool {tool!r} is a GitHub-compatible spelling of "
                    f"{AGENT_TOOL_COMPATIBLE[lowered]!r}; repo policy is the canonical alias",
                )
            else:
                err(
                    errors,
                    f"{name}: unknown tool {tool!r} — GitHub ignores unrecognized tool names silently, so "
                    f"this costs the agent a capability with no error anywhere",
                )

        delegates = data.get("agents")
        if delegates is not None and not unsupported(errors, path, "agents", delegates):
            if not isinstance(delegates, list):
                err(errors, f"{name}: `agents` must be a list, got {type(delegates).__name__}")
            else:
                for other in delegates:
                    if not isinstance(other, str) or other not in known:
                        err(errors, f"{name}: `agents` names {other!r}, which has no file in {rel(AGENTS_DIR)}")
                if delegates and "agent" not in tools:
                    err(errors, f"{name}: `agents` is non-empty but `tools` lacks `agent`, so it cannot delegate")

        invocable = data.get("user-invocable")
        if invocable is not None and not unsupported(errors, path, "user-invocable", invocable):
            if not isinstance(invocable, bool):
                err(errors, f"{name}: `user-invocable` must be a boolean, got {type(invocable).__name__}")

        headings = [line for line in body.splitlines() if line.strip() == AGENT_READING_HEADING]
        if len(headings) != 1:
            err(errors, f"{name}: needs exactly one '{AGENT_READING_HEADING}' heading, found {len(headings)}")
            continue
        section = body.split(AGENT_READING_HEADING, 1)[1]
        section = re.split(r"^#", section, maxsplit=1, flags=re.M)[0]
        for required in AGENT_CORE_READING:
            if required not in section:
                err(errors, f"{name}: required reading omits `{required}`")
        if not AGENT_PROJECT_MEMORY.search(section):
            err(errors, f"{name}: required reading names no project memory (say 'project memory' or cite `.ai/memory/projects/`)")

    table = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    listed = set(re.findall(r"`\.github/agents/([A-Za-z0-9_-]+)\.agent\.md`", table))
    for missing in sorted(known - listed):
        err(errors, f"AGENTS.md: no table row for {missing}")
    for orphan in sorted(listed - known):
        err(errors, f"AGENTS.md: table row for {orphan}, which has no file in {rel(AGENTS_DIR)}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    check_skill_frontmatter(errors)
    check_markdown_links(errors)
    check_backtick_paths(errors)
    check_workflow_contract(errors)
    check_settings(errors, warnings)
    check_codex_hooks(errors, warnings)
    check_hook_syntax(errors, warnings)
    check_hooks_neutral(errors)
    check_publish_scope(errors)
    check_mirror_drift(errors)
    check_eval_coverage(errors)
    check_agents(errors)
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
