---
name: json-data-analysis
description: Patterns for analyzing and outputting structured JSON answers from enterprise data queries.
---

# JSON Data Analysis and Output

## Output Format
When answering questions from enterprise data, use this standard format:
```json
{
  "q1": {"answer": ["item1", "item2"], "tokens": 123},
  "q2": {"answer": ["item1"], "tokens": 456}
}
```

## Key Rules
- Every answer is a list, even single items
- Token counts are numeric values (not strings)
- Employee IDs are strings like "eid_abc123"
- URLs are full strings including protocol

## Python Verification
```python
import json
with open('answer.json') as f:
    data = json.load(f)
for k, v in data.items():
    assert isinstance(v['answer'], list)
    assert isinstance(v['tokens'], (int, float))
```
