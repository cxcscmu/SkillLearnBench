---
name: github-report-builder
description: >
  Build structured JSON reports from GitHub repository activity data. Use this skill
  whenever you need to compile PR and issue statistics into a formatted JSON file for
  meeting summaries, community pulse reports, or stakeholder updates. Triggers on tasks
  that require outputting a report.json or similar artifact from GitHub metrics.
---

# GitHub Report Builder

Compile GitHub activity metrics into a structured JSON report.

## Report Schema

```json
{
  "pr": {
    "total": "<int> total PRs created in period",
    "merged": "<int> PRs merged (as of query time)",
    "closed": "<int> PRs closed without merge (as of query time)",
    "avg_merge_days": "<float> average days from creation to merge, 1 decimal",
    "top_contributor": "<str> login of user who opened the most PRs"
  },
  "issue": {
    "total": "<int> total issues created in period",
    "bug": "<int> issues with a label containing 'bug'",
    "resolved_bugs": "<int> bug issues that were closed during the period"
  }
}
```

## Computation Notes

### avg_merge_days

1. Filter to merged PRs only.
2. For each: `(mergedAt - createdAt)` in fractional days.
3. Average all values, round to 1 decimal place.
4. If no PRs were merged, use `0.0`.

### top_contributor

- Count PRs per `author.login`.
- If there is a tie, pick the one that appears first alphabetically (or as the requester specifies).

### resolved_bugs (closed during the month)

- Filter issues to those with at least one label containing `bug`.
- Among those, count the ones whose `closedAt` timestamp falls within the report period.

## Output

Write the JSON to the specified path using `Write` tool or `jq`. Ensure numeric types are correct (integers for counts, float for avg_merge_days).
