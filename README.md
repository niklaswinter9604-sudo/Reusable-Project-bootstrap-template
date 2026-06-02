# Reusable Project Bootstrap Template

A starting skeleton for Python projects run by **1 human + 2 AI agents** (Claude Code + OpenAI Codex) under the **ClaudeKit Engineer 7-stage cadence**, coordinated via **Linear + GitHub + graphify**.

It exists to make a new project start *compliant* instead of drifting *into* compliance. Every rule here was distilled from running a real project on this stack — including the failure modes (a `CLAUDE.md` that grew into a 650-line token tax, a knowledge graph whose feedback loop never ran, hand-written session handoffs that rot).

## What you get

- **A lean `CLAUDE.md` skeleton** (≤300 lines, invariants only, `{{PLACEHOLDERS}}` for project specifics) — the file every agent reads every session, kept cheap.
- **Path-scoped rule files** in `.claude/rules/*.md` — the detailed "how", loaded on demand, not on every turn.
- **`AGENTS.md`** — the Codex mirror that imports `CLAUDE.md` and names only the Codex deltas.
- **`docs/` stubs** — operator standing orders, engineering-workflow reference, an empty changelog with a format header.
- **`scripts/setup-linear-labels.py`** — creates the canonical Linear label taxonomy idempotently.
- **`scripts/verify-clean-tree.py` + `scan-rules.toml`** — a genericized secrets/PII pre-commit scanner (exit `0/1/2`).
- **`NEW_PROJECT_CHECKLIST.md`** — the from-zero adoption runbook, one pass top to bottom.

## The split that keeps it lean

| Layer | Holds | Read frequency |
|---|---|---|
| `CLAUDE.md` | always-true **invariants** + pointers + project facts | every session, every agent |
| `.claude/rules/*.md` | **path-scoped how-to** (the detail) | on demand (by path / topic) |
| `docs/*.md` | **reference & narrative** (handbook, changelog, standing orders) | when a human/agent needs it |

The cardinal rule of this template: *if an instruction is "do X when editing Y", it belongs in a path-scoped rule, never in `CLAUDE.md`.* That single discipline is what stops the entry doc from becoming a wiki.

## The rules (index)

| File | Group | What it enforces |
|---|---|---|
| `.claude/rules/context-economy.md` | Context / token economy | ≤300-line CLAUDE.md, query-don't-grep, delegate big reads, compaction survival, agent hand-off at 70% fill |
| `.claude/rules/knowledge-graph-graphify.md` | Knowledge graph | query-first, `path` impact pre-flight, `save-result` feedback loop, wiki navigation, `update .` after edits |
| `.claude/rules/multi-agent-coordination.md` | Coordination | dual source-of-truth, one-agent-per-tree, branch-per-issue, no self-merge, token-tier routing |
| `.claude/rules/linear-discipline.md` | Linear | issue-before-work, label taxonomy, gitBranchName auto-link, cycles, work-state vs code-state |
| `.claude/rules/quality-gates.md` | Quality | TDD + prove-it-can-fail, coverage ratchet, pre-commit secrets gate, no green-by-mocking |
| `.claude/rules/behavioral.md` | Behavioral | scout-first/ask-second, anti-hallucination, comments explain *why* not *origin* |
| `.claude/rules/karpathy-guidelines.md` | Behavioral | think-before-coding · simplicity-first · surgical-changes · goal-driven |
| `.claude/rules/review-audit-self-decision.md` | Behavioral | verified-decisions-are-sticky, audit-is-input-not-orders, never silently reverse a user decision |
| `.claude/rules/learning-loop.md` | Learning | how a noticed learning becomes an enforced rule |
| `.claude/rules/_APPLICABILITY.md` | meta | which rules are universal vs Claude-Code-only vs human-only |

## Adopt in ~15 minutes

```bash
git clone <this-template> my-new-project && cd my-new-project
rm -rf .git && git init        # start fresh history
```

Then follow `NEW_PROJECT_CHECKLIST.md` top to bottom (set the `{{PLACEHOLDERS}}`, run the Linear-label script, install graphify, wire the secrets gate).

## What this is NOT (deliberate omissions)

Adopt a tool only when you can name the *recurring failure it prevents*. This template deliberately ships **without**:

- Heavy multi-agent **swarm frameworks** — at 1 human + 2 agents, the Linear lock + one-agent-per-tree rule already serializes work safely. Add agent-team mode only at 5+ concurrent agents.
- **Cloud GUI multiplexers / dashboard servers** — they add a data-residency and maintenance surface; Linear's board + `/context` cover the solo/duo case.
- **MCP servers you don't call every turn** — each always-loaded tool permanently costs context. Keep Tool Search on; force-load nothing.
- **Heavy graph backends (Neo4j/Graphiti)** — graphify's local JSON is zero-infra and the default.

> The test for adoption: *can you name the recurring failure it prevents?* If not, leave it out — every adopted tool is permanent context plus permanent maintenance.

## Stack assumptions (and how to swap them)

Python 3.12 / `uv` / `pytest`. To use a different language, keep the rule files (they are language-agnostic) and replace `pyproject.toml`/`verify-clean-tree.py` specifics. The coordination, Linear, graphify, and behavioral rules transfer unchanged.

## Phase 2 (not shipped here, add on demand)

Documented in `NEW_PROJECT_CHECKLIST.md`: git hooks (`pre-commit`/`post-commit` → ruff/mypy/pytest/secrets-gate + graphify rebuild), CI with `--cov-fail-under`, `.pre-commit-config.yaml`, plan/phase-file templates. Add these when the project first *feels* the pain they prevent.
