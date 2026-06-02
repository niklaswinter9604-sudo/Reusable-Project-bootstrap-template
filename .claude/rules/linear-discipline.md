# Linear Discipline

Linear is the **work-state** source of truth (GitHub is code-state). This is the discipline that keeps both agents and the human seeing the same picture.

## The Linear-canonical invariant

Every actionable item — from a 10-line fix to a multi-phase milestone — is a `{{PREFIX}}-N` issue **before work starts**. No exceptions worth more than 30 seconds:

- Plans (`plans/*/plan.md`) get a tracking issue (`stage:plan`). The plan file is the *how*; the issue tracks *status*.
- Code/commit TODOs reference an issue: `# TODO({{PREFIX}}-N): …`. A bare `# TODO` is forbidden — file the issue first.
- Cross-session work gets an issue before the session ends. Chat-only commitments rot.
- Narrow exceptions: a trivial fix inside an already-claimed issue, or scratch exploration that produces no commit/PR. If exploration produces a commit, file the issue retroactively in the same PR.

The check before continuing any work: *can you point to the `{{PREFIX}}-N`?* If not, file it.

## Branch & status automation

- Use the issue's auto-generated `gitBranchName` (contains the identifier) so the PR auto-links.
- Wire workflow automation once (Linear Team Settings → Workflows): push → **In Progress**, PR opened → **In Review**, PR merged → **Done**. The setup script cannot do this; it's a manual one-time step.

## Label taxonomy

Mandatory grouped labels on every issue:

| Group | Values | Use |
|---|---|---|
| `agent` | `agent:opus`, `agent:sonnet`, `agent:codex`, `agent:human` | who claims it |
| `stage` | `stage:plan`, `:implement`, `:test`, `:review`, `:docs`, `:ship`, `:retro` | cadence position |
| `area` | project-specific (e.g. `area:api`, `:db`, `:cli`, `:infra`, `:docs`) | path scope |
| priority | built-in Urgent/High/Medium/Low | sort key |

Optional, **flat (ungrouped)** so several can co-occur: `flag:blocker`, `flag:research-needed`, `flag:sensitive`.

Create them with `scripts/setup-linear-labels.py` (idempotent).

## Cycles & milestones

- 1-week cycles, ISO-named (`2026-W23`), auto-rollover. The cycle is the smallest planning unit; each ends with a retro.
- Project milestones mirror GitHub milestones 1:1 by name.

## Claim discipline

Filter `agent:<self>` + status Todo/Backlog, priority-ordered; claim the top, set In Progress, assign self. If `agent:<self>` is empty, stop — don't poach. The human rebalances labels.
