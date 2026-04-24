---
name: gh-pr-analysis
description: >
  How to fetch and analyze pull request data from a GitHub repository for a
  given time period: counts, merge rates, average time-to-merge, and top
  contributors. Use this skill whenever the user wants PR metrics, pull request
  summaries, contributor leaderboards, or community pulse reports.
---

# PR Analysis via GitHub REST API

## Fetching PRs created in a date window

Use the `/repos/{owner}/{repo}/pulls` endpoint with `state=all` and `since`:

```python
BASE = "https://api.github.com/repos/cli/cli"

def get_prs(start_iso, end_iso, token=None):
    """Fetch all PRs created between start_iso and end_iso (ISO 8601 strings)."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    start_dt = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    end_dt   = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))

    results, page = [], 1
    while True:
        r = requests.get(f"{BASE}/pulls",
                         headers=headers,
                         params={"state": "all", "sort": "created",
                                 "direction": "desc", "per_page": 100,
                                 "page": page})
        data = r.json()
        if not data:
            break
        # Trim pages that are entirely before our window (sorted desc)
        page_items = []
        stop = False
        for pr in data:
            created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
            if created > end_dt:
                continue        # too recent
            if created < start_dt:
                stop = True     # gone past our window, no need to paginate further
                break
            page_items.append(pr)
        results.extend(page_items)
        if stop or len(data) < 100:
            break
        page += 1
    return results
```

## Key calculations

### Merged vs closed-not-merged

```python
merged = [p for p in prs if p.get("merged_at")]
# "closed" means closed without merge (GitHub convention in this report)
closed_not_merged = [p for p in prs if p["state"] == "closed" and not p.get("merged_at")]
```

### Average time-to-merge (days, 1 decimal)

```python
def ttm(pr):
    c = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
    m = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
    return (m - c).total_seconds() / 86400

avg_merge_days = round(sum(ttm(p) for p in merged) / len(merged), 1) if merged else 0.0
```

### Top contributor

```python
from collections import Counter
top_contributor = Counter(p["user"]["login"] for p in prs).most_common(1)[0][0]
```

## Gotchas

- `merged_at` is only present on the `/pulls` endpoint response, NOT on the
  `/issues` endpoint. Always use `/pulls?state=all` for PR data.
- GitHub sorts by `created` desc by default; bail out once `created_at < start`
  to avoid reading thousands of old PRs.
- Bots (e.g. `dependabot[bot]`, `github-actions[bot]`) appear as contributors;
  decide whether to include/exclude them based on context.
