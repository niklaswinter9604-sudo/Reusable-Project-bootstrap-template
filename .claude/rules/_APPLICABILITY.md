# Rules Applicability Matrix

Which rule files apply to which agent. Read this when unsure whether a rule binds Codex or only Claude Code.

| File | Universal | Claude-Code-only | Notes |
|---|:---:|:---:|---|
| `context-economy.md` | ● (principles) | ● (`/compact`, `/memory`) | Codex maps intent to its own context tools |
| `knowledge-graph-graphify.md` | ● | — | graphify CLI works for both agents |
| `multi-agent-coordination.md` | ● | — | the one-agent-per-tree + Linear lock bind everyone |
| `linear-discipline.md` | ● | — | work-state SoT for all |
| `quality-gates.md` | ● | — | TDD + secrets gate bind everyone |
| `behavioral.md` | ● | — | scout-first, anti-hallucination, comment hygiene |
| `karpathy-guidelines.md` | ● | — | the 4 anti-mistake guidelines |
| `review-audit-self-decision.md` | ● | — | **most load-bearing for cross-agent consistency** |
| `learning-loop.md` | ● | — | promotion ritual is agent-agnostic |
| `domain-rules.md` (you create) | ● | — | your project's invariants |

## How to use

- **Claude Code** reads `CLAUDE.md` → which points here. Treat universal files as binding.
- **Codex** reads `AGENTS.md` → which imports `CLAUDE.md`. Apply the universal files; skip Claude-Code-only mechanics (slash commands, Task-tool subagents) and map the *intent* to your tool surface.
- **Human** uses this as the audit baseline when changing workflow conventions.

The split that matters: rules state **intent** (what must hold). Mechanics (which command achieves it) differ per agent. When a rule names a `/ck:*` command, Codex substitutes the equivalent in-session action.
