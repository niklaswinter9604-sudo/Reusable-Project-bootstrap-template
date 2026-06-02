---
paths: ["src/**", "tests/**", "pyproject.toml"]
---

# Quality Gates

Binds anything touching `src/**` or `tests/**`.

## TDD (non-negotiable for logic)

1. Write the **failing test first**.
2. Run it — **watch it fail**, and confirm it fails for the *right reason* (feature missing, not a typo/import error). A test that never failed proves nothing.
3. Write the **minimal** code to pass.
4. Re-run; confirm green and no other test broke.

**Prove a test can fail** before trusting it (the anti-tautology rule): for an important assertion, neutralize the production code once and confirm the test goes red. A green test that can't go red is theater.

Never green a test by mocking the thing under test, weakening the assertion, or `xfail`/skip without a written reason. Never ignore failing tests to pass CI.

## Coverage ratchet

- `fail_under = 90` (config). Start `source = ["src"]` broad; as packages harden, narrow the gated set per-package and **widen** it — coverage only ratchets up.
- New/changed code must be covered. Pre-existing untested code is out of scope unless you're touching it.
- Recommended: enforce in CI (`pytest --cov --cov-fail-under=90`), not only in config, so a local skip can't slip through.

## Pre-commit chain

Order (fail-fast): `ruff check` → `mypy` → `pytest` (unit) → `python scripts/verify-clean-tree.py`. Any non-zero aborts the commit.

`verify-clean-tree.py` is the **secrets/PII gate** — exit `0` clean / `1` violation / `2` internal error. Never `--no-verify` past it without a written justification line in the commit message.

## Mechanics

- Compile/lint-check after every create or modify; don't leave syntax errors for the test run to find.
- pytest: `--import-mode=importlib`; accept both `test-*.py` and `test_*.py`.
- Keep files under ~200 LOC; split when they exceed it (extract modules, not god-files).
