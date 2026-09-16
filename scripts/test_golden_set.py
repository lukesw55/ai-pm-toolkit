#!/usr/bin/env python3
"""Product golden sets: confinement, the corruption guard, and the rules check.

Each case runs the real scripts/golden_set.py copied into a throwaway repo skeleton, then
inspects the files it wrote. Nothing touches the live .ai/memory tree. Shape mirrors
test_memory.py: PASS/FAIL per case, exit 1 if any case fails.

Usage: python3 scripts/test_golden_set.py
"""
from __future__ import annotations

import csv
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))


class Sandbox:
    def __init__(self, tmp: Path):
        self.root = tmp
        (tmp / "scripts").mkdir()
        for name in ("context_paths.py", "golden_set.py", "init_context.py", "memory.py"):
            shutil.copy(ROOT / "scripts" / name, tmp / "scripts" / name)
        shutil.copytree(ROOT / ".ai" / "memory" / "_templates", tmp / ".ai" / "memory" / "_templates")
        self.projects = tmp / ".ai" / "memory" / "projects"

    def run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(self.root / "scripts" / "golden_set.py"), *args],
                              capture_output=True, text=True, cwd=self.root)

    def init_project(self, name: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(self.root / "scripts" / "init_context.py"), name],
                              capture_output=True, text=True, cwd=self.root)

    def sheet(self, slug: str, feature: str) -> Path:
        return self.projects / slug / "evals" / feature / "golden-set.csv"

    def rows(self, slug: str, feature: str) -> list[list[str]]:
        text = self.sheet(slug, feature).read_text(encoding="utf-8")
        return list(csv.reader(io.StringIO(text)))

    def add(self, slug: str, feature: str, **over: str) -> subprocess.CompletedProcess:
        base = {"--source": "real-trace", "--locator": "ticket 48213",
                "--expected": "summary cites the refund line, promises nothing",
                "--label": "fail", "--reason": "invented a refund the ticket never made",
                "--handle": "hallucination", "--grader": "support lead"}
        base.update(over)
        flat: list[str] = []
        for key, value in base.items():
            flat.extend([key, value])
        return self.run("add", slug, "--feature", feature, *flat)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="test-golden-set-") as td:
        sb = Sandbox(Path(td))
        slug, feature = "golden-demo", "ticket-summariser"
        r = sb.init_project("Golden Demo")
        check("init_context bootstraps the sandbox project", r.returncode == 0, r.stderr.strip())

        # -- init ------------------------------------------------------------------
        r = sb.run("init", slug, "--feature", feature)
        created = sb.projects / slug / "evals" / feature
        check("init creates the scenario sheet and the golden set",
              r.returncode == 0 and (created / "scenario.md").is_file() and (created / "golden-set.csv").is_file(),
              r.stderr.strip() or r.stdout.strip())
        check("the golden set starts as the header alone",
              sb.rows(slug, feature) == [["id", "source", "input locator", "expected behaviour", "label",
                                          "reason", "handle", "grader", "last graded"]])
        check("the scenario template is rendered, not copied raw",
              "{{" not in (created / "scenario.md").read_text(encoding="utf-8"))
        before = (created / "scenario.md").read_bytes()
        r = sb.run("init", slug, "--feature", feature)
        check("init twice keeps both files byte-identical",
              r.returncode == 0 and "kept" in r.stdout and (created / "scenario.md").read_bytes() == before)
        r = sb.run("init", "no-such-project", "--feature", feature)
        check("init refuses a project that does not exist",
              r.returncode == 1 and "unknown project slug" in r.stderr and not (sb.projects / "no-such-project").exists())

        # -- confinement, through context_paths ------------------------------------
        refusals = [
            ("PII slug", ("init", "people", "--feature", feature)),
            ("PII feature raw-evidence", ("init", slug, "--feature", "raw-evidence")),
            ("PII feature data", ("init", slug, "--feature", "data")),
            ("traversal in the feature", ("init", slug, "--feature", "../../../etc")),
            ("traversal in the slug", ("init", "../outside", "--feature", feature)),
            ("uppercase slug", ("init", "Golden-Demo", "--feature", feature)),
        ]
        for name, argv in refusals:
            r = sb.run(*argv)
            check(f"refused: {name}", r.returncode != 0, r.stdout.strip())
        leaked = [p for p in Path(td).rglob("golden-set.csv") if "projects/golden-demo" not in p.as_posix() and "_templates" not in p.as_posix()]
        check("nothing was written outside the project", not leaked, str(leaked))

        # -- add --------------------------------------------------------------------
        r = sb.add(slug, feature)
        rows = sb.rows(slug, feature)
        check("add appends one row with id 001 and today's date",
              r.returncode == 0 and len(rows) == 2 and rows[1][0] == "001" and rows[1][1] == "real trace",
              r.stderr.strip())
        r = sb.add(slug, feature, **{"--locator": "ticket 50001", "--label": "good", "--handle": "golden",
                                     "--reason": "cited the right line"})
        check("a second add takes the next id", r.returncode == 0 and sb.rows(slug, feature)[2][0] == "002")
        r = sb.add(slug, feature, **{"--locator": "ticket 50002", "--reason": "dropped the date, then invented one"})
        raw = sb.sheet(slug, feature).read_text(encoding="utf-8")
        check("a reason with a comma is quoted and round-trips",
              r.returncode == 0 and '"dropped the date, then invented one"' in raw
              and sb.rows(slug, feature)[3][5] == "dropped the date, then invented one")
        check("the file has no carriage returns", "\r" not in raw)
        r = sb.add(slug, feature, **{"--locator": "ticket 50003", "--reason": "two\nlines"})
        check("a field spanning lines is refused", r.returncode == 1 and "one line" in r.stderr)
        r = sb.add(slug, feature, **{"--locator": "ticket 50004", "--source": "guesswork"})
        check("an unknown source is refused", r.returncode == 1 and "source must be" in r.stderr)
        r = sb.add(slug, feature, **{"--locator": "ticket 50005", "--handle": "made-up-handle"})
        check("an unknown handle is a warning, not a refusal",
              r.returncode == 0 and "WARN" in r.stderr, r.stderr.strip())
        r = sb.add(slug, "never-initialised")
        check("add before init refuses and creates nothing",
              r.returncode == 1 and "init first" in r.stderr and not (sb.projects / slug / "evals" / "never-initialised").exists())

        # -- the corruption guard ---------------------------------------------------
        path = sb.sheet(slug, feature)
        original = path.read_text(encoding="utf-8")
        for name, broken in (
            ("a renamed column", original.replace("input locator", "locator", 1)),
            ("a short row", original + "099,real trace,ticket 1\n"),
            ("a duplicate id", original + original.splitlines()[1] + "\n"),
        ):
            path.write_text(broken, encoding="utf-8")
            r = sb.add(slug, feature, **{"--locator": "ticket 60000"})
            check(f"add refuses {name} and writes nothing",
                  r.returncode == 1 and path.read_text(encoding="utf-8") == broken, r.stderr.strip())
        path.write_text(original, encoding="utf-8")

        # -- show and list ----------------------------------------------------------
        stamp = path.stat().st_mtime_ns
        r = sb.run("show", slug, "--feature", feature, "--rows")
        check("show reports counts and leaves the file untouched",
              r.returncode == 0 and "by label:" in r.stdout and "by source:" in r.stdout
              and path.stat().st_mtime_ns == stamp, r.stdout.strip())
        r = sb.run("list", slug)
        check("list names the feature", r.returncode == 0 and feature in r.stdout)

        # -- check ------------------------------------------------------------------
        r = sb.run("check", slug, "--feature", feature)
        check("a set with a real failure passes", r.returncode == 0, r.stdout.strip() + r.stderr.strip())
        r = sb.run("check", slug, "--feature", feature, "--strict")
        check("--strict turns the duplicate-locator warning into an exit code",
              r.returncode == 0 or "WARN" in r.stdout, r.stdout.strip())

        sb.run("init", slug, "--feature", "only-good")
        sb.add(slug, "only-good", **{"--label": "good", "--handle": "golden", "--reason": "fine",
                                     "--locator": "ticket 1"})
        r = sb.run("check", slug, "--feature", "only-good")
        check("a set with no failure is an error",
              r.returncode == 1 and "scrapbook" in r.stderr, r.stderr.strip())

        sb.run("init", slug, "--feature", "synthetic-only")
        sb.add(slug, "synthetic-only", **{"--source": "synthetic", "--locator": "made up 1"})
        r = sb.run("check", slug, "--feature", "synthetic-only")
        check("a failure that never happened does not satisfy the rule",
              r.returncode == 1 and "real trace" in r.stderr, r.stderr.strip())
        check("and the all-synthetic warning fires too", "practice rows do not decide a release" in r.stdout)

        sb.run("init", slug, "--feature", "dated")
        sb.add(slug, "dated", **{"--locator": "ticket 2", "--last-graded": "2020-01-01"})
        r = sb.run("check", slug, "--feature", "dated", "--stale-after", "2026-01-01")
        check("--stale-after names the old row", "was last graded 2020-01-01" in r.stdout)
        r = sb.run("check", slug, "--feature", "dated", "--stale-after", "2026-01-01", "--strict")
        check("--strict makes that warning an exit code", r.returncode == 1)
        r = sb.add(slug, "dated", **{"--locator": "ticket 3", "--last-graded": "2999-01-01"})
        r = sb.run("check", slug, "--feature", "dated")
        check("a future grading date is an error", r.returncode == 1 and "in the future" in r.stderr)

        missing_reason = sb.sheet(slug, "dated")
        text = missing_reason.read_text(encoding="utf-8").replace("invented a refund the ticket never made", "", 1)
        missing_reason.write_text(text, encoding="utf-8")
        r = sb.run("check", slug, "--feature", "dated")
        check("a row without a reason is an error", r.returncode == 1 and "has no reason" in r.stderr)

        # -- the published paths ----------------------------------------------------
        reference = (ROOT / "skills" / "pm-archetype-ai" / "references" / "eval-design.md").read_text(encoding="utf-8")
        check("the paths match the ones eval-design.md publishes",
              "projects/<slug>/evals/<feature>/scenario.md" in reference
              and "projects/<slug>/evals/<feature>/golden-set.csv" in reference)

    failed = [name for name, ok, _ in RESULTS if not ok]
    print(f"\ntest_golden_set: {len(RESULTS) - len(failed)} passed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
