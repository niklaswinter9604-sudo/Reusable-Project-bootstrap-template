"""Create the canonical Linear label taxonomy for a project. Idempotent.

Reads LINEAR_API_KEY from the environment and creates the grouped label sets
(agent / stage / area) plus flat flag labels. Re-running skips existing labels.

Usage:
    export LINEAR_API_KEY=lin_api_...
    python scripts/setup-linear-labels.py --team {{PREFIX}}
    python scripts/setup-linear-labels.py --team {{PREFIX}} --flags-grouped   # opt into grouped flags

Note: PR-status workflow automation (push->In Progress, PR->In Review, merge->Done)
must be wired manually in Linear Team Settings -> Workflows — the API cannot set it.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.linear.app/graphql"

# Grouped label sets. Edit AREA for your project's code paths.
GROUPS: dict[str, list[str]] = {
    "agent": ["opus", "sonnet", "codex", "human"],
    "stage": ["plan", "implement", "test", "review", "docs", "ship", "retro"],
    "area": ["api", "db", "cli", "infra", "docs"],  # {{PROJECT_AREAS}}
}
FLAGS = ["blocker", "research-needed", "sensitive"]  # flat by default


def _gql(query: str, variables: dict, key: str) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API, data=body,
        headers={"Authorization": key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        sys.exit(f"Linear API error {exc.code}: {exc.read().decode(errors='replace')}")
    if "errors" in data:
        sys.exit(f"Linear GraphQL error: {data['errors']}")
    return data["data"]


def _team_id(prefix: str, key: str) -> str:
    q = "query { teams { nodes { id key name } } }"
    for t in _gql(q, {}, key)["teams"]["nodes"]:
        if t["key"].lower() == prefix.lower() or t["name"].lower() == prefix.lower():
            return t["id"]
    sys.exit(f"No Linear team matching '{prefix}'. Found: "
             f"{[t['key'] for t in _gql(q, {}, key)['teams']['nodes']]}")


def _existing_labels(team_id: str, key: str) -> set[str]:
    q = ("query($id:String!){ team(id:$id){ labels(first:250){ nodes { name } } } }")
    nodes = _gql(q, {"id": team_id}, key)["team"]["labels"]["nodes"]
    return {n["name"] for n in nodes}


def _create(team_id: str, name: str, key: str) -> None:
    m = ("mutation($i:IssueLabelCreateInput!){ issueLabelCreate(input:$i){ success } }")
    _gql(m, {"i": {"teamId": team_id, "name": name}}, key)
    print(f"  + created {name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True, help="Linear team key/prefix, e.g. NIK")
    ap.add_argument("--flags-grouped", action="store_true",
                    help="create flags as a grouped set (default: flat, so flags co-occur)")
    args = ap.parse_args()

    key = os.environ.get("LINEAR_API_KEY")
    if not key:
        sys.exit("Set LINEAR_API_KEY in the environment.")

    team_id = _team_id(args.team, key)
    existing = _existing_labels(team_id, key)

    wanted: list[str] = []
    for group, values in GROUPS.items():
        wanted += [f"{group}:{v}" for v in values]
    wanted += [(f"flag:{f}" if args.flags_grouped else f"flag:{f}") for f in FLAGS]

    print(f"Team {args.team}: {len(existing)} existing labels; ensuring {len(wanted)}.")
    for name in wanted:
        if name in existing:
            print(f"  = exists {name}")
        else:
            _create(team_id, name, key)

    print("\nDone. MANUAL next step: Team Settings -> Workflows -> wire "
          "push->In Progress, PR->In Review, merge->Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
