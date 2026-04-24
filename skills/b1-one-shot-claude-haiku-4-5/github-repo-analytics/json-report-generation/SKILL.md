---
name: json-report-generation
description: Generate and write structured JSON reports with proper formatting and validation.
---

# JSON Report Generation Skill

## Overview
Create, validate, and write JSON reports with proper formatting and schema verification.

## Basic Report Structure

```json
{
  "pr": {
    "total": 0,
    "merged": 0,
    "closed": 0,
    "avg_merge_days": 0.0,
    "top_contributor": "username"
  },
  "issue": {
    "total": 0,
    "bug": 0,
    "resolved_bugs": 0
  }
}
```

## Field Specifications
- `pr.total`: Integer count of all PRs created during period
- `pr.merged`: Integer count of merged PRs (as of report date)
- `pr.closed`: Integer count of closed (non-merged) PRs
- `pr.avg_merge_days`: Float rounded to 1 decimal place
- `pr.top_contributor`: String username of author with most PRs
- `issue.total`: Integer count of all issues created during period
- `issue.bug`: Integer count of issues with 'bug' in any label
- `issue.resolved_bugs`: Integer count of bug issues that were closed

## Python Implementation

### Basic Write
```python
import json

report = {
    "pr": {
        "total": 125,
        "merged": 95,
        "closed": 20,
        "avg_merge_days": 3.2,
        "top_contributor": "alice"
    },
    "issue": {
        "total": 45,
        "bug": 18,
        "resolved_bugs": 12
    }
}

with open('/app/report.json', 'w') as f:
    json.dump(report, f, indent=2)
```

### With Validation
```python
import json

def validate_report(report):
    """Validate report structure and types"""
    required_keys = {'pr', 'issue'}
    pr_keys = {'total', 'merged', 'closed', 'avg_merge_days', 'top_contributor'}
    issue_keys = {'total', 'bug', 'resolved_bugs'}

    assert set(report.keys()) == required_keys, "Missing top-level keys"
    assert set(report['pr'].keys()) == pr_keys, "Missing PR keys"
    assert set(report['issue'].keys()) == issue_keys, "Missing issue keys"

    assert isinstance(report['pr']['total'], int), "PR total must be int"
    assert isinstance(report['pr']['merged'], int), "PR merged must be int"
    assert isinstance(report['pr']['closed'], int), "PR closed must be int"
    assert isinstance(report['pr']['avg_merge_days'], (int, float)), "avg_merge_days must be numeric"
    assert isinstance(report['pr']['top_contributor'], str), "top_contributor must be string"

    assert isinstance(report['issue']['total'], int), "Issue total must be int"
    assert isinstance(report['issue']['bug'], int), "Issue bug count must be int"
    assert isinstance(report['issue']['resolved_bugs'], int), "resolved_bugs must be int"

    return True

def write_report(report, filepath):
    """Write and validate report"""
    validate_report(report)
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Report written to {filepath}")
```

### Pretty Printing for Review
```python
import json

def print_report(report):
    """Pretty print report for verification"""
    print("=" * 60)
    print("DECEMBER 2024 - CLI/CLI REPOSITORY PULSE")
    print("=" * 60)
    print("\nPull Requests:")
    print(f"  Total Created:    {report['pr']['total']}")
    print(f"  Merged:           {report['pr']['merged']}")
    print(f"  Closed (unmerged):{report['pr']['closed']}")
    print(f"  Avg Merge Time:   {report['pr']['avg_merge_days']} days")
    print(f"  Top Contributor:  {report['pr']['top_contributor']}")
    print("\nIssues:")
    print(f"  Total Created:    {report['issue']['total']}")
    print(f"  Bug Reports:      {report['issue']['bug']}")
    print(f"  Resolved Bugs:    {report['issue']['resolved_bugs']}")
    print("=" * 60)
```

## Output Tips
- Use `indent=2` for readable JSON formatting
- Always validate before writing
- Include file path in success message
- Consider adding a timestamp or metadata (optional)

## Bash Alternative (not recommended)
```bash
# Using jq to construct JSON (complex and error-prone)
jq -n \
  --arg total "125" \
  --arg merged "95" \
  --arg closed "20" \
  --arg avg "3.2" \
  --arg contributor "alice" \
  '{
    pr: {total: ($total | tonumber), merged: ($merged | tonumber), closed: ($closed | tonumber), avg_merge_days: ($avg | tonumber), top_contributor: $contributor},
    issue: {total: 45, bug: 18, resolved_bugs: 12}
  }'
```
