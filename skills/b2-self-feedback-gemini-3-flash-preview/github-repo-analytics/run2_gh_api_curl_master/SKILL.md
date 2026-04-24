---
name: run2_gh_api_curl_master
description: Mastering GitHub API interactions using curl, including search, pagination, and rate limit handling.
---

# GitHub API with Curl

When the `gh` CLI is unavailable or unauthenticated, `curl` can be used to interact with the public GitHub API.

## Search API for Community Metrics

The Search API is powerful for time-based reports.

### Example: Pull Requests
```bash
curl -s "https://api.github.com/search/issues?q=repo:cli/cli+is:pr+created:2024-12-01..2024-12-31&per_page=100"
```

### Example: Issues
```bash
curl -s "https://api.github.com/search/issues?q=repo:cli/cli+is:issue+created:2024-12-01..2024-12-31&per_page=100"
```

## Handling Pagination

If `total_count` > `per_page`, you must iterate through pages:
```bash
curl -s "https://api.github.com/search/issues?q=...&page=2&per_page=100"
```

## Rate Limits

Unauthenticated requests are limited to 60 per hour (or 10 per minute for Search API). Check headers for status:
```bash
curl -i "https://api.github.com/..." | grep "x-ratelimit"
```

## Search Qualifiers

- `is:pr` or `is:issue`
- `created:YYYY-MM-DD..YYYY-MM-DD`
- `closed:YYYY-MM-DD..YYYY-MM-DD`
- `label:bug` (exact) or `label:"bug report"` (with spaces)
- `repo:OWNER/REPO`
