# Knowledge Graph (graphify)

graphify builds a local, queryable knowledge graph of the codebase at `graphify-out/`. Used well it delivers a large token reduction vs. raw grep/file reads. Most teams install it and use only `query` — the rest of this file is the part that's usually dormant.

## Query-first protocol

Before grepping or reading large files for "how/where does X work":

1. `graphify query "<question>"` — returns a scoped subgraph, usually far smaller than raw search output.
2. `graphify path "<A>" "<B>"` — the relationship/dependency chain between two symbols.
3. `graphify explain "<concept>"` — a focused concept neighborhood.
4. Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review; read `graphify-out/wiki/index.md` for navigation when it exists.

## Impact pre-flight

Before editing a load-bearing module, run `graphify path "<target>" "<dependent>"` to scope the blast radius. Cheaper and less error-prone than tracing dependencies by hand or trusting memory.

## Close the feedback loop (the dormant half)

- After a query produces a genuinely useful answer, run `graphify save-result` so the relationship enters graph memory (`graphify-out/memory/`) and future sessions inherit it. This is the antidote to amnesiac sessions.
- Generate the wiki once (`graphify-out/wiki/`) so agents — especially Codex — navigate via the index instead of grepping the whole tree.

## Keep it fresh

- After modifying code, run `graphify update .` (AST-only; no API cost) to keep the graph current.
- Use `--force` re-extraction only after deletions/large refactors.
- The post-commit hook (Phase 2) automates `update .`. Until installed, run it manually after edits.

## Hygiene

- Only `GEMINI_API_KEY` / `GOOGLE_API_KEY` are read for the semantic extraction pass; AST `update` needs no key.
- There is **no** `graphify init` — build the graph with `graphify extract .` (or the `/graphify` skill).
- Commit `graphify-out/` so the graph is shared context (it auto-rebuilds on commit).
