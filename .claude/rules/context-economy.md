# Context & Token Economy

Context is the scarce resource — especially under usage limits. Every token spent re-reading bloated instructions or dumping file contents is a token not spent reasoning.

## The CLAUDE.md tax

- `CLAUDE.md` is read **every session by every agent**. Keep it **≤300 lines**, invariants + pointers only.
- Three audiences, three homes — never mix:
  - *Stable invariants* → `CLAUDE.md` (rarely change).
  - *Active state* (what shipped, current status) → `docs/project-changelog.md` + Linear. **Never** a changelog inside `CLAUDE.md`.
  - *Path-specific how-to* → `.claude/rules/*.md` (loaded on demand).
- Test before adding a line to `CLAUDE.md`: "is this always true, for every task?" If it's "when editing X, do Y", it's a rule file, not `CLAUDE.md`.

## Reads dominate context

- Don't read a whole file when you need 30 lines — use offset/limit, or query the graph first (see `knowledge-graph-graphify.md`).
- Delegate broad/fan-out reads to a subagent and keep only its conclusion. You keep the answer, not the file dump.
- Prefer dedicated search tools over shelling out `cat`/`grep` for large outputs.

## Compaction survival

- When context is summarized, the **start** of each instruction file and the **root** `CLAUDE.md` survive most reliably. Put must-persist instructions at the top of files, unscoped.
- `/compact` preserves a summary + recent context to keep working; `/clear` resets. Use `/compact` mid-task, `/clear` between unrelated tasks. After `/clear`, restore via your handoff (plan file / `/context-restore`).

## Agent hand-off

- Frontier model (Opus) for the first ~15 min of meaningful work (frame + plan); hand volume to the mid-tier model / Codex.
- At **>70% context fill**, save a plan file and switch sessions/agents rather than pushing a degrading context further.

## MCP hygiene

- Keep MCP **Tool Search on**; force-load nothing. Each always-loaded tool's schema is permanent context cost.
- CLI and desktop-app MCP configs are **separate** — a server in the desktop app costs nothing in CLI sessions. Audit what each surface actually loads; prune unused.
- Scope a heavy MCP server to a single subagent's frontmatter rather than the global config when only that agent needs it.
