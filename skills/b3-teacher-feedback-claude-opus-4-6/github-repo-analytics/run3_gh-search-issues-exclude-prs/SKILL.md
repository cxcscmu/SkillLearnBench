---
name: gh-search-issues-exclude-prs
description: How to accurately search for issues (excluding pull requests) in a GitHub repository using the gh CLI, since GitHub's search API treats PRs as a type of issue.
---

# Searching Issues (Excluding PRs) with `gh` CLI

## Critical Pitfall

**GitHub's search API treats pull requests as issues.** When you use `gh search issues`, the results will include BOTH actual issues AND pull requests unless you explicitly filter them out.

This means counts from `gh search issues` will be inflated (often ~2x) if you don't exclude PRs.

## Correct Approach: Add `type:issue` Qualifier

### Method 1: Using `--` with search qualifiers

```bash
gh search issues --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 \
  -- "type:issue"
```

### Method 2: Using `gh issue list` with `--search`

This is often more reliable since `gh issue list` is inherently scoped to issues only:

```bash
gh issue list --repo cli/cli --search "created:2024-12-01..2024-12-31" --state all --limit 300 \
  --json number,labels,state,createdAt,closedAt
```

`gh issue list` should NOT return PRs, making it the safer choice.

## Counting Total Issues Created in a Date Range

```bash
gh issue list --repo cli/cli --search "created:2024-12-01..2024-12-31" --state all --limit 300 \
  --json number | jq length
```

## Counting Bug Reports

A bug report is any issue where at least one label contains the substring `bug` (case-insensitive check recommended):

```bash
gh issue list --repo cli/cli --search "created:2024-12-01..2024-12-31" --state all --limit 300 \
  --json number,labels | jq '
  [.[] | select(.labels | map(.name) | any(test("bug"; "i")))] | length'
```

This uses `test("bug"; "i")` for case-insensitive substring matching.

## Counting Resolved (Closed) Bug Reports

Bug reports that were closed (during the month or as of today — check task requirements):

```bash
gh issue list --repo cli/cli --search "created:2024-12-01..2024-12-31" --state closed --limit 300 \
  --json number,labels | jq '
  [.[] | select(.labels | map(.name) | any(test("bug"; "i")))] | length'
```

This counts issues that:
- Were created in the date range
- Are currently closed
- Have at least one label containing "bug"

## Verifying Results Exclude PRs

To double-check that no PRs snuck in:

```bash
gh issue list --repo cli/cli --search "created:2024-12-01..2024-12-31" --state all --limit 300 \
  --json number,url | jq '[.[] | select(.url | test("/pull/"))] | length'
```

If this returns 0, your results are clean. If non-zero, PRs are contaminating results and you need additional filtering.

## Alternative Verification with `gh search issues`

If you must use `gh search issues`, always add `type:issue`:

```bash
gh search issues --repo cli/cli --created "2024-12-01..2024-12-31" --limit 300 \
  --json number -- "type:issue" | jq length
```

Compare this count with the `gh issue list` approach to cross-validate.