---
name: run2_github-api-data-fetcher
description: Provides a robust python module for querying GitHub's search API using urllib with automatic pagination.
---

# GitHub API Data Fetcher (Improved)

Use this skill when you need to retrieve large numbers of issues or pull requests from a GitHub repository, apply complex filters, and perform calculations on the results without hitting pagination limits immediately.

## Setup
Built-in Python libraries (`urllib`, `json`, `datetime`) are used. No external installations are required.

## Usage
```python
import urllib.request
import urllib.parse
import json
from datetime import datetime

def fetch_search_all(query):
    """
    Fetches all results from the GitHub Search API for a given query,
    automatically handling pagination.
    """
    items = []
    page = 1
    while True:
        url = f"https://api.github.com/search/issues?q={urllib.parse.quote(query)}&per_page=100&page={page}"
        req = urllib.request.Request(url, headers={'User-Agent': 'python'})
        resp_data = json.loads(urllib.request.urlopen(req).read().decode())
        items.extend(resp_data.get('items', []))
        
        # Stop if we have fetched all items or the page is not full
        if len(items) >= resp_data.get('total_count', 0) or len(resp_data.get('items', [])) < 100:
            break
        page += 1
    return items

def calculate_average_merge_time(prs):
    """
    Given a list of PR items from the Search API, calculates the average time to merge.
    Returns the average in days, rounded to one decimal place.
    """
    merge_times = []
    for pr in prs:
        merged_at_str = pr.get('pull_request', {}).get('merged_at')
        if merged_at_str:
            created_at = datetime.strptime(pr['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            merged_at = datetime.strptime(merged_at_str, "%Y-%m-%dT%H:%M:%SZ")
            days = (merged_at - created_at).total_seconds() / (24 * 3600)
            merge_times.append(days)
            
    return round(sum(merge_times) / len(merge_times), 1) if merge_times else 0.0

# Example: Get all PRs created in Dec 2024 and calculate merge time
prs = fetch_search_all("repo:cli/cli type:pr created:2024-12-01..2024-12-31")
avg_days = calculate_average_merge_time(prs)
print(f"Average merge time: {avg_days} days")
```