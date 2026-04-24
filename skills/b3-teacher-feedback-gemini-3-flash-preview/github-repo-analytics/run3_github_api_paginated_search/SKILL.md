---
name: github_api_paginated_search
description: Fetch data from GitHub's Search API using the GitHub CLI (gh) while correctly handling pagination and merging results. Use this when you need to retrieve more than 100 items or ensure full dataset coverage for a specific period.
---

To fetch all items from a GitHub search query across multiple pages:

1. Use the `gh api` command with the `--paginate` flag.
2. Target the `search/issues` endpoint (which covers both Issues and Pull Requests).
3. Append your query using the `-f q="..."` parameter.
4. Use `jq` with the `-s` (slurp) flag to combine the separate JSON objects returned for each page into a single array of items.

Example for fetching all PRs created in a specific month:
```bash
gh api --paginate "search/issues" -f q="repo:cli/cli is:pr created:2024-12-01..2024-12-31" | jq -s 'map(.items) | add' > prs.json
```

Key considerations:
- **Pagination**: Without `-s 'map(.items) | add'`, `jq` will only process the first page's object or encounter errors when trying to treat multiple JSON objects as a single stream.
- **Separate Queries**: Use distinct queries for "created" and "closed" events to ensure accuracy, as an item created in one month might be closed in another.