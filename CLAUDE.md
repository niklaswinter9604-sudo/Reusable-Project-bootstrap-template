<!-- maintainer note: keep this file under 300 lines. Anything multi-step or path-specific → .claude/rules/. Anything narrative → docs/. This file is read every session by every agent; treat its length as a token tax. -->

# CLAUDE.md — {{PROJECT_NAME}}

Entry instructions for Claude Code. Invariants and pointers only. Detail lives in `.claude/rules/` (path-scoped) and `docs/` (reference). Where this file conflicts with a project brief, **the brief wins**.

## §0 Project facts

- **Project:** {{PROJECT_NAME}} — {{ONE_LINE_MISSION}}
- **Canonical checkout:** {{CANONICAL_CHECKOUT_PATH}} (always work here; `cd` here before any git op)
- **Linear:** team prefix `{{PREFIX}}` · project `{{LINEAR_PROJECT_ID}}`
- **GitHub:** `{{GITHUB_REPO}}` · default branch `main`
- **Stack:** Python 3.12 / uv / pytest (swap in `pyproject.toml` + `scripts/verify-clean-tree.py` if different)

## §1 Non-negotiable invariants

1. **Issue before work.** Every actionable item is a `{{PREFIX}}-N` Linear issue before code starts. No bare `# TODO` — write `# TODO({{PREFIX}}-N)`.
2. **One issue → one branch → one PR → one agent.** Use the issue's `gitBranchName` (contains the identifier → auto-links). The human merges; **never merge your own PR.**
3. **One agent per working tree.** A second concurrent agent uses a sibling worktree or GitHub/Linear-side ops only — never two agents branch-switching in one checkout (`.git/HEAD` race strands work).
4. **No secrets/PII in git.** `scripts/verify-clean-tree.py` is the pre-commit gate. Never `git commit --no-verify` without a written justification line in the commit message.
5. **Conventional commits, no AI attribution.** `feat()/fix()/test()/docs()/refactor()`. No "Generated with…", no `Co-Authored-By: Claude`.
6. **TDD.** Write the failing test first; watch it fail for the *right* reason; then minimal code. Never green a test by mocking the thing under test or ignoring failures.
7. **Never fabricate.** No invented APIs, file paths, statutes, config keys, or values. Cite a source (`file:line`) or say "uncertain" and ask.
8. **Surgical changes.** Every changed line traces to the task. Don't refactor what isn't broken; match existing style.

## §2 Audience map

| Agent | Reads | Owns |
|---|---|---|
| **Claude Code** (Opus/Sonnet) | this file + `.claude/rules/` | plan/implement/test/review per cadence |
| **Codex** | `AGENTS.md` (imports this) + universal rules | same cadence, no `/ck:*` slash commands |
| **Human** | everything | merge gate, Linear label rebalancing, final decisions |

## §3 Where the rules live (load on demand — detail is here, not above)

| File | Load when |
|---|---|
| `.claude/rules/context-economy.md` | managing context / token budget / compaction |
| `.claude/rules/knowledge-graph-graphify.md` | answering "how/where does X work"; before grepping |
| `.claude/rules/multi-agent-coordination.md` | coordinating with another agent; worktrees; routing |
| `.claude/rules/linear-discipline.md` | filing/claiming/labeling issues; cycles |
| `.claude/rules/quality-gates.md` | editing `src/**` or `tests/**`; committing |
| `.claude/rules/behavioral.md` | always — scout-first, anti-hallucination, comment hygiene |
| `.claude/rules/karpathy-guidelines.md` | always — the 4 anti-mistake guidelines |
| `.claude/rules/review-audit-self-decision.md` | reviewing/auditing; deciding whether to reverse a decision |
| `.claude/rules/learning-loop.md` | end of cycle; promoting a learning to an enforced rule |
| `.claude/rules/_APPLICABILITY.md` | unsure if a rule applies to Codex / team mode |

## §4 Cadence (one line)

**Plan → Cook → Test → Review → Docs → Commit → PR.** Detail: `docs/engineering-workflow.md`. New feature → start at `/ck:plan`; bug → `/ck:fix` (auto-scouts).

## §5 Token-tier routing (one line)

Frontier model (Opus) for the first ~15 min of meaningful work (frame + plan); then hand volume work to the mid-tier model / Codex. At >70% context fill, save a plan file and switch. Matrix: `multi-agent-coordination.md`.

## §6 graphify (one line)

Query the graph before grepping (`graphify query/path/explain`); run `graphify update .` after code changes. Protocol: `knowledge-graph-graphify.md`.

## §7 Project domain rules (overlay slot)

{{PROJECT_DOMAIN_RULES}}

> Keep domain invariants in a path-scoped `.claude/rules/domain-rules.md` and *reference* it here — do not inline them, or this file regrows the bloat this template exists to prevent.

## §8 Verify

`/memory` lists loaded instruction files; `/context` shows the token breakdown. Periodically audit for contradictions between this file, `.claude/rules/`, and the project brief.
