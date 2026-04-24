---
name: github-metrics
description: "How to calculate GitHub community pulse metrics using the `gh` CLI. Use this skill whenever the user asks for pull request metrics, issue metrics, community pulse, average merge times, top contributors, or bug reports over a specific timeframe."
---

# GitHub Community Metrics (gh-pulse)

Use this skill when you need to calculate metrics about GitHub repositories, such as PRs created, issues created, average merge times, and top contributors.

## Tools to use
You should use the `gh` CLI for querying GitHub's API.
To get raw data over a specific timeframe, you should leverage the `--search` flag with date queries.

## Fetching PR Metrics
To fetch PRs created within a month (e.g., Dec 2024), use:
```bash
gh pr list -R <owner>/<repo> --search "created:2024-12-01..2024-12-31" --state all --json number,state,createdAt,mergedAt,author --limit 1000
```
This gives you a JSON array of PR objects. You can then process this JSON using tools like `jq` or a small Python script to calculate:
- **Total**: Length of the array.
- **Merged**: Count where `state` is "MERGED" (or where `mergedAt` is not null). Note that GitHub CLI's `state` field might say `MERGED` or it might just say `CLOSED` with a `mergedAt` timestamp depending on the query, so prefer using `mergedAt` or `state`.
- **Closed**: Count where `state` is "CLOSED" and it's not merged.
- **Average Time-to-Merge**: For each merged PR, parse `createdAt` and `mergedAt` (ISO 8601), compute the difference in days, sum them up, divide by merged count. Round to one decimal.
- **Top Contributor**: Tally `author.login` of each PR, find the maximum.

## Fetching Issue Metrics
To fetch Issues created within a timeframe, use:
```bash
gh issue list -R <owner>/<repo> --search "created:2024-12-01..2024-12-31 is:issue" --state all --json number,state,labels --limit 1000
```
- **Total**: Length of the array.
- **Bugs**: Filter where at least one label's name contains "bug" (case-insensitive substring).
- **Resolved/Closed Bugs**: Of those bugs, count how many have `state` as "CLOSED".

## Best Practices
- Write a short Python script to orchestrate the `gh` calls and compute metrics. This is much more reliable and robust than attempting complex bash strings.
- Always add `--limit` large enough to capture the month's activity (e.g., `--limit 1000`).
