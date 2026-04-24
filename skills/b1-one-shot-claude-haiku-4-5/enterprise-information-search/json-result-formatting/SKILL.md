---
name: json-result-formatting
description: Format query results to JSON with proper structure and token tracking
---

# JSON Result Formatting

## Overview
Formatting retrieved data into standardized JSON output with answer lists and token tracking.

## Use Cases
- Writing query results to JSON files
- Formatting answers as lists regardless of count
- Tracking API token consumption
- Creating consistent output files for downstream processing

## Required Output Format
```json
{
    "q1": {"answer": ["xxx"], "tokens": 123},
    "q2": {"answer": ["xxx", "yyy"], "tokens": 456},
    "q3": {"answer": [], "tokens": 789}
}
```

## Code Examples

### Initialize Result Container
```python
import json

result = {
    "q1": {"answer": [], "tokens": 0},
    "q2": {"answer": [], "tokens": 0},
    "q3": {"answer": [], "tokens": 0}
}
```

### Add Single Answer
```python
def add_answer(result, question_key, answer_items, tokens=0):
    """Add answer as list (always list format)"""
    # Ensure answer_items is a list
    if isinstance(answer_items, str):
        answer_items = [answer_items]
    elif not isinstance(answer_items, list):
        answer_items = list(answer_items)

    result[question_key] = {
        "answer": answer_items,
        "tokens": int(tokens)
    }
    return result

# Usage
result = add_answer(result, "q1", ["eid_1e9356f5"], tokens=150)
result = add_answer(result, "q2", employee_ids_list, tokens=200)
```

### Write to JSON File
```python
import json

def write_result_file(result, filepath):
    """Write result to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(result, f, indent=4)
    print(f"Results written to {filepath}")

# Usage
write_result_file(result, '/root/answer.json')
```

### Track Token Usage (Without API)
```python
import json

# For local data processing, estimate tokens
def estimate_tokens_from_text(text):
    """Rough estimation: ~4 characters per token"""
    return len(text) // 4

# Better: track actual API usage
def track_tokens(usage_dict):
    """Track from API response"""
    if hasattr(usage_dict, 'input_tokens'):
        return usage_dict.input_tokens + usage_dict.output_tokens
    return 0
```

### Complete Result Building Flow
```python
import json

# Initialize
result = {
    "q1": {"answer": [], "tokens": 0},
    "q2": {"answer": [], "tokens": 0},
    "q3": {"answer": [], "tokens": 0}
}

# Q1: Authors and reviewers
authors = ["eid_1e9356f5"]
reviewers = ["eid_06cddbb3", "eid_99835861"]
result["q1"]["answer"] = authors + reviewers
result["q1"]["tokens"] = 150  # Estimated or tracked

# Q2: Competitor insights team members
competitor_team = ["eid_xxx", "eid_yyy"]
result["q2"]["answer"] = competitor_team
result["q2"]["tokens"] = 200

# Q3: Demo URLs
urls = ["https://example.com/demo1", "https://example.com/demo2"]
result["q3"]["answer"] = urls
result["q3"]["tokens"] = 100

# Write output
with open('/root/answer.json', 'w') as f:
    json.dump(result, f, indent=4)
```

## Best Practices

1. **Always Use Lists**
   - Single item: `["value"]` not `"value"`
   - Multiple items: `["item1", "item2"]`
   - Empty: `[]` not `null`

2. **Token Tracking**
   - For Claude API: Use `response.usage.input_tokens + response.usage.output_tokens`
   - For local processing: Track API calls made and sum their tokens
   - If no API: Use 0 or estimate conservatively

3. **Data Validation**
   ```python
   # Ensure no duplicates
   result["q1"]["answer"] = list(set(result["q1"]["answer"]))

   # Ensure proper types
   result["q2"]["tokens"] = int(result["q2"]["tokens"])
   ```

4. **Indent and Format**
   ```python
   # Always use proper formatting
   json.dump(data, f, indent=4)
   ```

## Validation Checklist
- [ ] All question keys present (q1, q2, q3)
- [ ] All answers are lists
- [ ] All token counts are integers
- [ ] No null values (use empty list [] instead)
- [ ] Output file is valid JSON
- [ ] Can be loaded with `json.load()`

## Testing Output
```python
import json

# Verify output file
with open('/root/answer.json', 'r') as f:
    data = json.load(f)

# Check structure
for q_key, q_data in data.items():
    assert "answer" in q_data
    assert "tokens" in q_data
    assert isinstance(q_data["answer"], list)
    assert isinstance(q_data["tokens"], int)
    print(f"{q_key}: {len(q_data['answer'])} items, {q_data['tokens']} tokens")
```
