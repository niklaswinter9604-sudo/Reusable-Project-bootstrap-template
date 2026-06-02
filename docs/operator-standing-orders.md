# Standing Operator Orders — {{PROJECT_NAME}}

Permanent operating instructions for agent sessions. **Read this before any other action.** Where this conflicts with the project brief, the brief wins.

## Framework

This repo runs the **ClaudeKit Engineer** 7-stage cadence: **Plan → Cook → Test → Review → Docs → Commit → PR**. Detail in `docs/engineering-workflow.md`; one-liners in `CLAUDE.md §4`.

## Hard guardrails (never break)

1. No secrets/PII in git — `scripts/verify-clean-tree.py` is the pre-commit gate.
2. Every actionable item is a `{{PREFIX}}-N` Linear issue before work starts.
3. One agent per working tree; one issue → one branch → one PR.
4. Don't merge your own PR — the human is the merge gate.
5. Conventional commits, no AI attribution.
6. TDD for logic; never green a test by mocking/ignoring.
7. Never fabricate — cite a source or say "uncertain".

## Self-Learning Loop

The canonical text lives in `.claude/rules/learning-loop.md`. Summary: capture (transient) → triage at cycle-end via retro → promote by type (arch→ADR, workflow→this file, behavioral→`.claude/rules/`) → human merges → enforced at next session start. A learning is "done" only when it's in a session-start file.

## When in doubt

- Conflict between this doc, `CLAUDE.md`, and the brief → **brief wins**.
- Ambiguous instruction → ask via `AskUserQuestion` before acting.
- Test failure → debug + root-cause, never bypass.
- Pre-commit gate rejection → fix the content, not the gate.

## Operator (human) authority

- Owns the merge gate and Linear label rebalancing.
- Reassigns `agent:*` labels to route work between agents.
- Approves any reversal of a previously-confirmed decision (see `.claude/rules/review-audit-self-decision.md`).
