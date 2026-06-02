# Learning Loop

How a noticed learning becomes an *enforced* rule. Capture is cheap and transient; enforcement is the point.

## The ritual

1. **Capture (continuous, transient).** Agents note candidate learnings inline; memory plugins record the raw stream. This is a buffer, **not** the durable record.
2. **Triage (cycle-end, frontier model via a retro).** Review the cycle's observations + incidents; extract the few learnings worth promoting; tag each by type. The retro lands in `docs/retrospectives/`.
3. **Promote (routed by type; agent drafts, human merges — the gate).** One PR per cycle batch:
   - Architecture / tech-direction → **ADR** (`docs/adr/ADR-NN-*.md`)
   - Workflow / process / operating rule → **`docs/operator-standing-orders.md`** (+ `CLAUDE.md` pointer / `AGENTS.md` if cross-agent)
   - Tech-stack choice → the project brief / `pyproject.toml`
   - Behavioral / agent-discipline → **`.claude/rules/`**
4. **Enforce (automatic).** Promotions land in files agents read at session start (`CLAUDE.md`, `AGENTS.md`, `.claude/rules/`) → the next session inherits them.

## Rules of thumb

- Only *recurring* or *expensive-mistake* learnings earn a promotion PR. Most observations stay transient.
- A learning is "done" only when it's in a file an agent reads at session start. Auto-memory is the buffer, not the record.
- Keep machine-local auto-memory (`MEMORY.md`) gitignored; promote what's proven rather than relying on it.
