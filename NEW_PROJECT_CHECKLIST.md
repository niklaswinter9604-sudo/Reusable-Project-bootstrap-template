# New Project Checklist

One pass, top to bottom. Each step is concrete; do not skip the `{{PLACEHOLDER}}` substitution.

## 1. Clone + reset history

```bash
git clone <this-template> my-new-project && cd my-new-project
rm -rf .git && git init && git add -A && git commit -m "chore: bootstrap from template"
```

## 2. Set the placeholders

Find-and-replace across the repo (`rg -l '{{'` to locate):

- `{{PROJECT_NAME}}`, `{{ONE_LINE_MISSION}}`
- `{{CANONICAL_CHECKOUT_PATH}}` (absolute path you will always work in)
- `{{PREFIX}}` (Linear team prefix, e.g. `NIK`), `{{LINEAR_PROJECT_ID}}`
- `{{GITHUB_REPO}}` (`owner/name`)
- `{{DATA_DIR}}` (gitignored data dir, if any)
- `{{PROJECT_DOMAIN_RULES}}` in `CLAUDE.md §7` — leave as a pointer to `.claude/rules/domain-rules.md` (create that file with your domain invariants)

## 3. Python toolchain

```bash
uv init            # if not already a package
uv sync
uv run pytest -q   # confirm the harness runs (0 tests is fine to start)
```

## 4. Secrets gate

```bash
# Review scripts/scan-rules.toml; add any project-specific forbidden paths/patterns.
python scripts/verify-clean-tree.py   # exit 0 on a clean tree
```

## 5. graphify

```bash
uv tool install --upgrade graphify          # (package name per the graphify repo)
graphify extract . --no-cluster             # build the initial graph (there is no `graphify init`)
graphify claude install                     # session-start + post-commit hooks for Claude Code
graphify codex install                      # equivalent for Codex
graphify query "what is this project"       # smoke test
```

## 6. Linear

```bash
export LINEAR_API_KEY=lin_api_...
python scripts/setup-linear-labels.py       # idempotent; creates agent/stage/area + flag labels
```

Then, **manually in the Linear UI** (the script cannot do these):

- [ ] Wire PR-status workflow automation: push → In Progress, PR opened → In Review, PR merged → Done.
- [ ] Enable 1-week, ISO-named cycles (`2026-W23`…) with auto-rollover.
- [ ] Create GitHub milestones mirroring Linear milestones 1:1 by name.

## 7. Verify the agent setup

- [ ] `/memory` lists `CLAUDE.md` + the `.claude/rules/` files.
- [ ] `/context` shows a healthy token budget (CLAUDE.md should be a small slice).
- [ ] Read `.claude/rules/_APPLICABILITY.md` to confirm which rules apply to Codex.

## 8. First feature

```
/ck:plan "<first feature>"      # frame + plan on the frontier model
/ck:cook <absolute plan path>   # implement (mid-tier / Codex)
```

---

## Phase 2 (add when the pain is real, not before)

- [ ] Git hooks: `.githooks/pre-commit` (ruff → mypy → pytest → verify-clean-tree) + `post-commit` (`graphify update .`), installed via `git config core.hooksPath .githooks`. Or a `.pre-commit-config.yaml`.
- [ ] CI: GitHub Actions running `uv sync` + `pytest --cov --cov-fail-under=90` (makes the coverage gate CI-enforced, not just config).
- [ ] `pyproject.toml` coverage ratchet: start `source=["src"]`, narrow per-package + widen as each hardens.
- [ ] `plans/templates/` plan + phase-file templates.
- [ ] Agent-team mode (`team-coordination-rules`) — only at 5+ concurrent agents.
