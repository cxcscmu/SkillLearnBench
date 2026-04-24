---
name: write-report-json
description: Compile PR and issue metrics into a report.json file at /app/report.json using the required schema for the December community pulse write-up.
---

## Writing report.json

After computing all metrics, write the result to `/app/report.json`.

### Required JSON structure

```json
{
  "pr": {
    "total": <int>,
    "merged": <int>,
    "closed": <int>,
    "avg_merge_days": <float>,
    "top_contributor": <str>
  },
  "issue": {
    "total": <int>,
    "bug": <int>,
    "resolved_bugs": <int>
  }
}
```

### Full end-to-end script

```python
#!/usr/bin/env python3
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone

START = datetime(2024, 12, 1, tzinfo=timezone.utc)
END   = datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def in_range(dt_str):
    return START <= parse_dt(dt_str) <= END

# --- PRs ---
pr_result = subprocess.run([
    "gh", "search", "prs",
    "--repo", "cli/cli",
    "--created", "2024-12-01..2024-12-31",
    "--limit", "200",
    "--json", "number,state,createdAt,mergedAt,closedAt,author"
], capture_output=True, text=True, check=True)

all_prs = json.loads(pr_result.stdout)
prs = [pr for pr in all_prs if in_range(pr["createdAt"])]

merged_prs = [pr for pr in prs if pr.get("mergedAt")]
closed_prs = [pr for pr in prs if pr["state"].lower() == "closed" and not pr.get("mergedAt")]

if merged_prs:
    avg_merge_days = round(
        sum(
            (parse_dt(pr["mergedAt"]) - parse_dt(pr["createdAt"])).total_seconds() / 86400
            for pr in merged_prs
        ) / len(merged_prs),
        1
    )
else:
    avg_merge_days = 0.0

author_counts = Counter(
    pr["author"]["login"] for pr in prs if pr.get("author")
)
top_contributor = author_counts.most_common(1)[0][0] if author_counts else ""

# --- Issues ---
issue_result = subprocess.run([
    "gh", "search", "issues",
    "--repo", "cli/cli",
    "--created", "2024-12-01..2024-12-31",
    "--limit", "200",
    "--json", "number,state,createdAt,closedAt,labels"
], capture_output=True, text=True, check=True)

all_issues = json.loads(issue_result.stdout)
issues = [i for i in all_issues if in_range(i["createdAt"])]

def is_bug(issue):
    return any("bug" in label["name"].lower() for label in issue.get("labels", []))

bug_issues = [i for i in issues if is_bug(i)]

resolved_bugs = [
    i for i in bug_issues
    if i.get("closedAt") and in_range(i["closedAt"])
]

# --- Report ---
report = {
    "pr": {
        "total": len(prs),
        "merged": len(merged_prs),
        "closed": len(closed_prs),
        "avg_merge_days": avg_merge_days,
        "top_contributor": top_contributor
    },
    "issue": {
        "total": len(issues),
        "bug": len(bug_issues),
        "resolved_bugs": len(resolved_bugs)
    }
}

with open("/app/report.json", "w") as f:
    json.dump(report, f, indent=2)

print(json.dumps(report, indent=2))
```

### Notes
- Always post-filter by `createdAt` range even when using `gh search` with `--created`, as a safety net.
- `resolved_bugs` counts bug issues whose `closedAt` also falls within December 2024.
- `closed` PRs are those with `state == "closed"` and no `mergedAt` (i.e., not merged, just closed).