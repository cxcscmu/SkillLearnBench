---
name: gh-cli-pr-stats
description: Computing pull request statistics (merge time, top contributors) from gh CLI JSON output using jq.
---

# PR Statistics from gh CLI Output

## Fetching PR Data with Timestamps

```bash
gh pr list --repo owner/repo --state all \
  --search "created:2024-12-01..2024-12-31" \
  --limit 500 \
  --json number,state,author,createdAt,mergedAt
```

The `author` field returns an object: `{"login": "username"}`.
The `state` field returns: `OPEN`, `CLOSED`, or `MERGED`.

## Computing Average Merge Time with jq

```bash
# Filter merged PRs and compute average days to merge
echo "$pr_json" | jq '
  [.[] | select(.state == "MERGED") |
    { created: (.createdAt | fromdateiso8601),
      merged: (.mergedAt | fromdateiso8601) } |
    (.merged - .created) / 86400
  ] | add / length
'
```

- `fromdateiso8601` converts ISO 8601 strings to Unix epoch seconds.
- Divide difference by 86400 to get days.
- `add / length` computes the mean.

## Finding Top Contributor

```bash
echo "$pr_json" | jq '
  group_by(.author.login) |
  map({login: .[0].author.login, count: length}) |
  sort_by(-.count) |
  .[0]
'
```

## Counting by State

```bash
echo "$pr_json" | jq '{
  total: length,
  merged: [.[] | select(.state == "MERGED")] | length,
  closed: [.[] | select(.state == "CLOSED")] | length
}'
```

Note: In `gh` CLI output, `CLOSED` and `MERGED` are distinct states. A merged PR has state `MERGED`, not `CLOSED`.
