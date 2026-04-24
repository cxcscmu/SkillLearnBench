import json
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest

REPORT = Path("/app/report.json")
PARAMS = json.loads((Path(__file__).parent / "query_params.json").read_text())
REPO = PARAMS["repo"]
DATE_RANGE = PARAMS["date_range"]
CUTOFF = PARAMS["cutoff"]
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
    t1 = datetime.fromisoformat(start.replace("Z", "+00:00"))
    t2 = datetime.fromisoformat(end.replace("Z", "+00:00"))
    return (t2 - t1).total_seconds() / 86400


def at_or_before_cutoff(ts: Optional[str]) -> bool:
    if not ts:
        return False
    moment = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    cutoff = datetime.fromisoformat(CUTOFF.replace("Z", "+00:00"))
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


def build_expected() -> dict:
    prs = gh_search_prs(REPO, DATE_RANGE)
    merged_prs = [pr for pr in prs if at_or_before_cutoff(pr.get("mergedAt"))]
    closed_without_merge_prs = [
        pr for pr in prs
        if at_or_before_cutoff(pr.get("closedAt")) and not at_or_before_cutoff(pr.get("mergedAt"))
    ]
    return {
        "pr": {
            "total": len(prs),
            "merged": len(merged_prs),
            "closed": len(closed_without_merge_prs),
            "avg_merge_days": round(
                sum(days_between(pr["createdAt"], pr["mergedAt"]) for pr in merged_prs) / len(merged_prs),
                1,
            ) if merged_prs else 0,
            "top_contributor": top_contributor(prs),
        }
    }


@pytest.fixture
def report():
    assert REPORT.exists(), f"Missing {REPORT}"
    return json.loads(REPORT.read_text())


@pytest.fixture(scope="session")
def expected():
    return build_expected()


class TestPR:
    def test_schema(self, report):
        assert set(report.keys()) == {"pr"}
        assert set(report["pr"].keys()) == {
            "total",
            "merged",
            "closed",
            "avg_merge_days",
            "top_contributor",
        }

    def test_total(self, report, expected):
        assert report["pr"]["total"] == expected["pr"]["total"]

    def test_merged(self, report, expected):
        assert report["pr"]["merged"] == expected["pr"]["merged"]

    def test_closed(self, report, expected):
        assert report["pr"]["closed"] == expected["pr"]["closed"]

    def test_avg_merge_days(self, report, expected):
        assert report["pr"]["avg_merge_days"] == pytest.approx(expected["pr"]["avg_merge_days"], abs=1e-9)

    def test_avg_merge_days_is_rounded(self, report):
        assert round(report["pr"]["avg_merge_days"], 1) == pytest.approx(report["pr"]["avg_merge_days"], abs=1e-9)

    def test_top_contributor(self, report, expected):
        assert report["pr"]["top_contributor"] == expected["pr"]["top_contributor"]
