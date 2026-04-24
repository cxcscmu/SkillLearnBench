---
name: github-search-issues
description: Use `gh search issues` to fetch issues from a specific repo within a date range. Returns structured JSON. More reliable than `gh issue list --search` for date-range filtering.
---

## Fetching Issues with `gh search issues`

Use `gh search issues` (not `gh issue list`) for reliable date-range filtering.

### Command pattern

```bash
gh search issues \
  --repo OWNER/REPO \
  --created "YYYY-MM-DD..YYYY-MM-DD" \
  --limit 200 \
  --json number,title,state,createdAt,closedAt,labels
```

### Key flags
- `--repo` — target repository
- `--created "2024-12-01..2024-12-31"` — server-side date range filter
- `--limit 200` — max results
- `--json` — comma-separated list of fields; include `labels` for bug detection

### Post-fetch date verification (safety net)

```python
import json, subprocess
from datetime import datetime, timezone

START = datetime(2024, 12, 1, tzinfo=timezone.utc)
END   = datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

result = subprocess.run([
    "gh", "search", "issues",
    "--repo", "cli/cli",
    "--created", "2024-12-01..2024-12-31",
    "--limit", "200",
    "--json", "number,title,state,createdAt,closedAt,labels"
], capture_output=True, text=True, check=True)

all_issues = json.loads(result.stdout)

# Post-fetch filter
issues = [
    issue for issue in all_issues
    if START <= datetime.fromisoformat(issue["createdAt"].replace("Z", "+00:00")) <= END
]
```

### Detecting bug reports

A bug report is any issue where at least one label's `name` contains the substring `bug` (case-insensitive).

```python
def is_bug(issue):
    return any("bug" in label["name"].lower() for label in issue.get("labels", []))

bug_issues = [i for i in issues if is_bug(i)]
```

### Counting resolved (closed) bugs within the month

```python
from datetime import datetime, timezone

def closed_in_month(issue):
    closed = issue.get("closedAt")
    if not closed:
        return False
    dt = datetime.fromisoformat(closed.replace("Z", "+00:00"))
    return START <= dt <= END

resolved_bugs = [i for i in bug_issues if closed_in_month(i)]
```