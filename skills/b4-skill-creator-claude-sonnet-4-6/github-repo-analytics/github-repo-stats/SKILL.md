---
name: github-repo-stats
description: >
  How to gather GitHub repository statistics (PRs, issues, contributors) using
  the GitHub REST API via curl and Python. Use this skill whenever the user asks
  for a community pulse, activity summary, monthly report, or repository metrics
  for any GitHub repo — even if they don't explicitly mention the API.
---

# GitHub Repository Stats via REST API

## Overview

Use the GitHub REST API (no SDK needed) with `curl` + `python3` to pull PR and
issue data for a given repo and date range. The unauthenticated rate limit is 60
requests/hour; set `GITHUB_TOKEN` in the environment for 5000/hour.

## Base URL pattern

```
https://api.github.com/repos/{owner}/{repo}/pulls     # PRs
https://api.github.com/repos/{owner}/{repo}/issues    # Issues (includes PRs!)
https://api.github.com/search/issues                  # Search endpoint
```

> Issues endpoint returns both issues AND pull requests. Filter with
> `"pull_request" in item` to separate them.

## Authenticated header (use when token available)

```bash
AUTH_HEADER="-H \"Authorization: token $GITHUB_TOKEN\""
```

## Pagination pattern

GitHub paginates at 100 items max per page. Always loop until an empty page:

```python
import requests, time

def fetch_all(url, params, token=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    headers["Accept"] = "application/vnd.github+json"
    results = []
    page = 1
    while True:
        params["page"] = page
        params["per_page"] = 100
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 403:
            time.sleep(60)   # rate-limited, back off
            continue
        data = r.json()
        if not data:
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results
```

## Date filtering

GitHub REST API supports `since` parameter (ISO 8601) for issues/PRs but NOT
`until`. Filter the `until` boundary in Python after fetching:

```python
from datetime import datetime, timezone

def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

start = datetime(2024, 12, 1, tzinfo=timezone.utc)
end   = datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

created_in_range = [i for i in items
                    if start <= parse_dt(i["created_at"]) <= end]
```

## Key fields

| Field | Description |
|---|---|
| `number` | PR/issue number |
| `state` | `"open"` or `"closed"` |
| `created_at` | ISO 8601 creation timestamp |
| `closed_at` | ISO 8601 close timestamp (null if open) |
| `merged_at` | ISO 8601 merge timestamp (PRs only, null if unmerged) |
| `pull_request.merged_at` | In issue-endpoint results; same as above |
| `user.login` | Author login |
| `labels` | List of `{"name": "..."}` objects |

## Detecting merged PRs

Via `/pulls` endpoint, `merged_at` is present and non-null.
Via `/issues` endpoint, check `item.get("pull_request", {}).get("merged_at")`.

## Computing average time-to-merge

```python
from datetime import datetime, timezone

def days_between(a, b):
    da = datetime.fromisoformat(a.replace("Z", "+00:00"))
    db = datetime.fromisoformat(b.replace("Z", "+00:00"))
    return (db - da).total_seconds() / 86400

merged = [p for p in prs if p.get("merged_at")]
avg = sum(days_between(p["created_at"], p["merged_at"]) for p in merged) / len(merged)
avg_rounded = round(avg, 1)
```

## Finding top contributor

```python
from collections import Counter
logins = [p["user"]["login"] for p in prs]
top = Counter(logins).most_common(1)[0][0]
```

## Output: write report.json

```python
import json, pathlib
report = {
    "pr": {
        "total": total_prs,
        "merged": merged_count,
        "closed": closed_count,
        "avg_merge_days": avg_merge_days,
        "top_contributor": top_contributor,
    },
    "issue": {
        "total": total_issues,
        "bug": bug_count,
        "resolved_bugs": resolved_bugs,
    }
}
pathlib.Path("/app/report.json").write_text(json.dumps(report, indent=2))
```
