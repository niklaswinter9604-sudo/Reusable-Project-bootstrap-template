# Engineering Workflow — {{PROJECT_NAME}}

The reference handbook for the 7-stage cadence. `CLAUDE.md §4/§5` are the one-liners that point here.

## The cadence

**Plan → Cook → Test → Review → Docs → Commit → PR.**

| Stage | Claude Code | Codex | Purpose |
|---|---|---|---|
| Plan | `/ck:plan` | in-session planning | frame the work, write a plan file, identify phases |
| Cook | `/ck:cook <plan>` | implement in-session | implement with TDD discipline |
| Test | `/ck:test` | run suite | run + analyze; fix failures, don't bypass |
| Review | `/ck:review` | self-review / Codex review | adversarial pre-PR pass |
| Docs | `/ck:docs:update` | edit docs | sync changelog + affected docs |
| Commit | `/git:cm` | `git commit` | conventional, no AI attribution |
| PR | `/git:pr` | `gh pr create` | open PR; **human merges** |

Routing by intent: new feature → start at Plan. Bug/CI failure → `/ck:fix` (auto-scouts) or scout → debug → fix. "How does X work" → scout/graphify → debug.

## Token-tier matrix

| Stage | Primary | Rationale |
|---|---|---|
| Framing / architecture / ADR / planning | Frontier (Opus) | decide-once, execute-many |
| Implementation / tests / docs / mechanics | Mid-tier (Sonnet) / Codex | volume |
| Security/threat reasoning, retros | Frontier | reasoning density |
| Merge | Human | final authority |

Practical rule: human → frontier for the first ~15 min (frame + plan), then hand off. At >70% context fill, save a plan file and switch.

## Subagent vs main conversation (Claude Code)

Use a subagent when the work is a self-contained fan-out (broad search, parallel review/test, research) and you only need the conclusion. Pass a crafted prompt (task + file paths + acceptance criteria), not session history. Subagents report `DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT`.

## Plans

Anything spanning more than a single commit gets a `plans/YYMMDD-HHMM-<slug>/plan.md` (overview, ≤80 lines) + `phase-XX-*.md` files. Reference the plan in commits and the Linear issue so work is resumable by another agent.
