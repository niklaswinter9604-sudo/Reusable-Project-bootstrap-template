# AGENTS.md — {{PROJECT_NAME}} (Codex entry)

@CLAUDE.md

The line above imports the full Claude Code instruction set. Codex follows the **same** invariants, cadence, Linear discipline, and behavioral rules. This file records only the **Codex-specific deltas**.

## Codex deltas

- **No `/ck:*` or `/git:*` slash commands.** Map the *intent* of each stage to your own tool surface — Plan → Cook → Test → Review → Docs → Commit → PR executed in-session.
- **No Task-tool subagents.** Where the Claude flow fans out subagents, do the work sequentially in-session or hand off via a Linear comment / a `plans/*/plan.md` file (the durable cross-agent artifact).
- **Trust list:** ensure `{{CANONICAL_CHECKOUT_PATH}}` is in `~/.codex/config.toml`. Work only in that checkout (the one-agent-per-tree rule applies to you too).
- **Applicability:** the universal rule files in `.claude/rules/` apply to you. Skip the Claude-Code-only ones (skill-routing trees, subagent orchestration) — see `.claude/rules/_APPLICABILITY.md`.

## Shared sources of truth

| Concern | Source of truth |
|---|---|
| Code state | GitHub (`main` + PRs) |
| Work state | Linear (`{{PREFIX}}-N` issues) |
| Shared context | `graphify-out/graph.json` (auto-rebuilt on commit) |
| Rules | `CLAUDE.md` + `.claude/rules/*` (human curates) |

Keep `CLAUDE.md` and this file in sync on workflow; LEXIS-canon-style content lives in `CLAUDE.md` and is *referenced*, not duplicated here.
