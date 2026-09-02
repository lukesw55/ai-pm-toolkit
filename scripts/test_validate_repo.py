#!/usr/bin/env python3
"""
test_validate_repo.py — regression cases for validate_repo.py's eval coverage
check: valid JSON with an unexpected schema must produce a validation finding,
never a traceback.

Each case writes one fake skill (SKILL.md + evals/evals.json) into a temporary
directory, points check_eval_coverage at it, and asserts that the call returns
normally with at least one error naming the offending field. The real
scripts/grade_evals.py is imported for the parity half of the check, so every
case also reports the fake eval as having no assertion block; that is expected
and not what is being tested here.

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
    if failures:
        print(f"\ntest_validate_repo: {failures}/{len(CASES)} case(s) failed")
        return 1
    print(f"\ntest_validate_repo: all {len(CASES)} case(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
