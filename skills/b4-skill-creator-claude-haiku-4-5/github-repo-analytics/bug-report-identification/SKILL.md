---
name: bug-report-identification
description: Identify bug reports by checking if any issue label contains the substring "bug" (case-insensitive matching). Use this skill when categorizing GitHub issues as bugs vs. features, filtering defects, or generating quality/reliability metrics.
---

# Bug Report Identification

Identify issues classified as bug reports based on label analysis.

## Definition

A **bug report** is any issue where at least one label contains the substring `"bug"` (case-insensitive).

**Examples of matching labels:**
- `bug`
- `type: bug`
- `kind/bug`
- `bug-regression`
- `BUGFIX` (case-insensitive)
- `p1-bug`

**Non-matching labels:**
- `feature`
- `documentation`
- `enhancement`

## Algorithm

For each issue:
1. Extract the `labels` array (list of label objects with `name` field)
2. For each label, check if `"bug"` is a substring of the lowercased label name
3. If any label matches, mark the issue as a bug report
4. Count total bug reports and track which were closed during a specified period

## Implementation (Python)

```python
def is_bug_report(issue: Dict) -> bool:
    """
    Args:
        issue: Issue object from GitHub API with 'labels' field

    Returns:
        True if any label contains "bug" (case-insensitive)
    """
    labels = issue.get('labels', [])
    return any('bug' in label['name'].lower() for label in labels)


def count_bug_reports(issues: List[Dict]) -> int:
    """Count total issues classified as bug reports"""
    return sum(1 for issue in issues if is_bug_report(issue))


def count_closed_bugs(issues: List[Dict], closed_during: str = None) -> int:
    """
    Count bug reports that are closed.

    Args:
        issues: List of issue objects
        closed_during: Optional date range to filter (e.g., "2024-12-01..2024-12-31")
                      If None, counts all closed bugs regardless of close date

    Returns:
        Count of closed bug issues
    """
    closed_bugs = []

    for issue in issues:
        if not is_bug_report(issue):
            continue

        if issue['state'] != 'CLOSED':
            continue

        # If no date filter, include
        if closed_during is None:
            closed_bugs.append(issue)
            continue

        # If date filter provided, check closedAt
        closed_at = issue.get('closedAt')
        if closed_at:
            # Parse and compare (implementation depends on date range format)
            closed_bugs.append(issue)

    return len(closed_bugs)
```

## Implementation (Bash with jq)

```bash
# Count total bug reports
jq '[.[] | select(.labels[].name | ascii_downcase | contains("bug"))] | length' issues.json

# Count closed bug reports
jq '[.[] | select(.labels[].name | ascii_downcase | contains("bug")) | select(.state == "CLOSED")] | length' issues.json
```

## Edge Cases

- **No labels**: Issue has empty `labels` array → not a bug report
- **Multiple bug-related labels**: Count as one bug report (not multiple)
- **Label name case variation**: Always normalize to lowercase for matching
- **Compound labels**: Labels like `type: bug` correctly match (substring match)

## Verification Steps

1. Manually inspect 5-10 issues marked as bugs and confirm they have relevant labels
2. Spot-check 2-3 non-bugs to ensure they're excluded
3. Count total bugs and closed bugs separately
4. Ensure counts don't exceed total issue count

## Special Note on Date Filtering

If filtering closed bugs by date (e.g., "issues created in December, but closed when?"):
- **Created during period but closed anytime**: No date filter on `closedAt`
- **Closed during the same period**: Compare `closedAt` against the same date range as creation

This skill provides the counting logic; the caller should specify which date comparison to use based on the metric definition.
