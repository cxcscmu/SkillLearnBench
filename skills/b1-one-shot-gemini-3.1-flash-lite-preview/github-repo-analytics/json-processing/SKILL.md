---
name: json-processing
description: "Skills for processing JSON data in the CLI, primarily using `jq`."
---

# JSON Processing with `jq`

Use `jq` to parse and transform JSON data from API responses.

## Examples
- Filter and count: `cat data.json | jq 'length'`
- Group and count occurrences: `cat data.json | jq 'group_by(.author.login) | map({author: .[0].author.login, count: length})'`
- Filter for specific labels: `jq 'select(.labels[].name | contains("bug"))'`
