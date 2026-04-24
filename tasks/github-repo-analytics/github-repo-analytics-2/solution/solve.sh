#!/bin/bash
set -e

python3 << 'EOF'
import json
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional

OUTPUT = Path("/app/report.json")
PARAM_CANDIDATES = (
    Path("/solution/query_params.json"),
    Path("query_params.json"),
    Path("/app/solution/query_params.json"),
)
GRAPHQL_QUERY = """
query($searchQuery: String!, $cursor: String) {
  search(query: $searchQuery, type: ISSUE, first: 100, after: $cursor) {
    nodes {
      ... on PullRequest {
        number
        state
        createdAt
        mergedAt
        closedAt
        author {
          login
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""


def load_params() -> dict:
    for path in PARAM_CANDIDATES:
        if path.exists():
            return json.loads(path.read_text())
    raise FileNotFoundError("query_params.json not found in solution directory")


PARAMS = load_params()
REPO = PARAMS["repo"]
DATE_RANGE = PARAMS["date_range"]
CUTOFF = PARAMS["cutoff"]


def gh_search_prs(repo: str, date_range: str) -> list[dict]:
    search_query = f"repo:{repo} is:pr created:{date_range}"
    prs: list[dict] = []
    cursor = None

    while True:
        cmd = [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={GRAPHQL_QUERY}",
            "-F",
            f"searchQuery={search_query}",
        ]
        if cursor:
            cmd += ["-F", f"cursor={cursor}"]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        payload = json.loads(result.stdout)
        page = payload["data"]["search"]
        prs.extend(node for node in page["nodes"] if node)

        if not page["pageInfo"]["hasNextPage"]:
            return prs

        cursor = page["pageInfo"]["endCursor"]


def days_between(start: str, end: str) -> float:
    t1 = datetime.fromisoformat(start.replace('Z', '+00:00'))
    t2 = datetime.fromisoformat(end.replace('Z', '+00:00'))
    return (t2 - t1).total_seconds() / 86400


def at_or_before_cutoff(ts: Optional[str]) -> bool:
    if not ts:
        return False
    moment = datetime.fromisoformat(ts.replace('Z', '+00:00'))
    cutoff = datetime.fromisoformat(CUTOFF.replace('Z', '+00:00'))
    return moment <= cutoff


def top_contributor(prs: list[dict]) -> str:
    authors = Counter(
        pr["author"]["login"]
        for pr in prs
        if pr.get("author") and pr["author"].get("login")
    )
    if not authors:
        return ""

    max_count = max(authors.values())
    return min(login for login, count in authors.items() if count == max_count)


def main():
    prs = gh_search_prs(REPO, DATE_RANGE)

    merged_prs = [p for p in prs if at_or_before_cutoff(p.get('mergedAt'))]
    closed_without_merge_prs = [
        p for p in prs
        if at_or_before_cutoff(p.get('closedAt')) and not at_or_before_cutoff(p.get('mergedAt'))
    ]

    pr_stats = {
        "total": len(prs),
        "merged": len(merged_prs),
        "closed": len(closed_without_merge_prs),
        "avg_merge_days": round(sum(days_between(p['createdAt'], p['mergedAt']) for p in merged_prs) / len(merged_prs), 1) if merged_prs else 0,
        "top_contributor": top_contributor(prs),
    }

    expected = {"pr": pr_stats}

    OUTPUT.write_text(json.dumps(expected, indent=2))
    print(f"Saved to {OUTPUT}")
    print(json.dumps(expected, indent=2))


if __name__ == '__main__':
    main()

EOF
