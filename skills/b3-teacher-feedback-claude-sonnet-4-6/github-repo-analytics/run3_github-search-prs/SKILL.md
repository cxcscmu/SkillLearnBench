---
name: github-search-prs
description: Use `gh search prs` to fetch pull requests from a specific repo within a date range. Returns structured JSON for downstream processing. More reliable than `gh pr list --search` for date-range filtering.
---

## Fetching PRs with `gh search prs`

Use `gh search prs` (not `gh pr list`) for reliable date-range filtering.

### Command pattern

```bash
gh search prs \
  --repo OWNER/REPO \
  --created "YYYY-MM-DD..YYYY-MM-DD" \
  --limit 200 \
  --json number,title,state,createdAt,mergedAt,closedAt,author
```

### Key flags
- `--repo` — target repository (e.g., `cli/cli`)
- `--created "2024-12-01..2024-12-31"` — server-side date range filter
- `--limit 200` — fetch up to 200 results (adjust if needed)
- `--json` — fields to retrieve

### Post-fetch date verification (safety net)

Always filter results in Python to confirm `createdAt` is within the target range:

```python
import json, subprocess
from datetime import datetime, timezone

START = datetime(2024, 12, 1, tzinfo=timezone.utc)
END   = datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

result = subprocess.run([
    "gh", "search", "prs",
    "--repo", "cli/cli",
    "--created", "2024-12-01..2024-12-31",
    "--limit", "200",
    "--json", "number,title,state,createdAt,mergedAt,closedAt,author"
], capture_output=True, text=True, check=True)

all_prs = json.loads(result.stdout)

# Post-fetch filter — keep only items whose createdAt is in range
prs = [
    pr for pr in all_prs
    if START <= datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00")) <= END
]
```

### Computing metrics from filtered PRs

```python
from datetime import datetime, timezone

merged_prs = [pr for pr in prs if pr.get("mergedAt")]
closed_prs = [pr for pr in prs if pr["state"].lower() == "closed" and not pr.get("mergedAt")]

# Average time to merge (days)
def days_between(a, b):
    fmt = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (fmt(b) - fmt(a)).total_seconds() / 86400

if merged_prs:
    avg_merge_days = round(
        sum(days_between(pr["createdAt"], pr["mergedAt"]) for pr in merged_prs) / len(merged_prs),
        1
    )
else:
    avg_merge_days = 0.0

# Top contributor by PR count
from collections import Counter
author_counts = Counter(pr["author"]["login"] for pr in prs if pr.get("author"))
top_contributor = author_counts.most_common(1)[0][0] if author_counts else ""
```