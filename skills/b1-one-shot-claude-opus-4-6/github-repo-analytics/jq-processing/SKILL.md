---
name: jq-processing
description: Using jq to parse, filter, and aggregate JSON data from CLI tools for generating reports.
---

# jq for JSON Processing

## Basics
- `jq '.'` - pretty-print JSON
- `jq '.field'` - extract a field
- `jq 'length'` - count array elements
- `jq '[.[] | select(.cond)]'` - filter arrays

## Date Handling
```bash
# Parse ISO 8601 date to epoch
echo '"2024-12-15T10:30:00Z"' | jq 'fromdateiso8601'

# Compute difference in days between two dates
jq -n '("2024-12-20T00:00:00Z" | fromdateiso8601) - ("2024-12-15T00:00:00Z" | fromdateiso8601) | . / 86400'
# Output: 5
```

## Rounding
```bash
# Round to 1 decimal place
jq -n '3.14159 * 10 | round / 10'
# Output: 3.1
```

## Building Final JSON
```bash
jq -n \
  --argjson pr_total 50 \
  --argjson pr_merged 40 \
  --arg top "user1" \
  '{
    pr: { total: $pr_total, merged: $pr_merged, top_contributor: $top }
  }'
```

## Label Matching (substring check)
```bash
# Check if any label name contains "bug" (case-insensitive)
echo "$issues_json" | jq '
  [.[] | select(.labels | any(.name | test("bug"; "i")))]
'
```
