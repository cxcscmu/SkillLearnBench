---
name: json-data-processing
description: Provides techniques for parsing and extracting data from JSON files in Python.
---
# JSON Data Processing in Python

## Introduction
Python's built-in `json` module is powerful for reading and writing JSON files.

## Reading JSON
```python
import json

with open('data.json', 'r') as f:
    data = json.load(f)
```

## Writing JSON
```python
with open('output.json', 'w') as f:
    json.dump(data, f, indent=4)
```
