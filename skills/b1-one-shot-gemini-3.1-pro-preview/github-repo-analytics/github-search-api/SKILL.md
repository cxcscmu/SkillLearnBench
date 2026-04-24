---
name: github-search-api
description: Fetch repository metrics, issues, and pull requests over a specific date range using the GitHub Search API.
---

# GitHub Search API

The GitHub Search API is a powerful tool to extract data about issues and pull requests, allowing for filters based on creation date, closed date, repository, and more.

## Installation / Setup
No special installation is required beyond `curl` or a standard HTTP client like `requests` in Python. If a GitHub Personal Access Token (PAT) is available, use it via the `Authorization: Bearer <TOKEN>` header to increase rate limits.

## Key Concepts
- The API endpoint for issues/PRs is `https://api.github.com/search/issues`.
- The `q` parameter takes a Lucene-like query. For example: `repo:cli/cli is:pr created:2024-12-01..2024-12-31`.
- Pagination is handled via `per_page` (max 100) and `page` parameters.
- Pull requests are technically returned as issues in the search API. You differentiate them by checking the presence of a `pull_request` key in the item dictionary.

## Code Example (Python)

```python
import requests

def fetch_items(query):
    url = "https://api.github.com/search/issues"
    headers = {"Accept": "application/vnd.github.v3+json"}
    items = []
    page = 1
    
    while True:
        params = {"q": query, "per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        items.extend(data.get("items", []))
        
        if len(items) >= data.get("total_count", 0) or not data.get("items"):
            break
        page += 1
        
    return items

# Example usage:
# prs = fetch_items("repo:cli/cli is:pr created:2024-12-01..2024-12-31")
# print(f"Fetched {len(prs)} PRs.")
```

## Best Practices
- Always check `total_count` to ensure you are fetching all results.
- Implement rate limit handling if fetching large datasets or running frequently.
- When searching for labels with specific strings, it is often more reliable to fetch the items and filter them in memory using string matching on the label names.
