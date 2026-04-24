---
name: run2_report-builder
description: How to assemble and write a structured JSON report for GitHub community pulse statistics with validation.
---

# GitHub Community Pulse Report Builder

## Report Schema
```json
{
  "pr": {
    "total": <int>,         // PRs created in the month
    "merged": <int>,        // subset: merged (pull_request.merged_at not null)
    "closed": <int>,        // subset: closed without merge
    "avg_merge_days": <float>, // average days from created_at to merged_at, 1 decimal
    "top_contributor": <str>  // login with most PRs created
  },
  "issue": {
    "total": <int>,          // issues created in the month
    "bug": <int>,            // issues with label containing "bug"
    "resolved_bugs": <int>   // bug issues closed within the month
  }
}
```

## Validation Checks
```python
def validate_report(report, prs, issues):
    pr = report["pr"]
    iss = report["issue"]
    # Merged + closed + open should equal total
    assert pr["merged"] + pr["closed"] <= pr["total"], "merged+closed exceeds total"
    # Bug count cannot exceed total issues
    assert iss["bug"] <= iss["total"], "bug > total issues"
    # Resolved bugs cannot exceed bug count
    assert iss["resolved_bugs"] <= iss["bug"], "resolved_bugs > bug"
    # avg_merge_days should be positive
    assert pr["avg_merge_days"] >= 0, "negative avg_merge_days"
```

## Writing the Report
```python
import json

def write_report(path, report):
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report written to {path}")
    print(json.dumps(report, indent=2))
```

## Full Assembly
```python
report = {
    "pr": {
        "total": len(prs),
        "merged": len(merged_prs),
        "closed": len(closed_prs),
        "avg_merge_days": compute_avg_merge_days(merged_prs),
        "top_contributor": get_top_contributor(prs)
    },
    "issue": {
        "total": len(issues),
        "bug": len(bug_issues),
        "resolved_bugs": len(resolved_bugs)
    }
}
validate_report(report, prs, issues)
write_report("/app/report.json", report)
```
