---
name: Query GitHub Issues for December Activity
description: Fetch all issues created in December 2024 from cli/cli repository using correct date filtering, and identify bug-related issues based on label substring matching.
---

# Query GitHub Issues for December Activity

## Overview
Use `gh issue list` to retrieve all issues created between 2024-12-01 and 2024-12-31 in the `cli/cli` repository, then filter for bug-related issues.

## Step 1: Test the Issue Search Syntax
Verify the correct syntax for date range filtering with `gh issue list`:

```bash
gh issue list \
  --repo cli/cli \
  --state all \
  --search "created:2024-12-01..2024-12-31" \
  --json number,title,labels,createdAt,closedAt,state \
  --limit 200
```

**Critical Notes:**
- `gh issue list` may NOT support `--search` flag the same way as `gh api graphql`
- Test this command **locally first** to confirm it returns results
- If results are roughly 2x expected, the date filter may be malfunctioning or including unintended issues
- Verify `--limit 200` is sufficient or increase as needed
- Check that `state=all` or `state=open,closed` correctly filters the date range

## Step 2: Verify Output Fields
Ensure the JSON output contains:
- `number`: Issue identifier
- `labels`: Array of label objects with `name` field (e.g., `[{"name": "bug"}, {"name": "type: regression"}]`)
- `createdAt`: ISO-8601 timestamp
- `closedAt`: ISO-8601 timestamp or null (indicates whether issue is open)
- `state`: Should indicate `OPEN` or `CLOSED` (verify actual values)

## Step 3: Count Total Issues
Count the total number of issues returned by the query — this should be significantly lower than you may be getting (verify expected count ~30, not ~60).

## Step 4: Identify Bug Reports
For each issue, check if ANY label contains the substring `bug` (case-insensitive or case-sensitive per repo convention):
- Examples of matching labels: `bug`, `type: bug`, `kind/bug`, `bug-report`
- Examples of non-matching labels: `debugging`, `bugsquash` (must contain as word/component, not substring if repo uses strict naming)
- Count all issues with at least one matching label

**Important:** Verify the case sensitivity convention used in the `cli/cli` repo (test manually).

## Step 5: Count Resolved Bug Reports
From the bug report issues identified in step 4:
- Count only those where `closedAt` is NOT null OR `state == "CLOSED"`
- These are bug reports that were closed during the month

## Troubleshooting
- If total count is ~60 instead of ~30: The date range filter is not working correctly; test the command locally
- If bug count is ~28 instead of ~9: You may be including non-December issues or counting non-bug labels
- If resolved_bugs is ~26 instead of ~8: Check if you're only counting bugs closed in December, or all closed bugs created in December
- Consider switching to GraphQL if CLI filters prove unreliable: `gh api graphql` with explicit date range queries