# Multi-Agent Coordination

For a team of 1 human + 2 AI agents (Claude Code + Codex). Keeps two agents from racing on the same work or the same checkout.

## Dual source-of-truth

| Concern | SoT | Who writes |
|---|---|---|
| Code state | GitHub (`main` + PRs) | via PRs only |
| Work state | Linear (`{{PREFIX}}-N` issues) | any agent (by claiming) |
| Shared context | `graphify-out/graph.json` | auto-rebuilt on commit |
| Rules | `CLAUDE.md` + `.claude/rules/` | human curates |

Joined by the issue identifier: the branch name contains `{{PREFIX}}-N`, so the PR auto-links to the issue. Never duplicate status across systems — Linear describes *what to do*, GitHub describes *what changed*.

## The locks

- **Linear is the work lock.** Before starting an issue: set it **In Progress** and assign yourself. Other agents see it and stay off that scope.
- **One agent per working tree (hard rule).** Only one agent edits/branch-switches in a given checkout at a time. A second concurrent agent uses a sibling worktree (`<repo>-<N>/`) or GitHub/Linear-side ops only. Two agents sharing `.git/HEAD` race: a concurrent `git switch` silently moves the other agent onto the wrong branch and strands its work.
- **No self-merge.** The human is the merge gate.

## Worktrees are disposable

- Default: branch-switch in place from the canonical checkout. Worktrees are the exception (concurrent shipping; a non-clean primary tree; destructive isolation).
- Naming: `<repo>-<N>/` where `<N>` is the issue number — never a name implying permanence.
- Cleanup is **mandatory and immediate** on PR merge: `git worktree remove --force …` + `git branch -D …` + `git worktree prune`.

## Token-tier routing

Spend the expensive model only where value-per-token is high.

| Stage | Primary | Rationale |
|---|---|---|
| Product framing / architecture / ADR / planning | **Frontier (Opus)** | decide-once, execute-many |
| Implementation / tests / docs / mechanics | **Mid-tier (Sonnet) / Codex** | volume work |
| Security/threat reasoning, retros | **Frontier** | reasoning density |
| Merge decision | **Human** | final authority |

Practical rule: human → frontier for the first ~15 min (frame + draft plan), then hand off. >70% context fill → save plan + switch.

## Claim discipline & file ownership

- Filter Linear by `agent:<self>` + status Todo/Backlog, ordered by priority; claim the top. If `agent:<self>` is empty, stop — do **not** poach another agent's labeled work.
- One agent per shared file per PR (`CLAUDE.md`, `AGENTS.md`, changelog, plan files). If you must touch a file open in another PR, coordinate first.

## Subagent context isolation (Claude Code)

When spawning subagents: pass a crafted prompt (task + specific file paths + acceptance criteria), **not** session history. Subagents report a status: `DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`. Never ignore BLOCKED/NEEDS_CONTEXT; never force the same approach after a BLOCK.
