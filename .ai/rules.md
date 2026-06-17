# Instructions

This repository is a reusable operating system for product and engineering work across multiple projects and contexts.

## Briefing

You are working inside **Umberto**, a Lean Double Diamond skill repo for discovery, definition, prototyping, implementation, and learning.

The active project is defined in `.ai/memory/active-context.md`.
The product definition lives in `.ai/app.md`.

## Environment

- Primary mode: Claude Code skill repo
- Secondary compatibility: GitHub Copilot-style agent docs in `.github/agents/`
- Dependency philosophy: zero-dependency by default; add tooling only when it materially improves leverage
- Memory system: file-based durable memory under `.ai/memory/`
- Delivery style: lean startup loop inside the Double Diamond
- Validation style: smallest meaningful verification first, then broader checks as risk increases

## Required reading before meaningful work

1. `.ai/changelog.md`
2. `.ai/app.md`
3. `.ai/memory/active-context.md`
4. active project memory under `.ai/memory/projects/<slug>/`

## Rules

You must always follow these rules:

- Start by identifying the current phase: Discover, Define, Develop, or Deliver.
- Do not jump to implementation if the problem, user, or success criteria are still unclear.
- Name assumptions explicitly. If an assumption is material, turn it into an experiment, question, or validation step.
- Prefer the smallest reversible move that can produce evidence.
- Keep raw evidence and durable decisions in memory; do not rely on transient chat context.
- When writing code, use test-first or verification-first thinking appropriate to the task risk.
- Run the narrowest useful validation after each meaningful change.
- Do not introduce speculative abstractions, configuration, or platform work without a second real use case.
- When touching user-facing UX, follow `.ai/design.md` and use clear recovery-oriented error copy.
- When a task is completed, update `.ai/tasks.md` and `.ai/changelog.md`.
- When a durable product, architecture, or process decision is made, update project memory.
- Keep changes small, intentional, and easy to review.
- Prefer explaining tradeoffs over pretending there is one obvious answer.
- Use Lean mode by default; use Caveman mode only when requested or clearly beneficial.
