---
name: json-answer-formatter
description: Format retrieval answers as a dictionary in /root/answer.json.
---

## Overview
This skill defines the format for saving the answers of retrieved data.

## Output Format
```json
{
    "q1": {"answer": ["value1", "value2"], "tokens": 123},
    "q2": {"answer": ["single_value"], "tokens": 456}
}
```

## Requirements
- `answer` field must always be a list.
- `tokens` field must be a positive numeric value.
- Store the file at `/root/answer.json`.
- When appending, read the existing file if it exists, update it, and write it back.
