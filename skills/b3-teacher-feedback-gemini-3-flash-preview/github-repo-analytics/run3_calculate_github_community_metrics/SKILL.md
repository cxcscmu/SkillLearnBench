---
name: calculate_github_community_metrics
description: Processes JSON data from GitHub Search results to compute specific repository health metrics including average merge time, top contributors, and bug resolution counts.
---

When calculating metrics from the JSON output of a paginated GitHub Search API call, use the following logic patterns:

### PR Metrics
- **Merged Count**: Filter items where `merged_at != null`.
- **Closed Count**: Filter items where `state == "closed"` and `merged_at == null`.
- **Average Merge Days**: 
  - Filter for merged PRs.
  - Calculate the difference between `merged_at` and `created_at` using `( (.merged_at | fromdateiso8601) - (.created_at | fromdateiso8601) ) / 86400`.
  - Use `add / length` to find the average and `round` or multiplication/division logic for decimal precision.
- **Top Contributor**: Use `group_by(.user.login)`, sort by group length, and select the login of the last group.

### Issue Metrics
- **Bug Identification**: Use a case-insensitive check for the substring "bug" within any of the issue's labels. Logic: `.labels[].name | ascii_downcase | contains("bug")`.
- **Resolved Bugs**: To accurately report bugs resolved *during* a month, query for issues closed in that period (`closed:YYYY-MM-DD..YYYY-MM-DD`) and then filter the results for labels containing "bug".

### JQ Integration Example
To compute average merge time to one decimal place:
```bash
jq '[.[] | select(.merged_at != null) | ((.merged_at | fromdateiso8601) - (.created_at | fromdateiso8601)) / 86400] | (add / length * 10 | round / 10)' input.json
```

To identify the user who opened the most PRs:
```bash
jq -r 'group_by(.user.login) | sort_by(length) | last | .[0].user.login' input.json
```