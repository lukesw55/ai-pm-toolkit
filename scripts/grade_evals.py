#!/usr/bin/env python3
"""
grade_evals.py — Grade eval runs across PM and data-analysis skills.

Walks skills/<skill>/workspace/iteration-1/ (canonical only — mirrors never
carry workspace/) and produces:
- grading.json per run (with_skill + without_skill)
- benchmark.json per skill
- aggregated benchmark_all.json
- eval-report.html (static viewer)
"""

import json
import re
import statistics
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"

# Assertions per (skill, eval_name) — each is (label, callable taking normalised text → bool)
def has(p: str):
    return lambda t: p.lower() in t

def hasr(pattern: str):
    rx = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    return lambda t: bool(rx.search(t))

def not_has(p: str):
    return lambda t: p.lower() not in t

def hedged(forbidden: str, near: list[str] | None = None, window: int = 160):
    """True unless `forbidden` appears with no hedge/negation/quote marker
    nearby. Plain `not_has()` false-fails a "does not assert X as fact"
    assertion whenever the model legitimately quotes X to reject or hedge
    it (e.g. "you asked me to write 'X' but I can't confirm that"). This
    only flags `forbidden` as an unguarded assertion when none of `near`
    appears within `window` characters on either side."""
    near = near or [
        "not", "don't", "won't", "can't", "cannot", "unverified", "unconfirmed",
        "hedge", "quote", "asked", "requested", "instead", "haven't", "unable",
        "refus", "declin", "without confirm",
    ]
    forbidden_l = forbidden.lower()

    def check(t: str) -> bool:
        start_at = 0
        while True:
            idx = t.find(forbidden_l, start_at)
            if idx == -1:
                return True
            start = max(0, idx - window)
            end = min(len(t), idx + len(forbidden_l) + window)
            ctx = t[start:end]
            if not any(n in ctx for n in near):
                return False
            start_at = idx + len(forbidden_l)

    return check


def all_named_scores_at_least(dimensions: list[str], minimum: int):
    """Require every named rubric dimension to carry an explicit score at
    or above the threshold. A single high score must not satisfy a claim that
    the response scored strongly across all dimensions."""
    patterns = []
    for name in dimensions:
        flexible_name = r"\s+".join(re.escape(part) for part in name.split())
        patterns.append(re.compile(
            rf"{flexible_name}[\s\S]{{0,80}}?([1-5])\s*/\s*5",
            re.IGNORECASE,
        ))

    def check(t: str) -> bool:
        scores = [pattern.search(t) for pattern in patterns]
        return all(match and int(match.group(1)) >= minimum for match in scores)

    return check

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
        "resist-solution-first-dashboard-premise": [
            ("Names the framing as solution-first / already decided", hasr(r"solution.first|already (?:decided|settled)|premise|treats?.*as decided")),
            ("Flags the evidence as thin / anecdotal / non-representative", hasr(r"thin|anecdotal|non.representative|weak evidence|one (?:competitor )?demo|not (?:a )?validated|single data point")),
            ("Asks what underlying problem the dashboard should solve", hasr(r"underlying problem|what problem|real problem|problem.*(?:dashboard|it).*(?:solve|meant to solve)")),
            ("Proposes discovery research on the problem before the solution", hasr(r"discovery|research (?:plan|question)|before (?:committing|building|development)")),
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
        "challenge-weak-prioritisation-rationale": [
            ("Pushes back on reverse-engineering the rationale to fit a predetermined order", hasr(r"predetermined|already decided|reverse.engineer|fit (?:a|the) (?:decision|order)|justify (?:a|the) (?:decision|order) already made")),
            ("Flags the SLA item as sized for a single renewal, not broad impact", hasr(r"single renewal|one renewal|sla.*(?:single|one|narrow)|one customer")),
            ("Flags the mobile redesign as engineering-driven with no user/business evidence", hasr(r"engineering.driven|no (?:user|business) (?:impact )?evidence|engineering.*ask(?:ing)?|modernize the stack")),
            ("Flags the billing item's vague 'sometimes' evidence", hasr(r"sometimes|vague|unquantified|not quantified")),
            ("Recommends scoring on actual merits rather than the given order", hasr(r"actual merits|score (?:the initiatives )?(?:on|honestly)|different order|may produce a different")),
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
        "challenge-unjustified-scope-expansion": [
            ("Challenges the scope expansion beyond the evidenced ask", hasr(r"scope expansion|scope creep|beyond (?:the )?evidence|expand(?:ing)? scope")),
            ("Names 'table stakes / eventually anyway' as an unjustified rationale", hasr(r"table stakes|eventually anyway|unjustified|not (?:a )?(?:justif|evidenc)")),
            ("Recommends scoping the PRD to CSV import", hasr(r"csv import|scope (?:the )?(?:prd )?to csv|bulk (?:user )?import")),
            ("Treats SCIM, field mapping, HR sync, audit log as non-goals or separately evidenced asks", hasr(r"non.goal|separately evidenc|out of scope|defer")),
            ("Cites the 14 tickets / signed commit as the actual evidence base", hasr(r"14 tickets|signed commit|14 support tickets")),
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
        "challenge-vanity-metric-victory-lap": [
            ("Challenges page views / social engagement as vanity metrics", hasr(r"vanity metric|page views?.*(?:not|isn't|aren't)|input metric|not the (?:actual )?outcome")),
            ("Names activation or retention as the metric that actually matters", hasr(r"activation|retention")),
            ("Flags the concurrent paid acquisition campaign as a confound", hasr(r"confound|concurrent.*campaign|paid (?:acquisition )?campaign")),
            ("Declines to write an unqualified success memo / immediate 100% rollout", hasr(r"(?:can't|cannot|won't|decline|not (?:yet|ready)) (?:declare|write|recommend)|before (?:declaring|recommending)|need(?:s)? (?:the )?activation")),
        ],
        "solid-ab-rationale-agree": [
            ("Recommends the rollout", hasr(r"recommend.*rollout|full rollout|roll out|recommend(?:ing)? (?:a )?(?:full|100%)")),
            ("Acknowledges the rigor of the evidence (SRM, sample size, significance)", hasr(r"srm|sample.ratio|p ?< ?0\.001|significant|adequate sample|42,?000")),
            ("Does not manufacture unwarranted hedges or caveats", lambda t: not re.search(r"however,? (?:we|i) (?:recommend|suggest|would) (?:wait|hold|delay|gather more|collect more|run (?:it )?(?:for )?(?:longer|another)|extend the test)", t)),
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
    "pm-transversal-comms": {
        "exec-decision-email-launch-slip": [
            ("Subject line names the action needed", hasr(r"subject:.*(decision|go/no-go|go.no.go|needed|approve)")),
            ("States a clear recommendation (option A)", hasr(r"recommend|option a\b.*(recommend|prefer)|go with a")),
            ("Both options given with a trade-off each", lambda t: ("option a" in t) and ("option b" in t)),
            ("Specific ask with the Wednesday date", hasr(r"wednesday")),
            ("Stays close to the ~300-word default (allows headroom)", lambda t: len(t.split()) < 420),
        ],
        "slack-bluf-status-update": [
            ("States the status + pending blocker up front", hasr(r"2 of 3|two of three|third bug|blocking bug")),
            ("Names the payment-webhook race condition and its ETA", hasr(r"payment.webhook|race condition|eta|tomorrow")),
            ("Names Thursday GA date's dependency on the fix", hasr(r"thursday.*(depend|contingent|assuming|if the fix|pending)|depend.*thursday")),
            ("Stays concise — BLUF, not a wall of text", lambda t: len(t.split()) < 150),
        ],
        "channel-fit-pricing-negotiation-sprawl": [
            ("Recommends moving the decision into a written record", hasr(r"doc|memo|daci|written record")),
            ("Names the 3-exchange rule or equivalent reasoning against chat sprawl", hasr(r"3.exchange|three exchange|3 back.and.forth|exchange rule|sprawl")),
            ("Points to the DACI/stakeholder escalation path", hasr(r"pm-transversal-stakeholder|daci")),
            ("Concrete step: summarise what's surfaced rather than restarting", hasr(r"summaris|summariz")),
            ("Posts the resulting doc link back to the original thread", hasr(r"post.*(link|thread)|link back|share.*(doc|link).*(thread|channel)|back (?:in|to) the (?:thread|channel)")),
        ],
        "deescalate-unverified-outage-blame-message": [
            ("Does not assert the causal claim as settled fact without hedge/quote context", hedged("your deploy last night broke our checkout flow")),
            ("Names the claim/figure as unconfirmed rather than settled", hasr(r"unconfirmed|haven't confirmed|not confirmed|unverified|don't (?:yet )?know if|not sure (?:it was|whether)")),
            ("Proposes a de-escalated version or asks to confirm before sending", hasr(r"instead|propose|de-escalat|toned.down|softer|check (?:whether|if)|confirm")),
            ("Still conveys real urgency rather than dropping it", hasr(r"urgent|now|immediate|asap|priority")),
        ],
        "solid-status-update-no-fabricated-objection": [
            ("Delivers the clean status (on track, GA Thursday)", hasr(r"on track|thursday")),
            ("States no ask / no blockers as given", hasr(r"no ask|no blocker")),
            ("Does not manufacture caveats or hedges the input didn't warrant", lambda t: not re.search(r"just to be safe|hold off|double.check everything|however,? (?:we|i) (?:recommend|suggest|would|should)", t)),
        ],
    },
    "pm-product-sense": {
        "build-onboarding-improvement": [
            ("Asks a clarifying question or states an explicit scoping assumption", hasr(r"clarify|clarifying question|assum(?:e|ing|ption)|scope")),
            ("States a strategy/goal the decision serves", hasr(r"goal|strategy|objective|north star")),
            ("Enumerates more than one user type before choosing one", hasr(r"user type|persona|segment")),
            ("Ranks pain points by severity rather than a flat list", hasr(r"pain point|most severe|ranked|priorit")),
            ("Proposes a solution and explicitly rejects at least one alternative", hasr(r"reject|ruled out|considered and (?:reject|rule)|instead of|rather than")),
            ("Cuts to an MVP with explicit scope and a success metric", hasr(r"mvp|in scope|out of scope|non.goal|success metric|measure success")),
        ],
        "evaluate-pet-feature": [
            ("Scores user empathy low — no specific evidenced user/pain named", hasr(r"user empathy.*(?:1|2)\s*/\s*5|(?:1|2)\s*/\s*5.*user empathy")),
            ("Scores product taste low — no MVP cut, unscoped feature bundle", hasr(r"product taste.*(?:1|2)\s*/\s*5|(?:1|2)\s*/\s*5.*product taste")),
            ("Reports the lowest score first rather than leading with a strength", hasr(r"lowest.scoring|lowest score|weakest dimension")),
            ("Verdict is sharpen or back-to-discovery, not proceed", hasr(r"sharpen|back.to.discovery")),
            ("Does not simply endorse the pitch as a clean proceed", lambda t: not re.search(r"verdict:?\s*proceed", t)),
        ],
        "evaluate-solid-control": [
            ("Scores strongly across dimensions given the evidence", all_named_scores_at_least([
                "user empathy", "structured thinking", "product taste",
                "strategic awareness", "communication",
            ], 4)),
            ("Verdict is proceed", hasr(r"verdict:?\s*proceed|proceed\b")),
            ("Does not manufacture a fabricated gap or unwarranted caveat", lambda t: not re.search(r"however,? (?:we|i) (?:recommend|suggest|would|should) (?:sharpen|revisit|reconsider|hold off|go back)", t)),
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
    "data-science-analyst": {
        "audit-powerbi-export-data-quality": [
            ("Says not to trust/ship the metric yet", hasr(r"no|não|do not|don't|hold|not ship|não confiar")),
            ("Flags stage normalization", hasr(r"stage|closed won|cw|normaliz|map|allowlist")),
            ("Flags amount parsing", hasr(r"amount|usd|strip|comma|numeric|parse")),
            ("Flags mixed date parsing", hasr(r"created_date|date|to_datetime|coerce|null")),
            ("Clarifies cohort definition", hasr(r"cohort|definition|first deal|signup|quarter")),
            ("Recommends profiling / validation before analysis", hasr(r"profile_dataset|profile|clean|validat|audit")),
        ],
        "validate-ab-test-significance": [
            ("Computes or states ~1.2pp lift", hasr(r"1\.2|1,2|percentage point|pp")),
            ("Finds not statistically significant", hasr(r"not significant|não significativo|p.?value|p\s*[≈=]|0\.1[5-9]|0,1[5-9]")),
            ("Mentions confidence interval crossing zero", hasr(r"confidence interval|ci|interval|cross|straddl|zero")),
            ("Mentions underpowered / more sample needed", hasr(r"power|underpower|sample|22k|n\s*≈")),
            ("Requires SRM check", hasr(r"srm|sample ratio mismatch|chi.?square")),
            ("Requires guardrails / retention checks", hasr(r"guardrail|retention|day.?7|day.?14")),
        ],
        "cohort-retention-sql-audit": [
            ("Finds missing denominator / cohort size", hasr(r"denominator|cohort size|cohort_size|retention rate")),
            ("Flags week-offset / week-0 issue", hasr(r"week.?0|week offset|off.?by.?one|activation week")),
            ("Mentions weekday-of-activation bias", hasr(r"weekday|monday|sunday|partial week|bias")),
            ("Requires post-activation event filter", hasr(r"event_date.*cohort_date|post.?activation|after activation")),
            ("Recommends rewrite / validation", hasr(r"rewrite|fix|validat|not ship|fails?")),
        ],
        "leakage-check-baseline-ml-churn-model": [
            ("Treats AUC 0.94 as leakage signal", hasr(r"leakage|too good|0\.94|strong signal")),
            ("Flags temporal leakage", hasr(r"temporal|as.?of|snapshot|future")),
            ("Questions last-login/support-window features", hasr(r"last.?login|support.?ticket|90.?day")),
            ("Rejects random split; recommends time split", hasr(r"random|80/20|time.?based|q1|q4")),
            ("Requires target definition", hasr(r"target definition|churned|cancellation|no.?activity|mrr")),
            ("Recommends baseline comparison/rebuild", hasr(r"logistic|baseline|rebuild|re.?evaluat")),
        ],
    },
    "anti-slop": {
        "remove-ai-slop-from-readme-section": [
            ("Rewrite drops marketing hype", lambda t: not re.search(r"empowers|seamless|game.?chang|revolutioniz", t)),
            ("Rewrite drops filler openers", lambda t: not re.search(r"in today's|it is crucial", t)),
            ("Keeps the concrete function of the thing described", hasr(r"toolkit|skill|team|does|provides")),
            ("Names what was cut and why", hasr(r"removed|cut|dropped|slop|hype|because")),
        ],
        "block-unrequested-plan-file": [
            ("Flags PLAN.md/SUMMARY.md as forbidden artefacts", hasr(r"plan\.md|summary\.md")),
            ("Recommends deleting the unrequested files", hasr(r"delete|remove|rm |drop")),
            ("References the anti-slop rule or gate", hasr(r"anti.?slop|forbidden|unrequested|gate")),
            ("Does not endorse keeping them", lambda t: not re.search(r"keep (?:the )?(?:plan|summary)", t)),
        ],
    },
    "humanize-deliverables": {
        "gate-before-slack-send": [
            ("Names the humanizer pass as prerequisite", hasr(r"humaniz")),
            ("Mentions the sha256 sentinel / mark script", hasr(r"sha256|sentinel|humanize-mark|mark")),
            ("Says the gate blocks the send otherwise", hasr(r"block|gate|refus")),
            ("Produces an actual Slack draft", hasr(r"draft|slack")),
        ],
    },
    "humanizer": {
        "humanize-exec-memo": [
            ("Rewrite avoids 'fast-paced landscape'", not_has("fast-paced")),
            ("Rewrite avoids 'leverage'", not_has("leverage")),
            ("Rewrite avoids 'crucial'", not_has("crucial")),
            ("Keeps the memo's substance", hasr(r"memo|we |our |team")),
        ],
        "preserve-technical-meaning": [
            ("Retains numbers/dates", hasr(r"\d")),
            ("States technical content preserved", hasr(r"preserv|unchanged|intact|same|não alter")),
            ("Actually rewrites the prose", hasr(r"rewrit|humaniz|revis|adjust")),
        ],
    },
    "inference-discipline": {
        "ambiguous-flow-approval": [
            ("Does not edit before clarifying", hasr(r"before edit|don't edit|não edit|ask|clarif|approv")),
            ("Names the onboarding flow candidate", has("onboarding")),
            ("Names the checkout flow candidate", has("checkout")),
            ("Tags the interpretation as inference needing OK", hasr(r"\[infer|inference|assumption|needs ok|approval")),
        ],
        "memory-not-proof": [
            ("Treats memory as prior, not proof", hasr(r"not proof|prior|reverif|re-?verif|stale")),
            ("Requires verification before the outbound message", hasr(r"verif|check|confirm|source")),
            ("Marks the launch date unverified until checked", hasr(r"\[unverified|\[from memory|unverified|tbd")),
        ],
        "hold-unverified-claim-under-pressure": [
            ("Does not assert the claim as settled fact without hedge/quote/rejection context", hedged("data residency is supported on the eu cluster today")),
            ("Names that confidence/urgency/responsibility-offer is not verification", hasr(r"not (?:the )?same as verif|confidence (?:is )?not|urgency (?:is )?not|isn't verification|not verification")),
            ("Proposes a hedged version or requires engineering confirmation before sending", hasr(r"hedge|unresolved|unverified|confirm(?:ation)? (?:from|with) engineering|two.minute|2.minute")),
            ("Holds the position despite the pressure pushback", hasr(r"still|even though|despite|hold(?:s|ing)? (?:this|the) position|not send(?:ing)? (?:it )?(?:as|unverified)")),
        ],
    },
    "pm-storytelling": {
        "turn-synthesis-into-narrative-spine": [
            ("Builds a narrative spine (tension/insight/change)", hasr(r"tension|insight|change|takeaway")),
            ("Marks evidence gaps instead of inventing", hasr(r"needs source|\[needs|gap|no evidence|não invent")),
            ("Produces a decision-memo shape", hasr(r"memo|decision|recommend")),
            ("Anchors claims in the source notes", hasr(r"quote|evidence|note")),
        ],
    },
    "repo-doctor": {
        "validate-skill-repo-health": [
            ("Checks skill frontmatter", hasr(r"frontmatter|description")),
            ("Checks hooks/settings wiring", hasr(r"hook|settings")),
            ("Checks the memory contract", hasr(r"memory")),
            ("Cites concrete paths in findings", hasr(r"\.md|\.sh|\.py")),
            ("Stays read-only (suggests, does not apply)", hasr(r"read.?only|suggest|do not apply|não aplica")),
        ],
    },
    "pm-prioritization-regua-comum": {
        "score-backlog-with-regua-comum": [
            ("Scores ARR dimension", hasr(r"arr")),
            ("Scores Abrangência dimension", hasr(r"abrang")),
            ("Scores CRA/strategic dimension", hasr(r"cra|strateg")),
            ("Applies confidence weighting", hasr(r"confian|confidence")),
            ("Flags the single-account ask against the Abrangência lock", hasr(r"customiz|single account|uma conta|lock")),
            ("Rates effort and plots the matrix", hasr(r"effort|esforço")),
            ("Recommends an order of execution", hasr(r"first|primeiro|order|priorit")),
        ],
    },
}


def grade_run(output_path: Path, skill: str, eval_name: str):
    if not output_path.exists():
        return None
    text = output_path.read_text(encoding="utf-8", errors="replace").lower()
    checks = ASSERTIONS.get(skill, {}).get(eval_name, [])
    if not checks:
        # 0/0 would read as a silent pass in the report; make the gap loud.
        print(f"WARN: no assertions for ({skill}, {eval_name}) — run graded as empty", file=sys.stderr)
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
        # Any skill with recorded runs is gradable — the old pm-* prefix
        # filter silently skipped anti-slop, humanizer, and friends.
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
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
        f"<p>Static report. {len(benchmark['skills'])} skill(s), {benchmark['overall'].get('n_evals') or 0} eval(s) × 2 configs "
        "(with_skill / baseline). Assertions are keyword-based programmatic checks (see scripts/grade_evals.py).</p>",
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
    master_path = REPO / "benchmark_all.json"
    master_path.write_text(json.dumps(benchmark, indent=2))
    # Viewer
    viewer_path = REPO / "eval-report.html"
    render_html(benchmark, results, viewer_path)

    ov = benchmark["overall"]
    if not ov.get("n_evals"):
        # No skills/*/workspace/iteration-1 runs found — pass_rate fields are
        # all None, so the summary below would crash on `None * 100`.
        print("Graded 0 evals — no skill workspace runs found.", file=sys.stderr)
        print(f"Master benchmark: {master_path}")
        print(f"HTML viewer:      {viewer_path}")
        return
    print(f"Graded {ov['n_evals']} evals")
    print(f"With-skill mean pass rate:    {ov['with_skill_pass_rate']*100:.1f}%")
    print(f"Baseline mean pass rate:      {ov['without_skill_pass_rate']*100:.1f}%")
    print(f"Delta:                        {(ov['with_skill_pass_rate']-ov['without_skill_pass_rate'])*100:+.1f}pp")
    print(f"Master benchmark: {master_path}")
    print(f"HTML viewer:      {viewer_path}")


if __name__ == "__main__":
    main()
