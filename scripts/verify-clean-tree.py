"""Secrets/PII pre-commit gate — generic, config-driven.

Scans the STAGED tree (``git diff --cached``) for two leak classes:
  1. forbidden paths (e.g. ``.env``, ``*.pem``, ``*.db``)
  2. forbidden content patterns (secret-looking strings) in staged blobs

All project specifics live in ``scripts/scan-rules.toml`` — keep this file generic.

Exit codes (stable contract):
  0  clean
  1  violation(s) found
  2  internal error (bad config, not a git repo, etc.)

Usage:
    python scripts/verify-clean-tree.py            # scan staged changes
    python scripts/verify-clean-tree.py --all      # scan whole working tree (tracked files)
"""
from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
import tomllib
from pathlib import Path

RULES_PATH = Path(__file__).resolve().parent / "scan-rules.toml"


def _load_rules() -> dict:
    try:
        return tomllib.loads(RULES_PATH.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        print(f"verify-clean-tree: cannot read {RULES_PATH}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def _git(args: list[str]) -> str:
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"verify-clean-tree: git failed: {exc}", file=sys.stderr)
        raise SystemExit(2)


def _staged_paths() -> list[str]:
    out = _git(["diff", "--cached", "--name-only", "--diff-filter=ACM"])
    return [p for p in out.splitlines() if p.strip()]


def _all_tracked_paths() -> list[str]:
    return [p for p in _git(["ls-files"]).splitlines() if p.strip()]


def _staged_blob(path: str, staged: bool) -> str | None:
    """Return file content (staged version if committing, else working tree)."""
    try:
        if staged:
            return _git(["show", f":{path}"])
        return Path(path).read_text(encoding="utf-8")
    except SystemExit:
        return None
    except (OSError, UnicodeDecodeError):
        return None


def _matches_any(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(path, f"**/{pat}") for pat in patterns)


def main() -> int:
    rules = _load_rules()
    staged = "--all" not in sys.argv
    paths = _staged_paths() if staged else _all_tracked_paths()

    forbidden = rules.get("forbidden_paths", [])
    allowed = rules.get("allowed_paths", [])
    content_allow = rules.get("content_check_allow_paths", [])
    skip_ext = set(rules.get("skip_content_extensions", []))
    patterns = [
        (p["name"], re.compile(p["regex"]), p.get("message", "forbidden pattern"))
        for p in rules.get("content_patterns", [])
    ]
    fixture_dir = rules.get("fixture_dir", "")
    fixture_marker = rules.get("fixture_safe_marker", "")

    violations: list[str] = []

    for path in paths:
        # 1. forbidden-path check
        if _matches_any(path, forbidden) and not _matches_any(path, allowed):
            violations.append(f"[path] {path} matches a forbidden path pattern")
            continue

        if Path(path).suffix.lower() in skip_ext:
            continue
        if _matches_any(path, content_allow):
            continue

        content = _staged_blob(path, staged)
        if content is None:
            continue

        # 2. content-pattern check
        for name, rx, msg in patterns:
            if rx.search(content):
                violations.append(f"[content:{name}] {path}: {msg}")

        # 3. fixture safe-marker check (optional)
        if fixture_dir and fixture_marker and _matches_any(path, [f"{fixture_dir}/**"]):
            if fixture_marker not in content:
                violations.append(
                    f"[fixture] {path}: missing safe marker '{fixture_marker}' "
                    f"(files under {fixture_dir}/ must prove they hold no real data)"
                )

    if violations:
        print("verify-clean-tree: BLOCKED — potential secrets/PII in the commit:", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        print(
            "\nFix the content (do not bypass). To override in a genuine false-positive, "
            "`git commit --no-verify` AND include a justification line in the commit message.",
            file=sys.stderr,
        )
        return 1

    print(f"verify-clean-tree: clean ({len(paths)} path(s) checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
