---
name: list-directory-files
description: Use when you need to enumerate files in a directory, optionally filtering by extension. Returns sorted list of file paths.
---

# Listing Directory Files

```python
import os
import glob

# List all files in a directory
files = os.listdir('/root/data/indiv-stock/')
print(sorted(files))

# List with full paths by extension
csv_files = glob.glob('/root/data/indiv-stock/*.csv')
csv_files.sort()
print(csv_files)

# Walk directory recursively
for root, dirs, files in os.walk('/root/data/'):
    for f in files:
        print(os.path.join(root, f))
```

Use `glob` for pattern matching, `os.listdir` for simple enumeration.