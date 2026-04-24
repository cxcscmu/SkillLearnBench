---
name: Identify Top PR Contributor in December
description: Determine which person opened the most pull requests in December 2024 by analyzing author data from the PR query results.
---

# Identify Top PR Contributor in December

## Overview
From the complete PR query results for December 2024, find the author who opened the most PRs.

## Step 1: Extract Author Information
From each PR object in the results, extract the author's login:
- Field path: `author.login` (e.g., `"octocat"`)
- Do NOT use commit author or merge author — use the PR opener field
- Include all PRs in the December date range, regardless of merge status

## Step 2: Count Author Occurrences
Group PRs by author login and count:
- Example: `{"alice": 5, "bob": 3, "charlie": 2, ...}`
- Ensure you're counting unique authors correctly (avoid double-counting same person)

## Step 3: Identify Top Contributor
Select the author with the highest PR count.

## Step 4: Validation
If the result differs from expected (e.g., you got `'malancas'` but expected someone else):
- Verify the PR query is actually returning December-only PRs (check a few createdAt timestamps)
- Confirm author field is being parsed correctly from the JSON
- Check if any filtering or deduplication logic is inadvertently excluding valid PRs
- Manually inspect the top 5 contributors and their PR counts to identify discrepancies

## Example Pseudocode
```
author_counts = {}
for pr in prs:
  author = pr.author.login
  author_counts[author] = author_counts.get(author, 0) + 1

top_contributor = max(author_counts, key=author_counts.get)
```