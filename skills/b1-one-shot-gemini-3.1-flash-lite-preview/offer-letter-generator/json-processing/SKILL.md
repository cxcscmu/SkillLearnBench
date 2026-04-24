---
name: json-processing
description: Efficiently read and parse JSON files for use in automation tasks.
---

# JSON Processing Skill

Use Python's built-in `json` module to interact with JSON data files.

## Reading JSON
```python
import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
```
