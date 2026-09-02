#!/usr/bin/env python3
"""
test_memory.py — sandboxed cases for memory.py's caps, distill fold, and the
in-code PII denylist.

Each case runs the real scripts/memory.py (and init_context.py) copied into a
throwaway repo skeleton, then inspects the files they wrote. Nothing touches
the live .ai/memory tree. Shape mirrors test_hooks.py: PASS/FAIL per case,
exit 1 if any case fails.

Usage: python3 scripts/test_memory.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))


class Sandbox:
    def __init__(self, tmp: Path):
        self.root = tmp
        (tmp / "scripts").mkdir()
        shutil.copy(ROOT / "scripts" / "memory.py", tmp / "scripts" / "memory.py")
        shutil.copy(ROOT / "scripts" / "init_context.py", tmp / "scripts" / "init_context.py")
        shutil.copytree(ROOT / ".ai" / "memory" / "_templates", tmp / ".ai" / "memory" / "_templates")
        self.mem = tmp / ".ai" / "memory"
        self.projects = self.mem / "projects"

    def run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(self.root / "scripts" / "memory.py"), *args],
                              capture_output=True, text=True, cwd=self.root)

    def init(self, name: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(self.root / "scripts" / "init_context.py"), name],
                              capture_output=True, text=True, cwd=self.root)

    def project(self, slug: str) -> Path:
        return self.projects / slug

    def read(self, slug: str, name: str) -> str:
        return (self.project(slug) / name).read_text(encoding="utf-8")

    def write(self, slug: str, name: str, text: str) -> None:
        (self.project(slug) / name).write_text(text, encoding="utf-8")

    def pkg(self, slug: str) -> Path:
        return self.project(slug) / ".distill"

    def manifest(self, slug: str) -> dict:
        return json.loads((self.pkg(slug) / "manifest.json").read_text(encoding="utf-8"))

    def fill_synthesis(self, slug: str, body: str) -> None:
        path = self.pkg(slug) / "synthesis.md"
        text = path.read_text(encoding="utf-8")
        head, _, tail = text.partition("\n\n")
        # keep the dated heading, replace the [Fill in ...] paragraph, keep the index
        rest = tail.split("\n\n", 1)[1] if "\n\n" in tail else ""
        path.write_text(f"{head}\n\n{body}\n\n{rest}", encoding="utf-8")


def blocks_of(text: str) -> list[str]:
    import re
    parts = re.split(r"(?m)^(?=## )", text)
    return parts[1:]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="test-memory-") as td:
        sb = Sandbox(Path(td))
        slug = "distill-demo"
        r = sb.init("Distill Demo")
        check("init_context bootstraps the sandbox project", r.returncode == 0, r.stderr.strip())

        # 1. fresh project: everything within caps
        r = sb.run("distill", slug)
        check("fresh project: distill reports nothing to fold (exit 0)",
              r.returncode == 0 and "within caps" in r.stdout, r.stdout + r.stderr)

        # 2. three ~3 KB entries push changelog.md over its 6144 B cap
        for n in (1, 2, 3):
            sb.run("log", slug, f"entry {n} " + ("lorem ipsum dolor sit amet " * 110), "--title", f"t{n}")
        size = (sb.project(slug) / "changelog.md").stat().st_size
        r = sb.run("distill", slug)
        d = sb.run("doctor")
        check("changelog over cap: distill exits 2 and doctor WARNs",
              size > 6144 and r.returncode == 2 and d.returncode == 0
              and "changelog.md" in d.stdout and "WARN" in d.stdout,
              f"size={size} distill={r.returncode} doctor={d.returncode} {d.stdout.strip()}")

        # 3. prepare: manifest oldest-first, blocks.md verbatim, synthesis rendered
        before = sb.read(slug, "changelog.md")
        r = sb.run("distill", slug, "--prepare")
        m = sb.manifest(slug)
        entries = blocks_of(before)
        folded = [entries[i] for i in sorted(b["index"] for b in m["blocks"])]
        blocks_md = (sb.pkg(slug) / "blocks.md").read_text(encoding="utf-8")
        synth = (sb.pkg(slug) / "synthesis.md").read_text(encoding="utf-8")
        check("prepare: package written, source untouched",
              r.returncode == 0 and sb.read(slug, "changelog.md") == before, r.stderr.strip())
        check("prepare: folds 2 of 3 entries and keeps the newest (t3)",
              len(m["blocks"]) == 2 and all("t3" not in b["heading"] for b in m["blocks"]),
              str([b["heading"] for b in m["blocks"]]))
        check("prepare: manifest lists blocks oldest first (t1 before t2)",
              [b["heading"][-2:] for b in m["blocks"]] == ["t1", "t2"],
              str([b["heading"] for b in m["blocks"]]))
        check("prepare: blocks.md is the folded blocks verbatim, in file order",
              blocks_md == "".join(folded))
        check("prepare: synthesis rendered (no {{key}} left, dated heading, index lines)",
              "{{" not in synth and synth.startswith("## ") and synth.count("\n- ") == 2)

        # 4. apply with the skeleton untouched -> exit 1, nothing changes
        r = sb.run("distill", slug, "--apply")
        check("apply with untouched skeleton refuses (exit 1) and writes nothing",
              r.returncode == 1 and sb.read(slug, "changelog.md") == before
              and not (sb.project(slug) / "changelog-archive.md").exists(), r.stderr.strip())
        r = sb.run("distill", slug, "--prepare")
        check("prepare refuses while a valid pending package exists",
              r.returncode == 1 and "pending" in r.stderr, r.stderr.strip())

        # 5. filled synthesis applies: verbatim archive, newest intact, size under cap
        sb.fill_synthesis(slug, "Kept: entries t1 and t2 said lorem ipsum; the decision stands.")
        r = sb.run("distill", slug, "--apply")
        after = sb.read(slug, "changelog.md")
        archive = sb.read(slug, "changelog-archive.md")
        check("apply: exit 0, folded blocks byte-for-byte in changelog-archive.md",
              r.returncode == 0 and all(b in archive for b in folded), r.stderr.strip())
        check("apply: newest entry intact, synthesis in place, source under cap",
              entries[0] in after and "Distilled: 2 block(s)" in after
              and "Folded blocks (verbatim in `changelog-archive.md`)" in after
              and after.count("\n- 2") >= 2
              and len(after.encode()) <= 6144)
        r = sb.run("distill", slug)
        check("after apply: distill is back to exit 0", r.returncode == 0)
        check("apply: manifest marked applied", sb.manifest(slug)["applied"] is True)

        # 6. second apply is refused (idempotent)
        r = sb.run("distill", slug, "--apply")
        check("second apply refused (exit 1), nothing changes",
              r.returncode == 1 and sb.read(slug, "changelog.md") == after
              and sb.read(slug, "changelog-archive.md") == archive)

        # 7. stale package: source changed after prepare -> apply refuses
        r = sb.run("distill", slug, "--prepare", "--file", "changelog")
        check("explicit --file under cap folds exactly one block",
              r.returncode == 0 and len(sb.manifest(slug)["blocks"]) == 1, r.stderr.strip())
        sb.run("log", slug, "a new entry after prepare", "--title", "t4")
        sb.fill_synthesis(slug, "Folded one older block.")
        r = sb.run("distill", slug, "--apply")
        check("stale package (source changed) refused with exit 1",
              r.returncode == 1 and "changed since" in r.stderr, r.stderr.strip())
        r = sb.run("distill", slug, "--prepare", "--file", "changelog")
        check("a stale pending package can be replaced by a new --prepare", r.returncode == 0, r.stderr.strip())

        # 8. apply binds the package to its project and canonical metadata,
        # and requires the dated heading that makes future folds discoverable.
        src_before = sb.read(slug, "changelog.md")
        arch_before = sb.read(slug, "changelog-archive.md")
        manifest_path = sb.pkg(slug) / "manifest.json"
        manifest = sb.manifest(slug)
        manifest["slug"] = "another-project"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        r = sb.run("distill", slug, "--apply")
        check("apply refuses a package prepared for another project",
              r.returncode == 1 and "belongs to project" in r.stderr
              and sb.read(slug, "changelog.md") == src_before
              and sb.read(slug, "changelog-archive.md") == arch_before, r.stderr.strip())

        manifest["slug"] = slug
        manifest["cap"] = 100_000
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        r = sb.run("distill", slug, "--apply")
        check("apply refuses a manifest that weakens the canonical cap",
              r.returncode == 1 and "canonical contract" in r.stderr
              and sb.read(slug, "changelog.md") == src_before
              and sb.read(slug, "changelog-archive.md") == arch_before, r.stderr.strip())

        manifest["cap"] = 6144
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        sb.fill_synthesis(slug, "A concise synthesis that keeps the decision.")
        synthesis_path = sb.pkg(slug) / "synthesis.md"
        synthesis = synthesis_path.read_text(encoding="utf-8")
        synthesis_path.write_text(synthesis.replace(synthesis.splitlines()[0], "## Distilled summary", 1),
                                  encoding="utf-8")
        r = sb.run("distill", slug, "--apply")
        check("apply refuses an undated synthesis heading",
              r.returncode == 1 and "dated" in r.stderr
              and sb.read(slug, "changelog.md") == src_before
              and sb.read(slug, "changelog-archive.md") == arch_before, r.stderr.strip())

        # 9. synthesis over cap: exit 2, source and archive untouched
        shutil.rmtree(sb.pkg(slug))
        r = sb.run("distill", slug, "--prepare", "--file", "changelog")
        sb.fill_synthesis(slug, "x" * 7000)
        r = sb.run("distill", slug, "--apply")
        check("oversized synthesis: exit 2, source and archive untouched",
              r.returncode == 2 and sb.read(slug, "changelog.md") == src_before
              and sb.read(slug, "changelog-archive.md") == arch_before, r.stderr.strip())
        shutil.rmtree(sb.pkg(slug))

        # 10. state.md: template example block is undated and never folded
        parked = "".join(
            f"## Parked 2026-0{m}-01\n\n- **Current stage**: discovery\n- session {m}\n\n" for m in range(6, 0, -1)
        )
        example = "## <Active|Parked|Closed> YYYY-MM-DD\n\n- **Current stage**: <discovery|define>\n- example\n"
        sb.write(slug, "state.md", "# State — Distill Demo\n\n> Newest first.\n\n" + parked + example)
        r = sb.run("distill", slug, "--prepare", "--file", "state")
        m = sb.manifest(slug)
        sb.fill_synthesis(slug, "January session folded.")
        a = sb.run("distill", slug, "--apply")
        state = sb.read(slug, "state.md")
        sarch = sb.read(slug, "state-archive.md")
        check("state.md: oldest Parked block folded, example block never folded",
              r.returncode == 0 and a.returncode == 0 and m["blocks"][0]["date"] == "2026-01-01"
              and example in state and "YYYY-MM-DD" not in sarch
              and "## Parked 2026-01-01" in sarch and "## Parked 2026-06-01" in state,
              (r.stderr + a.stderr).strip())
        check("state-archive.md created with its own header",
              sarch.startswith("# State archive"))
        shutil.rmtree(sb.pkg(slug))

        # 11. decisions.md: two heading separators, equal dates -> file order (oldest-first)
        sb.write(slug, "decisions.md",
                 "# Decisions\n\nUse one heading per decision.\n\n"
                 "## 2026-09-01 — First decision\n\n- **Choice**: A\n\n"
                 "## 2026-09-01: Second decision\n\n- **Choice**: B\n\n")
        r = sb.run("distill", slug, "--prepare", "--file", "decisions")
        m = sb.manifest(slug)
        sb.fill_synthesis(slug, "First decision folded; A still binds.")
        a = sb.run("distill", slug, "--apply")
        dec = sb.read(slug, "decisions.md")
        darch = sb.read(slug, "decisions-archive.md")
        check("decisions.md: same-date tie folds the earlier block (oldest-first convention)",
              r.returncode == 0 and a.returncode == 0 and m["blocks"][0]["heading"].endswith("First decision")
              and "First decision" in darch and "## 2026-09-01: Second decision" in dec
              and darch.startswith("# Decisions archive"),
              (r.stderr + a.stderr).strip())

        # 12. explicit fold with a single dated block -> refused (the synthesis
        # block written by 11 is itself dated, so that file still has two; build
        # the one-block case explicitly)
        shutil.rmtree(sb.pkg(slug))
        sb.write(slug, "decisions.md",
                 "# Decisions\n\nUse one heading per decision.\n\n"
                 "## 2026-09-01 — Only decision\n\n- **Choice**: A\n\n")
        r = sb.run("distill", slug, "--prepare", "--file", "decisions")
        check("one dated block cannot be folded (needs two, exit 1)",
              r.returncode == 1 and "at least two" in r.stderr, r.stderr.strip())

        # 13. PII denylist in code: a project literally named 'data' is refused
        sb.run("park", slug)
        r = sb.init("data")
        lg = sb.run("log", "data", "x")
        pr = sb.run("distill", "data", "--prepare")
        dc = sb.run("doctor")
        check("denylist: init creates projects/data but memory.py log refuses it",
              r.returncode == 0 and lg.returncode == 1 and "PII" in lg.stderr, lg.stderr.strip())
        check("denylist: distill --prepare refuses the PII project",
              pr.returncode == 1 and "PII" in pr.stderr, pr.stderr.strip())
        check("doctor skips the PII project with a WARN and still exits 0",
              dc.returncode == 0 and "PII path" in dc.stdout, dc.stdout.strip())

    failures = [r for r in RESULTS if not r[1]]
    if failures:
        print(f"\ntest_memory: {len(failures)}/{len(RESULTS)} case(s) failed")
        return 1
    print(f"\ntest_memory: all {len(RESULTS)} case(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
