---
name: run2_github-rest-api
description: Query GitHub REST API with pagination and date filtering for repository data (PRs, issues).
---

# GitHub REST API Queries for Repository Analytics

## Overview
Use GitHub's REST API directly to query repository data with fine-grained filtering and pagination.

## Setup
- Python 3 with `urllib` (standard library)
- No external dependencies required
- No authentication needed for public repositories (subject to rate limits)

## Key Endpoints

### Pull Requests
```
GET /repos/{owner}/{repo}/pulls?state=all&per_page=100&sort=created&direction=desc&page={page}
```

### Issues
```
GET /repos/{owner}/{repo}/issues?state=all&per_page=100&sort=created&direction=desc&page={page}
```

## Important: PR vs Issue Distinction
The issues endpoint returns both issues AND pull requests. PRs have a `pull_request` field. To get true issues only, filter out items with `"pull_request" not in item`.

## Date Filtering
The API doesn't support server-side date filtering. Filter client-side by:
```python
created = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
if created.year == 2024 and created.month == 12:
    # Process item
```

## Pagination Strategy
1. Use `per_page=100` for efficiency (max allowed)
2. Check results to find earliest date per page
3. Stop when all items in a page are before your target date range
4. Note: Results within pages may not be monotonically ordered across all pages

## Date Handling
- GitHub returns UTC timestamps in ISO 8601 format (e.g., "2024-12-15T10:30:45Z")
- Remove 'Z' and replace with '+00:00' for Python's `datetime.fromisoformat()`
- Compare timezone-aware datetimes only

## State Values
- `state=all`: both open and closed items
- `state=open`: only open
- `state=closed`: only closed
- For PRs only: `state=merged` (not standard, use state check in response)

## Response Fields
Key fields for analytics:
- `created_at`: ISO 8601 timestamp
- `merged_at`: For PRs, null if not merged
- `closed_at`: When closed (null if open)
- `state`: "open", "closed" (for PRs, may be "merged" in older API versions)
- `user.login`: Author username
- `labels`: Array of `{name: string}`
- `pull_request`: Present only for PRs (when querying issues)

## Error Handling
- Implement timeout handling (network delays)
- Check HTTP status codes
- Handle rate limiting (429 status)
- Graceful degradation for network failures

## Example Rate Limits
- Unauthenticated: 60 requests/hour
- Authenticated: 5,000 requests/hour
