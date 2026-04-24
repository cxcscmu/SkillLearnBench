---
name: copy-files-and-create-directories
description: Use when you need to create output directory structures and copy files into them for web app deployment.
---

# Copying Files and Creating Directories

```python
import os
import shutil

# Create directory tree
os.makedirs('/root/output/data/', exist_ok=True)
os.makedirs('/root/output/js/', exist_ok=True)
os.makedirs('/root/output/css/', exist_ok=True)

# Copy a single file
shutil.copy('/root/data/stock-descriptions.csv', '/root/output/data/stock-descriptions.csv')

# Copy entire directory
shutil.copytree('/root/data/indiv-stock/', '/root/output/data/indiv-stock/')

# Copy with overwrite (Python 3.8+)
shutil.copytree('/root/data/indiv-stock/', '/root/output/data/indiv-stock/',
                dirs_exist_ok=True)

# Copy all CSV files from a directory
import glob
for f in glob.glob('/root/data/indiv-stock/*.csv'):
    shutil.copy(f, '/root/output/data/indiv-stock/')
```