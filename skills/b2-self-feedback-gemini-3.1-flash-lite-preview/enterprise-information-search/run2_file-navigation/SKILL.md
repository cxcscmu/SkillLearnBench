---
name: run2_file-navigation
description: Efficient recursive exploration and content searching across large datasets.
---
# Advanced File Navigation Skill

Use `os.walk` or efficient `grep` piping to locate data patterns in large directory structures.

## Usage
```python
import os

def find_files(root, pattern):
    for root, dirs, files in os.walk(root):
        for file in files:
            if pattern in file:
                yield os.path.join(root, file)
```
