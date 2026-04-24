---
name: compile-community-pulse-report-json
description: How to compile PR and issue statistics into a report.json file for a GitHub repository community pulse report, using jq to build the final JSON structure.
---

# Compiling a Community Pulse report.json

## Overall Workflow

1. Fetch PR data with precise repo and date scoping
2. Fetch issue data excluding PRs
3. Compute all metrics
4. Assemble into a single JSON file

## Step-by-Step Script

```bash
#!/bin/bash
set -e

REPO="cli/cli"
START="2024-12-01"
END="2024-12-31"

# --- Pull Requests ---

# Fetch all PRs created in the date range (use gh pr list for repo-scoped accuracy)
gh pr list --repo "$REPO" --search "created:${START}..${END}" --state all --limit 300 \
  --json number,author,state,createdAt,mergedAt > /tmp/prs.json

# Total PRs
PR_TOTAL=$(jq length /tmp/prs.json)

# Merged PRs (mergedAt is not null and not empty)
PR_MERGED=$(jq '[.[] | select(.mergedAt != null and .mergedAt != "")] | length' /tmp/prs.json)

# Closed without merge (state != "open" and not merged)
# Note: state for merged PRs may be "MERGED" or "merged" depending on gh version
PR_CLOSED=$(jq '[.[] | select(
  (.state == "closed" or .state == "CLOSED") and
  (.mergedAt == null or .mergedAt == "")
)] | length' /tmp/prs.json)

# Average merge time in days
AVG_MERGE=$(jq '
  [.[] | select(.mergedAt != null and .mergedAt != "") |
    (((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 86400)
  ] | if length > 0 then (add / length * 10 | round / 10) else 0 end
' /tmp/prs.json)

# Top contributor (person who opened the most PRs)
TOP_CONTRIBUTOR=$(jq -r '
  [.[] | .author.login] | group_by(.) |
  map({login: .[0], count: length}) |
  sort_by(-.count) | .[0].login
' /tmp/prs.json)

# --- Issues ---

# Fetch all issues created in the date range (gh issue list excludes PRs)
gh issue list --repo "$REPO" --search "created:${START}..${END}" --state all --limit 300 \
  --json number,labels,state,createdAt,closedAt > /tmp/issues.json

# Total issues
ISSUE_TOTAL=$(jq length /tmp/issues.json)

# Bug reports (any label containing substring "bug", case-insensitive)
BUG_COUNT=$(jq '[.[] | select(.labels | map(.name) | any(test("bug";"i")))] | length' /tmp/issues.json)

# Resolved bugs (bug reports that are currently closed)
RESOLVED_BUGS=$(jq '[.[] | select(
  (.state == "closed" or .state == "CLOSED") and
  (.labels | map(.name) | any(test("bug";"i")))
)] | length' /tmp/issues.json)

# --- Assemble JSON ---
jq -n \
  --argjson pr_total "$PR_TOTAL" \
  --argjson pr_merged "$PR_MERGED" \
  --argjson pr_closed "$PR_CLOSED" \
  --argjson avg_merge "$AVG_MERGE" \
  --arg top "$TOP_CONTRIBUTOR" \
  --argjson issue_total "$ISSUE_TOTAL" \
  --argjson bug "$BUG_COUNT" \
  --argjson resolved "$RESOLVED_BUGS" \
  '{
    pr: {
      total: $pr_total,
      merged: $pr_merged,
      closed: $pr_closed,
      avg_merge_days: $avg_merge,
      top_contributor: $top
    },
    issue: {
      total: $issue_total,
      bug: $bug,
      resolved_bugs: $resolved
    }
  }' > /app/report.json

cat /app/report.json
```

## Key Points

- **`closed` in PR section** = closed WITHOUT merge (not all closed PRs)
- **`gh issue list`** inherently excludes PRs, unlike `gh search issues`
- **`gh pr list`** is repo-scoped and won't include fork PRs
- **Bug detection** uses case-insensitive substring match on label names for "bug"
- **`avg_merge_days`** is rounded to 1 decimal place
- **`top_contributor`** is the author login who opened the most PRs in the period

## Debugging Tips

If counts seem off:
1. Check that `createdAt` dates are within range: `jq '[.[] | .createdAt] | sort' /tmp/prs.json`
2. Check for PR contamination in issues: `jq '[.[] | .url // .number]' /tmp/issues.json`
3. Verify merged detection: `jq '[.[] | {number, state, mergedAt}]' /tmp/prs.json`
4. Cross-reference totals with GitHub web UI search: `repo:cli/cli is:pr created:2024-12-01..2024-12-31`