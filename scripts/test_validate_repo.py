#!/usr/bin/env python3
"""
test_validate_repo.py — regression cases for two validate_repo.py checks.

check_eval_coverage: valid JSON with an unexpected schema must produce a
validation finding, never a traceback. Each case writes one fake skill
(SKILL.md + evals/evals.json) into a temporary directory, points the check at
it, and asserts the call returns normally with at least one error naming the
offending field. The real scripts/grade_evals.py is imported for the parity
half of the check, so every case also reports the fake eval as having no
assertion block; that is expected and not what is being tested here.

check_agents: each case writes one fake .agent.md plus a matching AGENTS.md
row into a temporary directory and asserts the expected finding. One case
expects *no* finding — an MCP tool named `server/tool` is legitimate, and a
closed allowlist of built-in aliases would wrongly reject it.

Usage: python3 scripts/test_validate_repo.py
Exits 0 if every case passes, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate_repo as vr  # noqa: E402

GOOD_EVAL = {"id": 1, "name": "one", "category": "standard", "prompt": "p", "expected_output": "e"}

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
            vr.check_eval_coverage(errors)
            return errors
        finally:
            vr.SKILLS, vr.rel = saved_skills, saved_rel


AGENT_FM = 'description: "fixture"\ntools: [read, search]'
AGENT_BODY = """
You are **fake-agent**.

## Required reading

- `.ai/rules.md`
- `.ai/app.md`
- `.ai/memory/active-context.md`
- relevant project memory
"""

# (case name, frontmatter, body, substring the finding must contain — None means
# the case must produce no finding at all)
AGENT_CASES: list[tuple[str, str, str, str | None]] = [
    ("model is a list", AGENT_FM + "\nmodel: ['a (copilot)', 'b (copilot)']", AGENT_BODY, "remove `model`"),
    ("model is a string", AGENT_FM + "\nmodel: some-model", AGENT_BODY, "remove `model`"),
    ("tools is missing", 'description: "fixture"', AGENT_BODY, "`tools` must be a non-empty list"),
    ("unknown bare tool alias", 'description: "fixture"\ntools: [read, browse]', AGENT_BODY, "unknown tool"),
    ("mcp tool is accepted", 'description: "fixture"\ntools: [read, some-server/tool-1]', AGENT_BODY, None),
    ("agents names a missing file", AGENT_FM.replace("[read, search]", "[read, search, agent]") + "\nagents: [nope]", AGENT_BODY, "has no file in"),
    ("agents without the agent tool", AGENT_FM + "\nagents: [fake-agent]", AGENT_BODY, "lacks `agent`"),
    ("user-invocable is a string", AGENT_FM + "\nuser-invocable: 'false'", AGENT_BODY, "must be a boolean"),
    ("no required-reading heading", AGENT_FM, "\nYou are **fake-agent**.\n", "exactly one"),
    ("required reading omits rules.md", AGENT_FM, AGENT_BODY.replace("- `.ai/rules.md`\n", ""), "omits `.ai/rules.md`"),
]


def run_agent_case(frontmatter: str, body: str) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="test-validate-agents-") as td:
        root = Path(td)
        agents = root / ".github" / "agents"
        agents.mkdir(parents=True)
        (agents / "fake-agent.agent.md").write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
        (root / "AGENTS.md").write_text(
            "| fake-agent | `.github/agents/fake-agent.agent.md` | fixture |\n", encoding="utf-8"
        )
        saved = (vr.ROOT, vr.AGENTS_DIR, vr.rel)
        vr.ROOT, vr.AGENTS_DIR = root, agents
        vr.rel = lambda p: str(Path(p).relative_to(root))  # the fixture lives outside the repo root
        try:
            errors: list[str] = []
            vr.check_agents(errors)
            return errors
        finally:
            vr.ROOT, vr.AGENTS_DIR, vr.rel = saved


def main() -> int:
    failures = 0
    for name, payload, needle in CASES:
        try:
            errors = run_case(payload)
        except Exception as exc:  # the defect under test: a traceback instead of a finding
            failures += 1
            print(f"FAIL  {name}: raised {type(exc).__name__}: {exc}")
            continue
        hit = any(needle in e for e in errors)
        print(f"{'PASS' if hit else 'FAIL'}  {name}: {len(errors)} finding(s), expected one containing {needle!r}")
        if not hit:
            failures += 1
            for e in errors:
                print(f"      {e}")
    for name, frontmatter, body, needle in AGENT_CASES:
        try:
            errors = run_agent_case(frontmatter, body)
        except Exception as exc:  # a traceback is never an acceptable validator outcome
            failures += 1
            print(f"FAIL  agents: {name}: raised {type(exc).__name__}: {exc}")
            continue
        if needle is None:
            ok = not errors
            print(f"{'PASS' if ok else 'FAIL'}  agents: {name}: {len(errors)} finding(s), expected none")
        else:
            ok = any(needle in e for e in errors)
            print(f"{'PASS' if ok else 'FAIL'}  agents: {name}: {len(errors)} finding(s), expected one containing {needle!r}")
        if not ok:
            failures += 1
            for e in errors:
                print(f"      {e}")

    total = len(CASES) + len(AGENT_CASES)
    if failures:
        print(f"\ntest_validate_repo: {failures}/{total} case(s) failed")
        return 1
    print(f"\ntest_validate_repo: all {total} case(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
