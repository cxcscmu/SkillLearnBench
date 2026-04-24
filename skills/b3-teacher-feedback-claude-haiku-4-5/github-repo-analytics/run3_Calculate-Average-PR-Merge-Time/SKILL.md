---
name: Calculate Average PR Merge Time
description: Compute the average number of days from PR creation to merge for all merged PRs in December 2024, using correct timestamp parsing and filtering.
---

# Calculate Average PR Merge Time

## Overview
Calculate the average time-to-merge in days (rounded to 1 decimal place) for PRs that were successfully merged during December 2024.

## Step 1: Filter Merged PRs Only
From the PR query results, identify only PRs where:
- `mergedAt` is NOT null
- `state` equals `"MERGED"` (verify this is the actual state value)

Do NOT include closed-but-unmerged or open PRs in this calculation.

## Step 2: Parse Timestamps Correctly
For each merged PR, extract:
- `createdAt`: The PR creation timestamp (ISO-8601 format, e.g., `2024-12-15T10:30:45Z`)
- `mergedAt`: The PR merge timestamp (ISO-8601 format)

**Critical:** Use the **creation date** as the start point, not any other date field.

## Step 3: Convert to Days
For each PR:
1. Parse both timestamps as datetime objects (handle timezone info — typically UTC)
2. Calculate the difference: `mergedAt - createdAt`
3. Convert to total days (may be a float with decimal)
4. Example: If a PR was created on 2024-12-01 at 00:00:00 and merged on 2024-12-02 at 12:00:00, that's 1.5 days

## Step 4: Compute Average
- Sum all day values from step 3
- Divide by the count of merged PRs
- Round the result to exactly 1 decimal place (e.g., 1.2, 15.8, 0.5)

## Step 5: Validation Check
If your average is significantly higher than expected (e.g., 16+ days):
- Verify you're only including merged PRs (check `mergedAt != null`)
- Confirm you're measuring from `createdAt` (not some other field)
- Check if any timestamp parsing errors are inflating the values
- Inspect a few sample PRs manually to spot-check the calculation

## Example Pseudocode
```
merged_prs = [pr for pr in prs if pr.mergedAt is not null and pr.state == "MERGED"]
days_list = []
for pr in merged_prs:
  created = parse_datetime(pr.createdAt)
  merged = parse_datetime(pr.mergedAt)
  days = (merged - created).total_seconds() / 86400
  days_list.append(days)
avg = sum(days_list) / len(days_list)
rounded_avg = round(avg, 1)
```