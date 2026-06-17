#!/usr/bin/env python3
"""
grade_evals.py — Grade eval runs across all 7 PM skills.

Walks .claude/skills/<skill>/workspace/iteration-1/ and produces:
- grading.json per run (with_skill + without_skill)
- benchmark.json per skill
- aggregated benchmark_all.json
- eval-report.html (static viewer)
"""

import json
import re
import statistics
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / ".claude" / "skills"

# Assertions per (skill, eval_name) — each is (label, callable taking normalised text → bool)
def has(p: str):
    return lambda t: p.lower() in t

def hasr(pattern: str):
    rx = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    return lambda t: bool(rx.search(t))

def not_has(p: str):
    return lambda t: p.lower() not in t

ASSERTIONS = {
    "pm-phase-discover": {
        "problem-framing-from-stakeholder-asks": [
            ("Names a specific target user (not just 'users')", hasr(r"target user|new user|admin|segment|persona")),
            ("Identifies invalidation / what would change conclusion", hasr(r"invalidation|would change|would flip|would be wrong")),
            ("Parks / tables stakeholder asks rather than picking one", hasr(r"park|stakeholder|(?:ask|request)s? (?:are|will be|remain)|not commit")),
            ("Names next learning step before committing", hasr(r"next (learning )?step|next action|next move|first learn|before (?:any )?solution")),
            ("Separates known evidence from assumed", hasr(r"known|evidence|assumed|assumption")),
            ("Avoids committing to a specific proposed solution", lambda t: not re.search(r"(?:we will|let's|let us|recommend(?:ing)?) (?:ship|build|adopt|implement|deploy) (?:the )?(?:guided tour|ai.powered|simplified signup|tooltip)", t)),
        ],
        "research-plan-for-b2b-approvals": [
            ("Includes research questions (explicit list)", hasr(r"research question|rq\s*\d|\d\.\s|q\d:")),
            ("Justifies method choice", hasr(r"why|rationale|because|chosen|method")),
            ("Specifies sample + recruitment criteria", hasr(r"sample|recruit|n\s*=|participant|admin")),
            ("Includes interview guide or sample questions", hasr(r"interview guide|questions?:|guide|prompt")),
            ("Describes synthesis / coding approach", hasr(r"synthesi[sz]|coding|themes?|affinity")),
            ("Mentions triangulation with quant / existing data", hasr(r"triangul|quant|telemetry|analytics|data")),
        ],
    },
    "pm-phase-define": {
        "kpi-tree-for-b2b-onboarding": [
            ("Defines an explicit North Star metric", hasr(r"north star")),
            ("Provides at least one metric formula", hasr(r"formula|count|=|÷|/|sum")),
            ("Names guardrail metrics", hasr(r"guardrail")),
            ("Identifies missing instrumentation", hasr(r"instrument|missing|need to track|not tracked|add tracking|p0|p1")),
            ("Has multi-layer tree (inputs + sub-inputs)", hasr(r"input|layer|level|sub-input|layer 2|layer 1")),
            ("Names metric owners", hasr(r"owner|@\w+|pm:|growth pm|cs ops|analytics")),
        ],
        "prioritise-6-q3-initiatives": [
            ("Picks a named framework (RICE/WSJF/etc)", hasr(r"rice|wsjf|cost of delay|moscow|kano|scorecard")),
            ("Produces a ranked list", hasr(r"\b1\.|#1|rank|ranked")),
            ("Explicit non-funded items with rationale", hasr(r"not funded|not funding|defund|dropped|cut|rejected|parked")),
            ("Acknowledges assumptions / weak evidence", hasr(r"assumption|weak evidence|confidence|to be validated|flag")),
            ("References the 18 person-week capacity", hasr(r"18|pw|person.week|capacity|budget")),
            ("Compares discovery-level vs build-level bets", hasr(r"discovery|delivery|build|prd.ready")),
        ],
    },
    "pm-phase-develop": {
        "prd-csv-export-dashboard": [
            ("Has TL;DR section", hasr(r"tl;dr|tldr|summary")),
            ("Both goals and non-goals named", lambda t: ("goal" in t) and ("non.goal" in t or "out of scope" in t)),
            ("Testable acceptance criteria (given/when/then or bullet ACs)", hasr(r"given.*when.*then|acceptance criteria|\[ ?\]|\[x\]")),
            ("Tracking plan with ≥3 events + properties", hasr(r"event|property|properties|export_|tracking")),
            ("Release plan with rollback criteria", hasr(r"rollback|rollout|feature flag|gradual|canary")),
            ("Primary metric with baseline + target", hasr(r"primary metric|baseline|target|week \d")),
            ("Guardrails named", hasr(r"guardrail|p95|support|error")),
        ],
        "slice-sso-epic-into-stories": [
            ("MVP, R2, R3 all present", lambda t: ("mvp" in t or "r1" in t) and ("r2" in t or "release 2" in t) and ("r3" in t or "release 3" in t)),
            ("Stories framed as user outcomes (admin/end-user can)", hasr(r"admin (?:can|configures|turns|sees)|end user|user can|as an admin")),
            ("Non-goals at epic level", hasr(r"non.goal|out of scope|deferred|defer")),
            ("MVP sized for 4 weeks", hasr(r"4.?week|four week|week 4|4w|mvp.*week")),
            ("Learning outcomes / success criteria per release", hasr(r"learn|success criteria|measur|gate")),
        ],
    },
    "pm-phase-deliver": {
        "pricing-v2-launch-package": [
            ("Public changelog / release note present", hasr(r"changelog|release note|public|what's new")),
            ("Internal enablement for sales/CS/support", hasr(r"enable|sales|cs|support|talking point")),
            ("Customer email to admins", hasr(r"email|subject:|hi |dear |hello ")),
            ("Post-launch monitoring plan", hasr(r"monitor|post.launch|scorecard|primary metric")),
            ("Explicit rollback criteria", hasr(r"rollback|revert|rollback criter")),
            ("Mentions 12-month grandfathering", hasr(r"grandfather|12.month|grandfathered|migration")),
            ("Honest tone (acknowledges bills may rise)", hasr(r"pay more|higher|increase|honest|transparent|bill|cost.*up")),
        ],
        "interpret-onboarding-ab-test": [
            ("Gives a clear ship/iterate/kill/extend recommendation", hasr(r"ship|iterate|kill|extend|recommend")),
            ("Breaks out by Free/Pro/Enterprise segments", lambda t: ("free" in t) and ("pro" in t) and ("enterprise" in t)),
            ("Treats support-ticket lift as a guardrail concern", hasr(r"support ticket|guardrail|confused|12%")),
            ("Considers validity (SRM, novelty, concurrent tests, sample)", hasr(r"srm|novelty|sample|concurrent|validity|power")),
            ("Comments on practical vs statistical significance", hasr(r"practical|ci|confidence interval|magnitude|meaningful")),
        ],
    },
    "pm-transversal-stakeholder": {
        "daci-api-v1-deprecation": [
            ("Names a single approver", hasr(r"approver:|approver\s*=|approver.*@|approver is|vp.*approver|vp product")),
            ("Populates Driver, Contributors, Informed all four roles", lambda t: ("driver" in t) and ("contributor" in t) and ("informed" in t)),
            ("At least 3 options compared", hasr(r"option a.*option b.*option c|option 1.*option 2.*option 3|3 options|three options")),
            ("Has timeline with concrete dates / months", hasr(r"202[5-9]|month\s*\d|m\d|week \d|q[1-4]|day\s*\d")),
            ("Has specific ask + decision date", hasr(r"decision date|by (?:friday|next week|\w+ \d+)|approve by|sign.off by|decision by")),
        ],
        "exec-memo-slip-risk": [
            ("TL;DR up front", hasr(r"tl;dr|tldr|summary")),
            ("All three options (A, B, C) addressed", lambda t: ("option a" in t) and ("option b" in t) and ("option c" in t)),
            ("Clear recommendation stated", hasr(r"recommend|recommendation")),
            ("Ask with Friday / specific date", hasr(r"friday|decision by|approve by|by eod")),
            ("Risks named for the recommended option", hasr(r"risk|mitigat")),
            ("Concise (memo body under ~800 words)", lambda t: len(t.split()) < 850),
        ],
    },
    "pm-transversal-docs": {
        "confluence-prd-plus-jira-tickets": [
            ("Confluence page with title + status + links block", hasr(r"status:|owner:|related:|linked?:|title|updated")),
            ("Exactly one epic ticket", hasr(r"epic\b")),
            ("At least 4 stories", hasr(r"(?:story|story\s*\d|story[-\s]\d|EXP-10[2-9]|ADM-|stories)")),
            ("Bidirectional links mentioned", hasr(r"link|prd.*epic|epic.*prd|bidirectional|parent|child")),
            ("Acceptance criteria per story", hasr(r"given.*when.*then|acceptance criteria|\[ ?\]")),
            ("Labels / components / DoD present", hasr(r"label|component|definition of done|dod")),
        ],
        "ticket-hygiene-pass": [
            ("Refactors all 4 tickets", lambda t: sum(1 for n in ["ticket 1", "ticket 2", "ticket 3", "ticket 4"] if n in t) >= 3),
            ("Bug (#2) flagged needs-repro", hasr(r"repro|reproduc|steps to reproduce|needs.repro")),
            ("Backend task (#3) linked to user story", hasr(r"task|parent|blocks|blocked by|under story|belongs to")),
            ("Epic (#4) gets primary metric", hasr(r"primary metric|north star|activation|metric")),
            ("Epic (#4) gets MVP / slicing", hasr(r"mvp|r1|r2|slicing|slice|parking lot")),
            ("Open questions per refactor", hasr(r"open question|questions?(?:\s+for|\s+to ask)|pm question|would ask|ask the pm")),
            ("Mentions Definition of Ready or similar gate", hasr(r"definition of ready|dor|ready|not ready|needs")),
        ],
    },
    "pm-transversal-analysis": {
        "synthesise-5-interview-transcripts": [
            ("Ranks themes", hasr(r"theme 1|theme 2|ranked|rank|top theme")),
            ("Caveats sample size N=5", hasr(r"n ?= ?5|5 interview|sample size|saturation|directional")),
            ("Evidence strength per theme", hasr(r"strength|low|medium|high|confidence")),
            ("Segment pattern discussed", hasr(r"segment|seat|10.50|30.person|size|role")),
            ("Triangulation with quant suggested", hasr(r"triangul|quant|posthog|funnel|cohort|telemetry|analytics")),
            ("Counter-evidence / P02 or P05 acknowledged", hasr(r"p02|p05|counter|out of icp|not a priority|low engagement")),
            ("Pain vs request distinction", hasr(r"pain.*request|request.*pain|not the (?:same|solution)|solution.disguised|symptom")),
        ],
        "triangulate-checkout-confusion": [
            ("States combined confidence (low/med/high)", hasr(r"confidence: (?:low|medium|med|high)|confidence\s*[=:]|high confidence|medium confidence")),
            ("Assesses quali strength", hasr(r"quali|qualitative")),
            ("Assesses quant strength", hasr(r"quant|quantitative|funnel|42|drop")),
            ("Names what would change conclusion", hasr(r"would change|would flip|invalidat|would weaken|would overturn")),
            ("Specific next action (diagnostic, not generic)", hasr(r"step.level|session replay|instrument|diagnostic|re.interview|exit.intent|before redesign")),
            ("Acknowledges pattern alignment or mixed signal", hasr(r"aligned|pattern 1|both support|converge|reinforc|support each other")),
        ],
    },
}


def grade_run(output_path: Path, skill: str, eval_name: str):
    if not output_path.exists():
        return None
    text = output_path.read_text(encoding="utf-8", errors="replace").lower()
    checks = ASSERTIONS.get(skill, {}).get(eval_name, [])
    expectations = []
    for label, fn in checks:
        try:
            passed = bool(fn(text))
        except Exception as e:
            passed = False
            label = f"{label} (error: {e})"
        expectations.append({
            "text": label,
            "passed": passed,
            "evidence": "" if passed else "assertion did not match output",
        })
    total = len(expectations)
    passed_count = sum(1 for e in expectations if e["passed"])
    return {
        "expectations": expectations,
        "total": total,
        "passed": passed_count,
        "pass_rate": (passed_count / total) if total else 0.0,
        "word_count": len(text.split()),
    }


def load_timing(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def grade_all():
    results_by_skill = {}
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or not skill_dir.name.startswith("pm-"):
            continue
        skill = skill_dir.name
        iteration = skill_dir / "workspace" / "iteration-1"
        if not iteration.exists():
            continue
        skill_runs = []
        for eval_dir in sorted(iteration.iterdir()):
            if not eval_dir.is_dir():
                continue
            m = re.match(r"eval-(\d+)-(.+)", eval_dir.name)
            if not m:
                continue
            eval_id = int(m.group(1))
            eval_name = m.group(2)
            for config in ["with_skill", "without_skill"]:
                out = eval_dir / config / "outputs" / "output.md"
                timing = load_timing(eval_dir / config / "timing.json")
                grading = grade_run(out, skill, eval_name)
                if grading is None:
                    continue
                grading_path = eval_dir / config / "grading.json"
                grading_path.write_text(json.dumps(grading, indent=2))
                run = {
                    "skill": skill,
                    "eval_id": eval_id,
                    "eval_name": eval_name,
                    "config": config,
                    "grading": grading,
                    "timing": timing or {},
                    "output_path": str(out.relative_to(REPO)),
                }
                skill_runs.append(run)
        results_by_skill[skill] = skill_runs
    return results_by_skill


def aggregate_benchmark(results_by_skill):
    benchmark = {"skills": {}, "overall": {}}
    with_skill_rates = []
    baseline_rates = []
    with_skill_tokens = []
    baseline_tokens = []
    with_skill_durations = []
    baseline_durations = []

    for skill, runs in results_by_skill.items():
        skill_entry = {"evals": []}
        by_eval = {}
        for run in runs:
            by_eval.setdefault((run["eval_id"], run["eval_name"]), {})[run["config"]] = run
        for (eval_id, eval_name), configs in sorted(by_eval.items()):
            ws = configs.get("with_skill")
            bs = configs.get("without_skill")
            entry = {"eval_id": eval_id, "eval_name": eval_name}
            if ws:
                entry["with_skill"] = {
                    "pass_rate": ws["grading"]["pass_rate"],
                    "passed": ws["grading"]["passed"],
                    "total": ws["grading"]["total"],
                    "tokens": ws["timing"].get("total_tokens"),
                    "duration_ms": ws["timing"].get("duration_ms"),
                    "word_count": ws["grading"].get("word_count"),
                }
                with_skill_rates.append(ws["grading"]["pass_rate"])
                if ws["timing"].get("total_tokens"):
                    with_skill_tokens.append(ws["timing"]["total_tokens"])
                if ws["timing"].get("duration_ms"):
                    with_skill_durations.append(ws["timing"]["duration_ms"])
            if bs:
                entry["without_skill"] = {
                    "pass_rate": bs["grading"]["pass_rate"],
                    "passed": bs["grading"]["passed"],
                    "total": bs["grading"]["total"],
                    "tokens": bs["timing"].get("total_tokens"),
                    "duration_ms": bs["timing"].get("duration_ms"),
                    "word_count": bs["grading"].get("word_count"),
                }
                baseline_rates.append(bs["grading"]["pass_rate"])
                if bs["timing"].get("total_tokens"):
                    baseline_tokens.append(bs["timing"]["total_tokens"])
                if bs["timing"].get("duration_ms"):
                    baseline_durations.append(bs["timing"]["duration_ms"])
            skill_entry["evals"].append(entry)
        # skill-level aggregates
        skill_ws = [e["with_skill"]["pass_rate"] for e in skill_entry["evals"] if "with_skill" in e]
        skill_bs = [e["without_skill"]["pass_rate"] for e in skill_entry["evals"] if "without_skill" in e]
        skill_entry["summary"] = {
            "with_skill_pass_rate": statistics.mean(skill_ws) if skill_ws else None,
            "without_skill_pass_rate": statistics.mean(skill_bs) if skill_bs else None,
            "delta": (statistics.mean(skill_ws) - statistics.mean(skill_bs)) if skill_ws and skill_bs else None,
        }
        benchmark["skills"][skill] = skill_entry
        # write per-skill benchmark.json
        (SKILLS_DIR / skill / "workspace" / "iteration-1" / "benchmark.json").write_text(
            json.dumps(skill_entry, indent=2)
        )

    benchmark["overall"] = {
        "with_skill_pass_rate": statistics.mean(with_skill_rates) if with_skill_rates else None,
        "without_skill_pass_rate": statistics.mean(baseline_rates) if baseline_rates else None,
        "delta": (statistics.mean(with_skill_rates) - statistics.mean(baseline_rates)) if with_skill_rates and baseline_rates else None,
        "with_skill_avg_tokens": statistics.mean(with_skill_tokens) if with_skill_tokens else None,
        "baseline_avg_tokens": statistics.mean(baseline_tokens) if baseline_tokens else None,
        "with_skill_avg_duration_s": (statistics.mean(with_skill_durations) / 1000) if with_skill_durations else None,
        "baseline_avg_duration_s": (statistics.mean(baseline_durations) / 1000) if baseline_durations else None,
        "n_evals": len(with_skill_rates),
    }
    return benchmark


def render_html(benchmark, results_by_skill, output_path: Path):
    def pct(x):
        return f"{x*100:.0f}%" if x is not None else "—"

    def delta_cell(ws, bs):
        if ws is None or bs is None:
            return "—"
        d = ws - bs
        arrow = "▲" if d > 0 else ("▼" if d < 0 else "—")
        color = "#1a7f37" if d > 0 else ("#cf222e" if d < 0 else "#6e7781")
        return f'<span style="color:{color}">{arrow} {abs(d)*100:.0f}pp</span>'

    html_parts = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        "<title>PM Toolkit — Eval Report</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;max-width:1200px;margin:2em auto;padding:0 1em;color:#1f2328}",
        "h1{margin-bottom:0.2em}h2{margin-top:2em;border-bottom:1px solid #d1d9e0;padding-bottom:0.3em}",
        "h3{color:#0969da}",
        "table{border-collapse:collapse;width:100%;margin:0.5em 0 1em;font-size:0.95em}",
        "th,td{border:1px solid #d1d9e0;padding:6px 10px;text-align:left}",
        "th{background:#f6f8fa}",
        ".summary{background:#f6f8fa;padding:1em;border-radius:6px;margin:1em 0}",
        ".pass{color:#1a7f37}.fail{color:#cf222e}",
        ".eval-block{background:#f6f8fa;padding:0.8em 1em;border-radius:6px;margin:1em 0}",
        "details{margin:0.4em 0}details summary{cursor:pointer;font-weight:600}",
        "pre{background:#f6f8fa;padding:1em;border-radius:6px;overflow-x:auto;white-space:pre-wrap;font-size:0.85em;max-height:400px;overflow-y:auto}",
        ".badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:0.8em;margin-right:0.4em}",
        ".badge-pass{background:#dafbe1;color:#1a7f37}.badge-fail{background:#ffe3e3;color:#cf222e}",
        "</style></head><body>",
        "<h1>PM Toolkit — Eval Report — Iteration 1</h1>",
        "<p>Static report. 7 skills × 2 test prompts × 2 configs = 28 runs. Assertions are keyword-based programmatic checks (see scripts/grade_evals.py).</p>",
    ]

    # Overall summary
    ov = benchmark["overall"]
    html_parts.append("<div class='summary'>")
    html_parts.append("<h2 style='border:none;margin-top:0'>Overall</h2>")
    html_parts.append("<table>")
    html_parts.append("<tr><th>Metric</th><th>With skill</th><th>Baseline</th><th>Δ</th></tr>")
    html_parts.append(f"<tr><td>Mean pass rate</td><td>{pct(ov['with_skill_pass_rate'])}</td><td>{pct(ov['without_skill_pass_rate'])}</td><td>{delta_cell(ov['with_skill_pass_rate'], ov['without_skill_pass_rate'])}</td></tr>")
    if ov.get("with_skill_avg_tokens"):
        html_parts.append(f"<tr><td>Avg tokens/run</td><td>{ov['with_skill_avg_tokens']:.0f}</td><td>{ov['baseline_avg_tokens']:.0f}</td><td>+{(ov['with_skill_avg_tokens']-ov['baseline_avg_tokens'])/ov['baseline_avg_tokens']*100:.0f}%</td></tr>")
    if ov.get("with_skill_avg_duration_s"):
        html_parts.append(f"<tr><td>Avg duration</td><td>{ov['with_skill_avg_duration_s']:.1f}s</td><td>{ov['baseline_avg_duration_s']:.1f}s</td><td>+{(ov['with_skill_avg_duration_s']-ov['baseline_avg_duration_s'])/ov['baseline_avg_duration_s']*100:.0f}%</td></tr>")
    html_parts.append(f"<tr><td>N evals</td><td colspan='3'>{ov['n_evals']}</td></tr>")
    html_parts.append("</table>")
    html_parts.append("</div>")

    # Per-skill breakdown
    for skill_name, skill_entry in benchmark["skills"].items():
        html_parts.append(f"<h2>{escape(skill_name)}</h2>")
        s = skill_entry["summary"]
        html_parts.append(f"<p><b>Skill-level pass rate:</b> with skill {pct(s['with_skill_pass_rate'])} vs baseline {pct(s['without_skill_pass_rate'])} &nbsp; {delta_cell(s['with_skill_pass_rate'], s['without_skill_pass_rate'])}</p>")

        html_parts.append("<table>")
        html_parts.append("<tr><th>Eval</th><th>With skill</th><th>Baseline</th><th>Δ pass</th><th>Tokens (w/b)</th><th>Duration (w/b)</th></tr>")
        for e in skill_entry["evals"]:
            ws = e.get("with_skill", {})
            bs = e.get("without_skill", {})
            ws_rate = ws.get("pass_rate")
            bs_rate = bs.get("pass_rate")
            tok_line = f"{ws.get('tokens','—')} / {bs.get('tokens','—')}" if ws and bs else "—"
            dur_line = f"{ws.get('duration_ms','—')}ms / {bs.get('duration_ms','—')}ms" if ws and bs else "—"
            html_parts.append(f"<tr><td>{e['eval_id']} — {escape(e['eval_name'])}</td>")
            html_parts.append(f"<td>{pct(ws_rate)} ({ws.get('passed','—')}/{ws.get('total','—')})</td>")
            html_parts.append(f"<td>{pct(bs_rate)} ({bs.get('passed','—')}/{bs.get('total','—')})</td>")
            html_parts.append(f"<td>{delta_cell(ws_rate, bs_rate)}</td>")
            html_parts.append(f"<td>{tok_line}</td>")
            html_parts.append(f"<td>{dur_line}</td></tr>")
        html_parts.append("</table>")

        # Assertion-level detail per eval
        runs = results_by_skill.get(skill_name, [])
        by_eval = {}
        for r in runs:
            by_eval.setdefault(r["eval_name"], {})[r["config"]] = r
        for eval_name, configs in by_eval.items():
            html_parts.append(f"<div class='eval-block'>")
            html_parts.append(f"<h3>{escape(eval_name)}</h3>")
            html_parts.append("<table>")
            html_parts.append("<tr><th>Assertion</th><th>With skill</th><th>Baseline</th></tr>")
            ws = configs.get("with_skill", {}).get("grading", {}).get("expectations", [])
            bs = configs.get("without_skill", {}).get("grading", {}).get("expectations", [])
            for i, a in enumerate(ws):
                bsi = bs[i] if i < len(bs) else None
                ws_badge = "<span class='badge badge-pass'>PASS</span>" if a["passed"] else "<span class='badge badge-fail'>FAIL</span>"
                bs_badge = "<span class='badge badge-pass'>PASS</span>" if (bsi and bsi["passed"]) else "<span class='badge badge-fail'>FAIL</span>"
                html_parts.append(f"<tr><td>{escape(a['text'])}</td><td>{ws_badge}</td><td>{bs_badge}</td></tr>")
            html_parts.append("</table>")

            # Output excerpts
            for config in ["with_skill", "without_skill"]:
                r = configs.get(config)
                if r:
                    out_path = REPO / r["output_path"]
                    try:
                        content = out_path.read_text(encoding="utf-8", errors="replace")
                    except Exception:
                        content = "(could not read)"
                    html_parts.append(f"<details><summary>{config} output ({r['grading']['word_count']} words)</summary>")
                    html_parts.append(f"<pre>{escape(content)}</pre>")
                    html_parts.append("</details>")
            html_parts.append("</div>")

    html_parts.append("</body></html>")
    output_path.write_text("\n".join(html_parts))


def main():
    results = grade_all()
    benchmark = aggregate_benchmark(results)
    # Master benchmark file
    master_path = SKILLS_DIR.parent / "benchmark_all.json"
    master_path.write_text(json.dumps(benchmark, indent=2))
    # Viewer
    viewer_path = SKILLS_DIR.parent / "eval-report.html"
    render_html(benchmark, results, viewer_path)

    ov = benchmark["overall"]
    print(f"Graded {ov['n_evals']} evals")
    print(f"With-skill mean pass rate:    {ov['with_skill_pass_rate']*100:.1f}%")
    print(f"Baseline mean pass rate:      {ov['without_skill_pass_rate']*100:.1f}%")
    print(f"Delta:                        {(ov['with_skill_pass_rate']-ov['without_skill_pass_rate'])*100:+.1f}pp")
    print(f"Master benchmark: {master_path}")
    print(f"HTML viewer:      {viewer_path}")


if __name__ == "__main__":
    main()
