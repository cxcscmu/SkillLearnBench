---
name: json-data-analysis
description: Python patterns for analyzing large JSON datasets to find specific information, track tokens, and write answers in the required format.
---

# JSON Data Analysis

## Loading and Analyzing Large JSON Files
```python
import json

with open('/path/to/file.json') as f:
    data = json.load(f)
```

## Counting Tokens (Approximate)
```python
import json

def count_tokens(text):
    """Approximate token count: ~4 chars per token"""
    return len(str(text)) // 4

# Or use tiktoken for more accurate counting
# pip install tiktoken
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
tokens = len(enc.encode(str(data)))
```

## Writing Answer File
```python
import json

answers = {
    "q1": {"answer": ["emp001", "emp002"], "tokens": 150},
    "q2": {"answer": ["emp003"], "tokens": 200},
}

with open('/root/answer.json', 'w') as f:
    json.dump(answers, f, indent=4)
```

## Searching Nested Structures
```python
def deep_search(obj, keyword):
    """Recursively search for keyword in nested structure"""
    results = []
    if isinstance(obj, str):
        if keyword.lower() in obj.lower():
            results.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            results.extend(deep_search(v, keyword))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(deep_search(item, keyword))
    return results
```

## Extracting Employee IDs
```python
import re

def extract_employee_ids(text):
    """Extract employee IDs matching pattern like EMP001, E001, etc."""
    return re.findall(r'\b[A-Z]{1,3}\d{3,6}\b', text)
```
