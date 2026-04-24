---
name: gh-issue-analysis
description: >
  How to fetch and analyze GitHub issues for a repository within a date range:
  total counts, bug report identification by label substring matching, and
  resolved bug counts. Use this skill whenever the user asks about issue
  metrics, bug counts, triage stats, or community health reports for a GitHub
  repo.
---

# Issue Analysis via GitHub REST API

## Fetching issues (excluding PRs)

The `/repos/{owner}/{repo}/issues` endpoint returns BOTH issues and PRs.
Filter out PRs by checking for the absence of the `pull_request` key:

```python
def get_issues(owner, repo, start_dt, end_dt, token=None):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    results, page = [], 1
    while True:
        r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues",
                         headers=headers,
                         params={"state": "all", "sort": "created",
                                 "direction": "desc", "per_page": 100,
                                 "page": page,
                                 "since": start_dt.isoformat()})
        data = r.json()
        if not data:
            break
        stop = False
        for item in data:
            if "pull_request" in item:
                continue   # skip PRs
            created = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
            if created > end_dt:
                continue
            if created < start_dt:
                stop = True
                break
            results.append(item)
        if stop or len(data) < 100:
            break
        page += 1
    return results
```

## Identifying bug reports

A bug report is any issue where **at least one label name contains the substring
`"bug"`** (case-insensitive):

```python
def is_bug(issue):
    return any("bug" in label["name"].lower() for label in issue.get("labels", []))

bug_issues = [i for i in issues if is_bug(i)]
```

Common matching labels: `bug`, `type: bug`, `kind/bug`, `confirmed-bug`, etc.

## Counting resolved bugs in the period

A bug is "resolved" (closed) during the period if:
- `is_bug(issue)` is True
- `issue["state"] == "closed"`
- `issue["closed_at"]` falls within the target month

```python
def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

resolved_bugs = [
    i for i in bug_issues
    if i["state"] == "closed"
    and i.get("closed_at")
    and start_dt <= parse_dt(i["closed_at"]) <= end_dt
]
```

> Note: An issue created before December can be closed in December and still
> count as a resolved bug for the period. Fetch with `state=all` and filter
> closed_at in Python.

## Gotchas

- The `since` query param on `/issues` filters by `updated_at`, not
  `created_at`. Always re-filter in Python using `created_at`.
- Labels may be empty (`[]`) for unlabelled issues — handle gracefully.
- Rate limit: each page = 1 request. With 60 unauthenticated requests, you can
  fetch ~6000 items before hitting the limit.
