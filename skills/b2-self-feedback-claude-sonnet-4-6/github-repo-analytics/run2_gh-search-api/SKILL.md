---
name: run2_gh-search-api
description: How to query the GitHub Search API for PRs and issues with date filtering, handling pagination and unauthenticated access via Python urllib.
---

# GitHub Search API via Python urllib

## Overview
The GitHub Search API (`/search/issues`) supports date-range filtering and covers both PRs and Issues. No authentication needed for public repos (rate limit: 10 req/min, 60/hr unauthenticated).

## Endpoint
```
GET https://api.github.com/search/issues?q=QUERY&per_page=100&page=N
```

## Query Syntax for Date Range
```python
# PRs created in December 2024
pr_query = "repo:cli/cli is:pr created:2024-12-01..2024-12-31"

# Issues created in December 2024
issue_query = "repo:cli/cli is:issue created:2024-12-01..2024-12-31"
```

## Response Structure
```json
{
  "total_count": 50,
  "incomplete_results": false,
  "items": [
    {
      "number": 123,
      "state": "open" | "closed",
      "created_at": "2024-12-05T10:00:00Z",
      "closed_at": "2024-12-10T15:00:00Z" | null,
      "user": {"login": "username"},
      "labels": [{"id": 1, "name": "bug", "color": "..."}],
      "pull_request": {   // only present for PRs
        "merged_at": "2024-12-10T15:00:00Z" | null,
        "html_url": "...",
        "url": "..."
      }
    }
  ]
}
```

## Python Fetch Function (no external dependencies)
```python
import json, time, urllib.request, urllib.parse

def fetch_search(query, per_page=100):
    """Fetch all items from GitHub search API with pagination."""
    all_items = []
    page = 1
    while True:
        encoded_q = urllib.parse.quote(query)
        url = f"https://api.github.com/search/issues?q={encoded_q}&per_page={per_page}&page={page}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "stats-script/1.0"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        items = data.get("items", [])
        all_items.extend(items)
        total = data.get("total_count", 0)
        if len(all_items) >= total or len(items) < per_page:
            break
        page += 1
        time.sleep(1)  # respect rate limit
    return all_items
```

## Important Notes
- Search API max: 1000 results. For repos with >1000 monthly items, split query by date sub-ranges.
- `incomplete_results: true` means results may be truncated due to timeout (not rate limit).
- The `pull_request` key is present on all PR items; `merged_at` within it is null if not merged.
- Labels are returned as objects: `{"id": int, "name": str, "color": str, ...}` — extract with `.get("name")`.
