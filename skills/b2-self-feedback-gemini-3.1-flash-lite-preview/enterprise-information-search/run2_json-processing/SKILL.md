---
name: run2_json-processing
description: Provides advanced techniques for reading, parsing, and structured writing of JSON data, including complex filtering and aggregation.
---
# Advanced JSON Processing Skill

Use the `json` module for deep inspection of complex, nested JSON objects.

## Usage
```python
import json

def filter_nested(data, key):
    # Perform complex search in nested structures
    return [item for item in data if key in item]
```
