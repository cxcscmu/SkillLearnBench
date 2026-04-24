---
name: gh-data-retrieval
description: Retrieve pull request and issue data from GitHub repositories using the gh CLI with specific filters and JSON output for downstream processing.
---

# GitHub Data Retrieval

This skill focuses on using the `gh` CLI to efficiently fetch data for repository analysis.

## Key Commands

### Searching Pull Requests
To find PRs created in a specific timeframe:
```bash
gh search prs --repo OWNER/REPO --created "YYYY-MM-DD..YYYY-MM-DD" --json number,author,createdAt,mergedAt,state
```

### Searching Issues
To find issues created in a specific timeframe:
```bash
gh search issues --repo OWNER/REPO --created "YYYY-MM-DD..YYYY-MM-DD" --json number,labels,createdAt,closedAt,state
```

### Filtering by Labels
To find bug reports (labels containing "bug"):
```bash
gh search issues --repo OWNER/REPO --label "bug" --created "YYYY-MM-DD..YYYY-MM-DD" --json number
```

## Tips for Analysis
- Use `--limit` to ensure you get all results if there are many (default is 30).
- Use `--json` to specify only the fields you need to keep the payload small.
- Date ranges use the `YYYY-MM-DD..YYYY-MM-DD` syntax.
