---
name: python-text-search
description: Techniques to find specific data points in nested Python dictionaries using recursion.
---
# Python Dictionary Search

## Introduction
When dealing with enterprise JSON, you often have deeply nested dictionaries. Finding specific keys or values requires recursion.

## Finding by Key
```python
def find_key(obj, key):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                results.append(v)
            if isinstance(v, (dict, list)):
                results.extend(find_key(v, key))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(find_key(item, key))
    return results
```
