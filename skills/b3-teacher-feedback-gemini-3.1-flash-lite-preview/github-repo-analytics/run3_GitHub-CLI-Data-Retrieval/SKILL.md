---
name: GitHub CLI Data Retrieval
description: Used to query, filter, and extract metadata from GitHub PRs and Issues using the `gh` command line tool with appropriate search qualifiers and pagination limits.
---

To retrieve data from GitHub using the `gh` CLI, follow these standards:

1. **Broaden Scope:** Always use the `-s all` flag (or `state:all`) to ensure the command retrieves merged, closed, and open items.
2. **Apply Search Qualifiers:** Use the `-S` flag with the search query `created:2024-12-01..2024-12-31`. Do not use date ranges that exceed the repository activity window.
3. **Lift Limits:** Explicitly set the `--limit` flag to a high value (e.g., `--limit 1000`) to avoid the default truncation of results, which causes inaccurate counts.
4. **Select Fields Carefully:** When using `--json`, always verify the object path. For user names, use `author.login`. For dates, use `createdAt`, `mergedAt`, and `closedAt` to ensure accurate time calculations.
5. **JSON Formatting:** Rely on `jq` to process raw JSON output from `gh`. Ensure all calculations (averages, counts) handle empty arrays by providing default values (e.g., `0`) to prevent null-pointer or syntax errors in the final output file.