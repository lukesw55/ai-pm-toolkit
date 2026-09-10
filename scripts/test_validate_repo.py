#!/usr/bin/env python3
"""
test_validate_repo.py — regression cases for two validate_repo.py checks.

check_eval_coverage: valid JSON with an unexpected schema must produce a
validation finding, never a traceback. Each case writes one fake skill
(SKILL.md + evals/evals.json) into a temporary directory, points the check at
it, and asserts the exact findings. The assertion manifest and coverage floor
are scoped to the one-eval fixture; production policy is not changed.

check_agents: each case writes one fake .agent.md plus a matching AGENTS.md
row into a temporary directory and asserts the expected finding. Every case
runs twice, once with PyYAML and once with vr.yaml set to None, and must reach
the same verdict in both: a finding, or none. Two cases expect *no* finding --
`server/tool` and `server/*` are legitimate MCP tools, and a closed allowlist
of built-in aliases would wrongly reject them. Two more expect different
diagnostics per mode, because invalid YAML fails the whole frontmatter under
PyYAML and only one field in the fallback.

load_frontmatter: one canonical fixture checks the parsed *value*, not just
the absence of a finding, so a block-scalar marker such as ">-" cannot pass as
a description the way it used to.

Usage: python3 scripts/test_validate_repo.py
Exits 0 if every case passes, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
import tempfile
from unittest.mock import patch
import grade_evals
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate_repo as vr  # noqa: E402

GOOD_EVAL = {"id": 1, "name": "one", "category": "doctrine-adversarial", "prompt": "p", "expected_output": "e"}

# (case name, manifest payload, substring the finding must contain)
CASES: list[tuple[str, object, str]] = [
    ("category is a list", {"skill_name": "fake-skill", "evals": [dict(GOOD_EVAL, category=[])]}, "category must be a string"),
    ("category is an object", {"skill_name": "fake-skill", "evals": [dict(GOOD_EVAL, category={})]}, "category must be a string"),
    ("category is a wrong string", {"skill_name": "fake-skill", "evals": [dict(GOOD_EVAL, category="adversarial")]}, "invalid category"),
    ("id is a list", {"skill_name": "fake-skill", "evals": [dict(GOOD_EVAL, id=[])]}, "id must be an integer"),
    ("name is a list", {"skill_name": "fake-skill", "evals": [dict(GOOD_EVAL, name=[])]}, "non-string name"),
    ("eval is not an object", {"skill_name": "fake-skill", "evals": ["not-an-object"]}, "each eval must be an object"),
    ("evals is not a list", {"skill_name": "fake-skill", "evals": {"id": 1}}, "'evals' must be a list"),
    ("top-level is not an object", [GOOD_EVAL], "top-level JSON value must be an object"),
]


_PREFIX = "fake-skill/evals/evals.json: "
_NO_ADV = _PREFIX + "no adversarial eval (need one of ['doctrine-adversarial', 'skill-functional-adversarial'])"
_ORPHAN = "scripts/grade_evals.py: ASSERTIONS['fake-skill']['one'] has no matching eval in evals.json (orphan block)"
EXPECTED_FINDINGS = {
    "category is a list": {_PREFIX + "eval 'one' category must be a string, got list", _NO_ADV},
    "category is an object": {_PREFIX + "eval 'one' category must be a string, got dict", _NO_ADV},
    "category is a wrong string": {_PREFIX + "eval 'one' has invalid category 'adversarial'; must be one of ['doctrine-adversarial', 'negative-control', 'skill-functional-adversarial', 'standard']", _NO_ADV},
    "id is a list": {_PREFIX + "eval 'one' id must be an integer, got []"},
    "name is a list": {_PREFIX + "eval id 1 has an empty or non-string name", _ORPHAN},
    "eval is not an object": {_PREFIX + "each eval must be an object, got str", _NO_ADV, _ORPHAN},
    "evals is not a list": {_PREFIX + "'evals' must be a list", _ORPHAN},
    "top-level is not an object": {_PREFIX + "top-level JSON value must be an object", _ORPHAN},
}


def run_case(payload: object) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="test-validate-repo-") as td:
        skill = Path(td) / "fake-skill"
        (skill / "evals").mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: fake-skill\ndescription: fixture\n---\n", encoding="utf-8")
        (skill / "evals" / "evals.json").write_text(json.dumps(payload), encoding="utf-8")
        saved_skills, saved_rel = vr.SKILLS, vr.rel
        vr.SKILLS = Path(td)
        vr.rel = lambda p: str(Path(p).relative_to(td))  # the fixture lives outside the repo root
        try:
            errors: list[str] = []
            with patch.object(grade_evals, "ASSERTIONS", {"fake-skill": {"one": [("fixture", lambda text: True)]}}), patch.object(vr, "MIN_EVALS_PER_SKILL", 1):
                vr.check_eval_coverage(errors)
            return errors
        finally:
            vr.SKILLS, vr.rel = saved_skills, saved_rel


AGENT_FM = 'description: "fixture"\ntools: [read, search]'
AGENT_BODY = """
You are **fake-agent**.

## Required reading

- `.ai/rules.md`
- `.ai/memory/projects/<slug>/app.md`
- `.ai/memory/active-context.md`
- relevant project memory
"""

# (case name, frontmatter, body, substring the finding must contain — None means
# the case must produce no finding at all)
AGENT_CASES: list[tuple[str, str, str, str | None]] = [
    ("model is a list", AGENT_FM + "\nmodel: ['a (copilot)', 'b (copilot)']", AGENT_BODY, "omit `model`"),
    ("model is a string", AGENT_FM + "\nmodel: some-model", AGENT_BODY, "omit `model`"),
    ("tools is missing", 'description: "fixture"', AGENT_BODY, "explicit non-empty YAML list"),
    ("unknown bare tool alias", 'description: "fixture"\ntools: [read, browse]', AGENT_BODY, "unknown tool"),
    ("mcp tool is accepted", 'description: "fixture"\ntools: [read, some-server/tool-1]', AGENT_BODY, None),
    ("agents names a missing file", AGENT_FM.replace("[read, search]", "[read, search, agent]") + "\nagents: [nope]", AGENT_BODY, "has no file in"),
    ("agents without the agent tool", AGENT_FM + "\nagents: [fake-agent]", AGENT_BODY, "lacks `agent`"),
    ("user-invocable is a string", AGENT_FM + "\nuser-invocable: 'false'", AGENT_BODY, "must be a boolean"),
    ("no required-reading heading", AGENT_FM, "\nYou are **fake-agent**.\n", "exactly one"),
    ("required reading omits rules.md", AGENT_FM, AGENT_BODY.replace("- `.ai/rules.md`\n", ""), "omits `.ai/rules.md`"),
    # B17 review: the project-memory rule used to be a tautology, because the
    # core set already contains "memory" via active-context.md.
    ("required reading names no project memory", AGENT_FM, AGENT_BODY.replace("- relevant project memory\n", ""), "names no project memory"),
    # Three distinct failure modes where the head only had one.
    ("canonical alias in wrong case", 'description: "fixture"\ntools: [read, "Read"]', AGENT_BODY, "lowercase form"),
    ("github-compatible spelling", 'description: "fixture"\ntools: [read, "NotebookRead"]', AGENT_BODY, "compatible spelling"),
    # Forms GitHub accepts that repo policy refuses; the message must say so.
    ("tools as a comma separated string", 'description: "fixture"\ntools: read, search', AGENT_BODY, "explicit non-empty YAML list"),
    ("tools disables everything", 'description: "fixture"\ntools: []', AGENT_BODY, "explicit non-empty YAML list"),
    ("tools enables everything", 'description: "fixture"\ntools: ["*"]', AGENT_BODY, "explicit allowlist"),
    # MCP form: server/tool and server/* only.
    ("mcp tool without a server", 'description: "fixture"\ntools: [read, "/tool"]', AGENT_BODY, "malformed MCP tool"),
    ("mcp server without a tool", 'description: "fixture"\ntools: [read, "server/"]', AGENT_BODY, "malformed MCP tool"),
    ("mcp tool with two slashes", 'description: "fixture"\ntools: [read, "a/b/c"]', AGENT_BODY, "malformed MCP tool"),
    ("mcp server wildcard is accepted", 'description: "fixture"\ntools: [read, "server/*"]', AGENT_BODY, None),
    # Genuinely invalid YAML: PyYAML rejects the frontmatter, the fallback
    # rejects the field. Same verdict, different diagnostic.
    ("inline list with an empty item", 'description: "fixture"\ntools: [read,, search]', AGENT_BODY,
     ("invalid YAML frontmatter", "outside the frontmatter subset")),
    ("inline list with an unclosed quote", 'description: "fixture"\ntools: ["read, search]', AGENT_BODY,
     ("invalid YAML frontmatter", "outside the frontmatter subset")),
]

# One canonical frontmatter, checked by value: the folded description must come
# back as text in both modes, never as the ">-" marker.
CANONICAL_FRONTMATTER = """---
name: fixture
description: >-
  A real folded description.
metadata:
  version: "1"
---

body
"""
CANONICAL_DESCRIPTION = "A real folded description."


def run_agent_case(frontmatter: str, body: str, without_pyyaml: bool = False) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="test-validate-agents-") as td:
        root = Path(td)
        agents = root / ".github" / "agents"
        agents.mkdir(parents=True)
        (agents / "fake-agent.agent.md").write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
        (root / "AGENTS.md").write_text(
            "| fake-agent | `.github/agents/fake-agent.agent.md` | fixture |\n", encoding="utf-8"
        )
        saved = (vr.ROOT, vr.AGENTS_DIR, vr.rel, vr.yaml)
        vr.ROOT, vr.AGENTS_DIR = root, agents
        vr.rel = lambda p: str(Path(p).relative_to(root))  # the fixture lives outside the repo root
        if without_pyyaml:
            vr.yaml = None
        try:
            errors: list[str] = []
            vr.check_agents(errors)
            return errors
        finally:
            vr.ROOT, vr.AGENTS_DIR, vr.rel, vr.yaml = saved


def main() -> int:
    failures = 0
    modes = (False, True) if vr.yaml is not None else (True,)
    if vr.yaml is None:
        print("SKIP PyYAML cases: optional dependency is unavailable")
    for name, payload, needle in CASES:
        try:
            errors = run_case(payload)
        except Exception as exc:  # the defect under test: a traceback instead of a finding
            failures += 1
            print(f"FAIL  {name}: raised {type(exc).__name__}: {exc}")
            continue
        hit = set(errors) == EXPECTED_FINDINGS[name] and len(errors) == len(EXPECTED_FINDINGS[name])
        print(f"{'PASS' if hit else 'FAIL'}  {name}: {len(errors)} finding(s), exact expected finding set")
        if not hit:
            failures += 1
            for e in errors:
                print(f"      {e}")
    for name, frontmatter, body, needle in AGENT_CASES:
        for without_pyyaml in modes:
            mode = "no-pyyaml" if without_pyyaml else "pyyaml"
            want = needle[without_pyyaml] if isinstance(needle, tuple) else needle
            try:
                errors = run_agent_case(frontmatter, body, without_pyyaml)
            except Exception as exc:  # a traceback is never an acceptable validator outcome
                failures += 1
                print(f"FAIL  agents[{mode}]: {name}: raised {type(exc).__name__}: {exc}")
                continue
            if want is None:
                ok = not errors
                print(f"{'PASS' if ok else 'FAIL'}  agents[{mode}]: {name}: {len(errors)} finding(s), expected none")
            else:
                ok = any(want in e for e in errors)
                print(f"{'PASS' if ok else 'FAIL'}  agents[{mode}]: {name}: {len(errors)} finding(s), expected one containing {want!r}")
            if not ok:
                failures += 1
                for e in errors:
                    print(f"      {e}")

    # The folded description must be parsed, not merely accepted. Checking only
    # for the absence of a finding is what let ">-" pass as a description.
    for without_pyyaml in modes:
        mode = "no-pyyaml" if without_pyyaml else "pyyaml"
        with tempfile.TemporaryDirectory(prefix="test-validate-fm-") as td:
            path = Path(td) / "SKILL.md"
            path.write_text(CANONICAL_FRONTMATTER, encoding="utf-8")
            saved = (vr.rel, vr.yaml)
            vr.rel = lambda p: str(Path(p).relative_to(td))
            if without_pyyaml:
                vr.yaml = None
            try:
                errors = []
                data = vr.parse_frontmatter(path, errors)
            finally:
                vr.rel, vr.yaml = saved
        got = data.get("description") if data is not None else None
        ok = not errors and got == CANONICAL_DESCRIPTION
        print(f"{'PASS' if ok else 'FAIL'}  frontmatter[{mode}]: folded description parsed by value: {got!r}")
        if not ok:
            failures += 1
            for e in errors:
                print(f"      {e}")

    total = len(CASES) + (len(AGENT_CASES) + 1) * len(modes)
    if failures:
        print(f"\ntest_validate_repo: {failures}/{total} case(s) failed")
        return 1
    print(f"\ntest_validate_repo: all {total} case(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
