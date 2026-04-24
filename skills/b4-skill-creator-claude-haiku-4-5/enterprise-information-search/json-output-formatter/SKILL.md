---
name: json-output-formatter
description: Format enterprise data retrieval results as JSON with token tracking. Use this skill when you need to output query results to JSON files in the format {"q1": {"answer": [...], "tokens": N}, ...}. Handles answer list formatting, token counting, and file output validation.
---

## JSON Output Format for Data Retrieval

### Output Structure
Every answer must follow this exact format:
```json
{
    "q1": {"answer": ["item1", "item2"], "tokens": 123},
    "q2": {"answer": ["item1"], "tokens": 456},
    "q3": {"answer": ["url1", "url2"], "tokens": 789}
}
```

### Rules
- `answer`: Always a list, even if only 1 item
- `tokens`: Positive numeric value (not a string)
- Questions keys: Match question identifiers (q1, q2, q3, etc.)

### Answer Formatting

**Multiple Items** (list with length > 1):
```json
"answer": ["eid_abc123", "eid_def456", "eid_ghi789"]
```

**Single Item** (still in a list):
```json
"answer": ["eid_abc123"]
```

**Empty Results**:
```json
"answer": []
```

### Token Counting

Track tokens consumed for each question:
1. Note the token count from API usage or elapsed processing
2. Store as positive integer in `tokens` field
3. Total tokens = sum of all question tokens

Python code to write output:
```python
import json

results = {
    "q1": {"answer": ["eid_1e9356f5", "eid_06cddbb3"], "tokens": 150},
    "q2": {"answer": ["eid_99835861"], "tokens": 200},
    "q3": {"answer": ["https://example.com/demo"], "tokens": 100}
}

with open('/root/answer.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Validation Checklist
- [ ] All questions answered (q1, q2, q3, ...)
- [ ] Each answer is a list
- [ ] Single items still in list format
- [ ] Token counts are positive integers
- [ ] File saved to `/root/answer.json`
- [ ] Valid JSON (test with `jq` or `python -m json.tool`)
