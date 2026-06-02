# Review / Audit / Self-Decision

The most load-bearing file for cross-agent consistency. Governs when an agent may reverse a decision and how to treat audit findings. Read before any non-trivial review or audit.

## 1. Verified decisions are sticky — audits don't auto-reverse

- Once a decision is verified (read the source, ran the test, ran the experiment), lock it with a source note: `verified by {file:line}` or `verified by test {name}`.
- An audit/red-team counter-argument **alone is insufficient** to revise. Revise only when the audit brings (a) a *new* issue the verification missed — state it and why the prior check missed it — or (b) context changed since.
- Surface contradictions to the human: "audit says X, but Y is verified by {source} — does the audit bring new data to justify a reverse?" Do **not** silently flip.

## 2. Validate findings against the real threat model

Before applying a finding flagged "too narrow / too loose / risky":

1. Identify what the code actually does/protects.
2. Walk each flagged scenario through that lens — does it produce a real bad outcome, or only a theoretical one?
3. Real → fix. Non-real → document the rationale. Borderline → ask.
4. Look for the failure mode the reviewer *missed* — often one step from what was flagged.

Anti-pattern: accepting every "widen/harden/add-check" recommendation without tracing it to a real failure.

## 3. Guard human decisions against audit/YAGNI drift

**Never silently reverse a decision the human already confirmed.** Before any cut/change from an audit:

- Trace before cutting: did the human explicitly choose that value/design?
- Categorize: ✅ safe (things Claude proposed, never confirmed) · ⚠️ confirm-first (thresholds, scope, library, schema, feature inclusion the human chose) · 🚫 never auto-reverse (business/pricing/compliance/scope-boundary decisions).
- Surface reversals: present the human's original decision, the audit reasoning, the trade-off, and ask "keep / change / hybrid?" — don't apply.
- Auditors lean YAGNI/minimalism — their output is **input to the human, not orders to the agent**.

## 4. Scout-first, ask-second

See `behavioral.md`. Grep/read/graph answers it (confidence ≥85%) → answer with a citation. Otherwise ask. Don't ask what a 5-second scout resolves; don't guess what needs human judgment.

## 5. No plan references in code/artifacts

See `behavioral.md` (comment hygiene). Code/migration/test names explain the *why*, never the *origin* (no phase/finding/audit labels) — those references rot when plans get renumbered.
