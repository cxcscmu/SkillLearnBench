---
name: run2_gh-rest-api
description: Using the GitHub REST Search API to query PRs and issues with date filtering, pagination, and field extraction.
---

# GitHub REST Search API for Repository Activity

## Search endpoints
- PRs: `https://api.github.com/search/issues?q=repo:OWNER/REPO+type:pr+created:YYYY-MM-DD..YYYY-MM-DD`
- Issues: `https://api.github.com/search/issues?q=repo:OWNER/REPO+type:issue+created:YYYY-MM-DD..YYYY-MM-DD`

## Pagination
- `per_page` max is 100
- Use `&page=N` for subsequent pages
- `total_count` in response gives total matches

## PR states in Search API
- Search API returns `state: "open"` or `state: "closed"`
- Merged PRs have `state: "closed"` AND `pull_request.merged_at != null`
- Closed-not-merged PRs have `state: "closed"` AND `pull_request.merged_at == null`
- The `pull_request` object in search results contains `merged_at`

## Issue fields
- `labels`: array of objects with `name`, `color`, etc.
- `state`: "open" or "closed"
- `closed_at`: ISO 8601 timestamp or null
- `created_at`: ISO 8601 timestamp

## Rate limiting
- Unauthenticated: 10 requests/minute for search API
- Authenticated: 30 requests/minute
- Add `&per_page=100` to minimize requests

## Important notes
- Search API `created:` qualifier uses inclusive date range
- `closed:` qualifier can filter by close date: `closed:2024-12-01..2024-12-31`
- The `type:issue` excludes PRs; `type:pr` excludes issues
