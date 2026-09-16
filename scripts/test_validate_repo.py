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

check_readme_contract: six cases build a tiny tree with two skills, one gate, one agent
and two scripts, then feed the check a README that matches it and five that drift — a
wrong count, a count stated twice, a missing table row, a row for a script that is gone,
and a contents list out of step with the headings.

check_backtick_paths and check_markdown_links: a generated eval proposal quotes a
recorded output, so it may carry a path that never existed. Two cases assert the
skip is scoped to the proposals directory and does not spread to the rest of
docs/benchmarks/, where a report is a live contract like any other doc.

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

    # A proposal quotes a recorded output; a report in the same tree does not.
    generated_cases = [
        ("docs/benchmarks/iteration-1/proposals/a-skill__eval-1-a-name__with_skill__abc123.md", True),
        ("docs/benchmarks/iteration-1/proposals/index.md", True),
        ("docs/benchmarks/iteration-1/report.md", False),
        ("docs/benchmarks/pilot-deps.json", False),
        ("docs/EVAL_PROTOCOL.md", False),
    ]
    for rel_path, expected in generated_cases:
        got = bool(vr.GENERATED_RECORDS.match(rel_path))
        ok = got is expected
        print(f"{'PASS' if ok else 'FAIL'}  generated-record skip: {rel_path} -> {got}")
        if not ok:
            failures += 1

    # The regex is half the claim; the other half is that both document checks consult it.
    # Same broken document in two places under docs/benchmarks/, one skipped and one not.
    broken = "# A doc\n\nSee [the plan](nope.md) and `skills/nope/SKILL.md`.\n"
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td)
        iteration = tree / "docs" / "benchmarks" / "iteration-1"
        (iteration / "proposals").mkdir(parents=True)
        (iteration / "report.md").write_text(broken, encoding="utf-8")
        (iteration / "proposals" / "a-skill__eval-1-a-name__with_skill__abc123.md").write_text(broken, encoding="utf-8")
        saved = (vr.ROOT, vr.MIRRORS, vr.SKILLS)
        vr.ROOT, vr.MIRRORS, vr.SKILLS = tree, [], tree / "skills"
        try:
            link_errors, path_errors = [], []
            vr.check_markdown_links(link_errors)
            vr.check_backtick_paths(path_errors)
        finally:
            vr.ROOT, vr.MIRRORS, vr.SKILLS = saved
    consulted_cases = [("check_markdown_links", link_errors), ("check_backtick_paths", path_errors)]
    for name, errors in consulted_cases:
        ok = len(errors) == 1 and "report.md" in errors[0] and "proposals/" not in errors[0]
        print(f"{'PASS' if ok else 'FAIL'}  {name} skips a proposal and still checks the report beside it")
        if not ok:
            failures += 1
            for e in errors:
                print(f"      {e}")

    # check_readme_contract: every count comes from the tree, so a README that drifts is a
    # finding rather than a thing someone notices six months later.
    readme_cases = [
        ("a README that matches the tree", lambda t: t, [], 0),
        ("a count that drifted", lambda t: t.replace("2 hard-skill", "9 hard-skill"),
         ["says skills 9; the tree has 2"], 1),
        ("a count stated twice", lambda t: t + "\n\nStill 2 hard-skill PM skills.\n",
         ["stated exactly once as a digit", "matched 2 time(s)"], 1),
        ("a script with no row", lambda t: t.replace("| `two.py` | second |\n", ""),
         ["no row for scripts/two.py"], 1),
        ("a row for a script that is gone", lambda t: t.replace("| `two.py` |", "| `three.py` |"),
         ["no row for scripts/two.py", "names scripts/three.py, which does not exist"], 2),
        ("a contents list out of step with the headings",
         lambda t: t.replace("- [Second](#second)\n", ""),
         ["contents list and the top-level headings disagree"], 1),
    ]
    for name, mutate, expected, expected_count in readme_cases:
        with tempfile.TemporaryDirectory() as td:
            tree = Path(td)
            for skill in ("alpha", "beta"):
                (tree / "skills" / skill / "evals").mkdir(parents=True)
                (tree / "skills" / skill / "SKILL.md").write_text("x", encoding="utf-8")
                (tree / "skills" / skill / "evals" / "evals.json").write_text(json.dumps(
                    {"skill_name": skill, "evals": [{"name": "a", "category": "standard"},
                                                    {"name": "b", "category": "negative-control"}]}), encoding="utf-8")
            (tree / "hooks").mkdir()
            (tree / "hooks" / "only-gate.sh").write_text("x", encoding="utf-8")
            (tree / ".github" / "agents").mkdir(parents=True)
            (tree / ".github" / "agents" / "one.agent.md").write_text("x", encoding="utf-8")
            (tree / "scripts").mkdir()
            for script in ("one.py", "two.py"):
                (tree / "scripts" / script).write_text("x", encoding="utf-8")
            readme = "\n".join([
                "# t", "", "2 hard-skill PM skills, 1 blocking hooks, 1 agents, 4 eval cases:",
                "2 standard, 0 doctrine-adversarial, 0 skill-functional-adversarial and 2 negative controls.",
                "", "- [First](#first)", "- [Second](#second)", "",
                "## First", "", "| Script | Purpose |", "|---|---|",
                "| `one.py` | first |", "| `two.py` | second |", "", "## Second", "", "done.", ""])
            (tree / "README.md").write_text(mutate(readme), encoding="utf-8")
            saved = (vr.ROOT, vr.SKILLS, vr.HOOKS, vr.README)
            vr.ROOT, vr.SKILLS, vr.HOOKS, vr.README = tree, tree / "skills", tree / "hooks", tree / "README.md"
            try:
                readme_errors: list[str] = []
                vr.check_readme_contract(readme_errors)
            finally:
                vr.ROOT, vr.SKILLS, vr.HOOKS, vr.README = saved
        joined = " ".join(readme_errors)
        ok = len(readme_errors) == expected_count and all(want in joined for want in expected)
        print(f"{'PASS' if ok else 'FAIL'}  readme contract: {name}")
        if not ok:
            failures += 1
            for e in readme_errors:
                print(f"      {e}")

    # check_readme_contract derives its counts from the same manifests check_eval_coverage
    # hardens, and main() runs it first, so every shape that suite feeds must be tolerated
    # here too. A finding is fine; an exception aborts the validator before the check that
    # reports the schema defect ever runs.
    def readme_tree(td: str, payload: object, skills_said: int = 1) -> Path:
        tree = Path(td)
        (tree / "skills" / "fake-skill" / "evals").mkdir(parents=True)
        (tree / "skills" / "fake-skill" / "SKILL.md").write_text("x", encoding="utf-8")
        body = payload if isinstance(payload, str) else json.dumps(payload)
        (tree / "skills" / "fake-skill" / "evals" / "evals.json").write_text(body, encoding="utf-8")
        (tree / "hooks").mkdir()
        (tree / "hooks" / "one-gate.sh").write_text("x", encoding="utf-8")
        (tree / ".github" / "agents").mkdir(parents=True)
        (tree / ".github" / "agents" / "one.agent.md").write_text("x", encoding="utf-8")
        (tree / "scripts").mkdir()
        (tree / "README.md").write_text("\n".join([
            "# t", "",
            f"{skills_said} hard-skill PM skills, 1 blocking hooks, 1 agents, 9 eval cases:",
            "9 standard, 0 doctrine-adversarial, 0 skill-functional-adversarial and 0 negative controls.",
            "", "- [First](#first)", "", "## First", "", "done.", ""]), encoding="utf-8")
        return tree

    def run_readme_contract(payload: object, skills_said: int = 1) -> tuple[list[str], str]:
        with tempfile.TemporaryDirectory(prefix="test-readme-contract-") as td:
            tree = readme_tree(td, payload, skills_said)
            saved = (vr.ROOT, vr.SKILLS, vr.HOOKS, vr.README)
            vr.ROOT, vr.SKILLS, vr.HOOKS, vr.README = tree, tree / "skills", tree / "hooks", tree / "README.md"
            try:
                found: list[str] = []
                vr.check_readme_contract(found)
                return found, ""
            except Exception as exc:  # the regression this case exists for
                return [], f"{type(exc).__name__}: {exc}"
            finally:
                vr.ROOT, vr.SKILLS, vr.HOOKS, vr.README = saved

    schema_cases = list(CASES) + [("not even JSON", "{{{ broken", "")]
    for name, payload, _expected in schema_cases:
        _found, raised = run_readme_contract(payload)
        ok = not raised
        print(f"{'PASS' if ok else 'FAIL'}  readme contract survives a malformed manifest: {name}")
        if not ok:
            failures += 1
            print(f"      {raised}")

    # and the skip is scoped: the counts that do not come from a manifest are still compared
    scoped, raised = run_readme_contract(CASES[-1][1], skills_said=9)
    ok = not raised and len(scoped) == 1 and "says skills 9" in scoped[0]
    print(f"{'PASS' if ok else 'FAIL'}  readme contract still checks the counts a manifest cannot break")
    if not ok:
        failures += 1
        print(f"      {raised or scoped}")

    total = (len(CASES) + (len(AGENT_CASES) + 1) * len(modes) + len(generated_cases)
             + len(consulted_cases) + len(readme_cases) + len(schema_cases) + 1)
    if failures:
        print(f"\ntest_validate_repo: {failures}/{total} case(s) failed")
        return 1
    print(f"\ntest_validate_repo: all {total} case(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
