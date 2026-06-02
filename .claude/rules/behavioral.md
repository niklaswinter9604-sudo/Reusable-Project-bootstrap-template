# Behavioral Rules

Always active. Pairs with `karpathy-guidelines.md` (the 4 anti-mistake guidelines) and `review-audit-self-decision.md` (when to reverse a decision).

## Scout-first, ask-second

For anything answerable by grep/read/graphify on the codebase:

1. **Scout first** — query the graph, read the live code, check current state.
2. **Self-rate confidence (0–100%):**
   - **≥ ~85%** → answer directly with a `path:line` citation.
   - **< 85%** → ask the human.
3. Ask only when: confidence is low, two sources genuinely conflict (not a stale note already verified), a real business/UX judgment is needed, or the action is high-risk/hard-to-reverse.

Anti-pattern: asking what grep answers in 5 seconds. Good pattern: "verified at `file:line`, confidence ~95%, applying X."

## Anti-hallucination

- Never fabricate APIs, file paths, config keys, statutes, or values. If unsure of an exact name/signature, look it up (graph/docs) or say "uncertain" and ask.
- Mark uncertainty explicitly (e.g. a `requires_validation` flag in output, or a clear "UNVERIFIED" note) rather than presenting a guess as fact.
- Report outcomes faithfully: if tests failed, say so with the output; if a step was skipped, say that. State "done" only when verified.

## Comment & artifact hygiene — explain *why*, never *origin*

Code comments, file names, migration names, and test names **must not** reference plan artifacts (phase numbers, finding codes like F13/A4, audit labels, brainstorm sections). Those references become unresolvable noise when plans get renumbered.

- Explain the invariant/race/trade-off: `// org-scoped lock serializes concurrent reassigns` — not `// per F13 fix`.
- Migration/test names use a domain slug, not a phase number.
- Allowed: symbol names, stable external IDs (RFC, CVE, SQLSTATE, durable issue numbers). Plan refs belong in `plans/` and PR descriptions, not in code.

## Confirm before irreversible/outward-facing actions

For hard-to-reverse or outward-facing actions (publishing, deleting, deploying, sending), confirm first unless durably authorized. Approval in one context does not extend to the next. Before deleting/overwriting, look at the target — if it contradicts how it was described, surface that instead of proceeding.
