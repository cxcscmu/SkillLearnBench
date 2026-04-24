---
name: gh-search-prs-precise
description: How to accurately search for pull requests in a specific GitHub repository within a date range using the gh CLI, and correctly distinguish merged vs closed-without-merge PRs.
---

# Searching Pull Requests with `gh` CLI — Precise Filtering

## Key Pitfalls

1. **`gh search prs` may return results from forks or related repos** — always use `--repo owner/repo` flag explicitly.
2. **`--state closed` includes BOTH merged and closed-without-merge PRs** — GitHub treats merged PRs as a subset of closed PRs.
3. **Date range filtering** — use `--created "2024-12-01..2024-12-31"` to filter by creation date.
4. **Result limits** — `gh search prs` defaults to 30 results. Use `--limit 300` or higher to get all results (max ~1000).

## Getting Total PRs Created in a Date Range

```bash
gh search prs --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 --json number | jq length
```

This returns the count of all PRs created in the date range in the specified repo.

## Getting All PR Details for Processing

```bash
gh search prs --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 \
  --json number,author,state,createdAt,closedAt,mergedAt
```

- `mergedAt` — if non-empty/non-null, the PR was merged. If empty/null, it was NOT merged.
- `state` — will be `open`, `closed`, or `merged` in search results.

## Counting Merged PRs (as of today)

From the JSON output, count entries where `mergedAt` is not empty/null:

```bash
gh search prs --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 \
  --json mergedAt | jq '[.[] | select(.mergedAt != "" and .mergedAt != null)] | length'
```

## Counting Closed-Without-Merge PRs (as of today)

These are PRs where `state` is not open AND `mergedAt` is empty/null. In other words: closed but NOT merged.

```bash
gh search prs --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 \
  --json state,mergedAt | jq '[.[] | select(.state != "open" and (.mergedAt == "" or .mergedAt == null))] | length'
```

**Important**: The `closed` field in the report means "closed without merge", NOT all closed PRs.

## Computing Average Time-to-Merge (in days)

For merged PRs, compute the difference between `mergedAt` and `createdAt`:

```bash
gh search prs --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 \
  --json createdAt,mergedAt | jq '
  [.[] | select(.mergedAt != "" and .mergedAt != null) |
    (((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 86400)
  ] | if length > 0 then (add / length * 10 | round / 10) else 0 end'
```

This produces the average in days, rounded to 1 decimal place.

## Identifying Top Contributor (Most PRs Opened)

```bash
gh search prs --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 \
  --json author | jq '
  [.[] | .author.login] | group_by(.) | map({login: .[0], count: length}) |
  sort_by(-.count) | .[0].login'
```

## Alternative Approach Using `gh pr list`

If `gh search prs` is giving unexpected results, try:

```bash
gh pr list --repo cli/cli --search "created:2024-12-01..2024-12-31" --state all --limit 300 \
  --json number,author,state,createdAt,closedAt,mergedAt
```

`gh pr list` is scoped to the exact repo and won't include forks.

## Verifying Result Accuracy

Always verify that:
1. All returned PRs have `createdAt` within the expected date range
2. The repository field (if available) matches `cli/cli`
3. The count seems reasonable (check against the GitHub web UI)

```bash
# Verify date range of results
gh search prs --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 \
  --json createdAt | jq '[.[] | .createdAt] | sort | [first, last]'
```