---
name: Query GitHub PRs for December Activity
description: Fetch all pull requests created in December 2024 from cli/cli repository using the GitHub CLI, applying correct date range filtering to ensure accurate total count and contributor identification.
---

# Query GitHub PRs for December Activity

## Overview
Use `gh pr list` with proper date range syntax to retrieve all PRs created between 2024-12-01 and 2024-12-31 in the `cli/cli` repository.

## Step 1: Test the Search Syntax
First, verify the correct syntax for date range filtering with `gh pr list`:

```bash
gh pr list \
  --repo cli/cli \
  --state all \
  --search "created:2024-12-01..2024-12-31" \
  --json number,title,author,createdAt,mergedAt,closedAt,state \
  --limit 200
```

**Critical Notes:**
- `gh pr list` may NOT support `--search` flag directly — check `gh pr list --help`
- If `--search` doesn't work, you may need to use `gh api graphql` instead for complex date filtering
- Test this command **locally first** to confirm it returns results before using in scripts
- The date format `YYYY-MM-DD` should be ISO-8601 compatible
- Increase `--limit` if you expect more than 200 PRs

## Step 2: Verify Output Fields
Ensure the JSON output contains:
- `number`: PR identifier
- `author`: Object with `login` field (for top contributor)
- `createdAt`: ISO-8601 timestamp (for date range filtering)
- `mergedAt`: ISO-8601 timestamp or null (indicates merge status)
- `closedAt`: ISO-8601 timestamp or null
- `state`: Should be `MERGED`, `CLOSED`, or `OPEN` (verify actual values)

## Step 3: Parse and Count
From the returned JSON:
- Count total number of records returned
- Count records where `state == "MERGED"` (do NOT use mergedAt != null alone)
- Count records where `state == "CLOSED"` (and mergedAt == null to exclude merged PRs)
- Extract author login and count occurrences to find top contributor

## Troubleshooting
- If counts are still too high, check if `--search` is including PRs outside the date range
- Verify state values are exactly as expected (case-sensitive)
- Consider using GraphQL query if CLI flags prove unreliable