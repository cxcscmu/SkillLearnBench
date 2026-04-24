I’m preparing a short "Q4 2024 large-PR community pulse" write-up for the `cli/cli` repository, and I want you to help me turn raw activity into a clean, meeting-ready summary.

For the period 2024-10-01 to 2024-12-31, I want you to gather the following pull request metrics for PRs that changed at least 8 files:

- Count how many such PRs were created during the period.
- Report how many of those PRs had been merged by `2025-01-01T00:00:00Z`.
- Report how many of those PRs had been closed without merge by `2025-01-01T00:00:00Z`.
- Compute the average time-to-merge in days across those PRs merged by `2025-01-01T00:00:00Z`, measured from PR creation time to merge time, rounded to one decimal place.
- Identify the person who opened the most such PRs during the period. If there is a tie, return the lexicographically smallest GitHub login.

I want you to compile everything into a `report.json` file and place it in the `/app/` directory. The JSON must use this exact structure:

```json
{
  "pr": {
    "total": <int>,
    "merged": <int>,
    "closed": <int>,
    "avg_merge_days": <float>,
    "top_contributor": <str>
  }
}
```

In the output schema, `closed` means "closed without merge by 2025-01-01T00:00:00Z".
