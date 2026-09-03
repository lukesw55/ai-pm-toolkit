#!/usr/bin/env python3
"""
test_memory.py — sandboxed cases for memory.py's caps, distill fold, the
cold-layer archive index, and the in-code PII denylist.

Each case runs the real scripts/memory.py (and init_context.py) copied into a
throwaway repo skeleton, then inspects the files they wrote. Nothing touches
the live .ai/memory tree. Shape mirrors test_hooks.py: PASS/FAIL per case,
exit 1 if any case fails.

Usage: python3 scripts/test_memory.py
"""

from __future__ import annotations

import json
import re
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


INDEX_MARKER = "Index (one line per archived block"


def blocks_of(text: str) -> list[str]:
    parts = re.split(r"(?m)^(?=## )", text)
    return parts[1:]


def index_block(text: str) -> str:
    m = re.search(r"(?ms)^" + re.escape(INDEX_MARKER) + r".*?\n\n", text)
    return m.group(0) if m else ""


def index_lines(text: str) -> list[str]:
    return [ln for ln in index_block(text).splitlines() if ln.startswith("- ")]


def heading_lines(text: str) -> list[str]:
    """The index the archive should carry, re-derived from its own block headings
    here rather than by calling memory.py, so the two can disagree."""
    out = []
    for block in blocks_of(text):
        head = block.splitlines()[0].lstrip("#").strip()
        m = re.search(r"\d{4}-\d{2}-\d{2}", head)
        date = m.group(0) if m else "0000-00-00"
        rest = re.sub(r"\d{4}-\d{2}-\d{2}:?\s*", "", head, count=1).strip()
        out.append(f"- {date} {rest}".rstrip())
    return out


def drop_index(text: str) -> str:
    return text.replace(index_block(text), "", 1)


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

        # 13. cold layer: the archive index block (grep-first retrieval)
        archive = sb.project(slug) / "changelog-archive.md"
        r = sb.run("log", slug, "an entry that pushes the oldest one out", "--title", "ix1")
        arch = archive.read_text(encoding="utf-8")
        check("rotation regenerates the index: one line per archived block, file order",
              r.returncode == 0 and INDEX_MARKER in arch and len(blocks_of(arch)) >= 1
              and index_lines(arch) == heading_lines(arch),
              f"{len(index_lines(arch))} line(s) vs {len(blocks_of(arch))} block(s)")

        r = sb.run("log", slug, "and one more after that", "--title", "ix2")
        arch2 = archive.read_text(encoding="utf-8")
        check("a second rotation extends the index instead of duplicating lines",
              r.returncode == 0 and index_lines(arch2) == heading_lines(arch2)
              and len(blocks_of(arch2)) == len(blocks_of(arch)) + 1,
              f"{len(index_lines(arch2))} line(s) vs {len(blocks_of(arch2))} block(s)")

        archive.write_text(drop_index(arch2), encoding="utf-8")
        r = sb.run("index", slug)
        once = archive.read_text(encoding="utf-8")
        r2 = sb.run("index", slug)
        twice = archive.read_text(encoding="utf-8")
        check("index rebuilds a missing index block, lists it, and is idempotent",
              r.returncode == 0 and r2.returncode == 0 and once == twice
              and index_lines(once) == heading_lines(once)
              and "changelog-archive.md" in r.stdout and index_lines(once)[0] in r.stdout,
              (r.stderr + r2.stderr).strip())
        check("rebuild keeps every pre-existing block byte-for-byte, in the same order",
              blocks_of(once) == blocks_of(arch2))

        sarch = sb.read(slug, "state-archive.md")
        check("index line drops the date the heading already carries (state.md blocks)",
              "- 2026-01-01 Parked" in sarch and index_lines(sarch) == heading_lines(sarch),
              str(index_lines(sarch)))

        archive.write_text(once.replace(index_lines(once)[0] + "\n", "", 1), encoding="utf-8")
        d = sb.run("doctor")
        fix = sb.run("index", slug)
        d2 = sb.run("doctor")
        check("doctor WARNs on a stale index and goes quiet once index rebuilds it",
              d.returncode == 0 and "archive index stale" in d.stdout and fix.returncode == 0
              and "archive index stale" not in d2.stdout, d.stdout.strip())

        # a failure before os.replace must leave the live archive untouched. The
        # staging path is occupied by a directory, so the write fails for any
        # user, root included.
        archive.write_text(drop_index(archive.read_text(encoding="utf-8")), encoding="utf-8")
        before = archive.read_bytes()
        blocker = archive.with_name(archive.name + ".tmp")
        blocker.mkdir()
        broken = sb.run("index", slug)
        mid = archive.read_bytes()
        blocker.rmdir()
        rec = sb.run("index", slug)
        recovered = archive.read_text(encoding="utf-8")
        check("a failure before the replace leaves the archive intact; index recovers after",
              broken.returncode != 0 and mid == before and rec.returncode == 0
              and index_lines(recovered) == heading_lines(recovered),
              f"exit={broken.returncode} {broken.stderr.strip()}")

        for n in range(4):
            sb.run("log", "repo", f"repo entry {n}", "--title", f"r{n}")
        root_archive = sb.root / ".ai" / "changelog-archive.md"
        root_archive.write_text(drop_index(root_archive.read_text(encoding="utf-8")), encoding="utf-8")
        r = sb.run("index", "repo")
        ra = root_archive.read_text(encoding="utf-8")
        check("index repo rebuilds and lists .ai/changelog-archive.md",
              r.returncode == 0 and index_lines(ra) == heading_lines(ra)
              and "changelog-archive.md" in r.stdout, (r.stdout + r.stderr).strip())

        formats = ("# Decisions archive\n\n> Rotated out of `decisions.md`. Full entries, verbatim.\n\n"
                   "## 2026-03-01: colon heading\n\n- body\n\n"
                   "## Parked 2026-03-02\n\n- body\n\n"
                   "## 2026-03-03 — dash heading\n\n- body\n\n")
        sb.write(slug, "decisions-archive.md", formats)
        r = sb.run("index", slug)
        darch = sb.read(slug, "decisions-archive.md")
        check("the index line covers the three heading shapes the archives use",
              r.returncode == 0 and index_lines(darch) == ["- 2026-03-01 colon heading",
                                                           "- 2026-03-02 Parked",
                                                           "- 2026-03-03 — dash heading"],
              str(index_lines(darch)))

        stale_header = INDEX_MARKER + ", file order; grep here before opening a block):"
        sb.write(slug, "decisions-archive.md",
                 "# Decisions archive\n\n> Rotated out of `decisions.md`. Full entries, verbatim.\n\n"
                 + stale_header + "\n- 1999-01-01 a line that no longer matches any block\n"
                 "## 2026-03-01: colon heading\n\n- body\n\n")
        r = sb.run("index", slug)
        fixed = sb.read(slug, "decisions-archive.md")
        check("an index block missing its blank line is replaced, not duplicated, and the header survives",
              r.returncode == 0 and fixed.count(INDEX_MARKER) == 1 and "1999-01-01" not in fixed
              and fixed.startswith("# Decisions archive")
              and "> Rotated out of `decisions.md`" in fixed
              and index_lines(fixed) == heading_lines(fixed), fixed[:170])

        # 14. PII denylist in code: a project literally named 'data' is refused
        sb.run("park", slug)
        r = sb.init("data")
        lg = sb.run("log", "data", "x")
        pr = sb.run("distill", "data", "--prepare")
        ix = sb.run("index", "data")
        dc = sb.run("doctor")
        check("denylist: init creates projects/data but memory.py log refuses it",
              r.returncode == 0 and lg.returncode == 1 and "PII" in lg.stderr, lg.stderr.strip())
        check("denylist: distill --prepare refuses the PII project",
              pr.returncode == 1 and "PII" in pr.stderr, pr.stderr.strip())
        check("denylist: index refuses the PII project too",
              ix.returncode == 1 and "PII" in ix.stderr, ix.stderr.strip())
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
