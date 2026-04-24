---
name: run2_file_organization_and_validation
description: Safely moves files and validates the integrity of the organization process.
---

# File Organization and Validation Skill

## Process
1. **Identify**: List all files to be moved.
2. **Classify**: Map each file to exactly one target folder.
3. **Pre-check**: Ensure target folders exist.
4. **Execute**: Move files using `mv`.
5. **Post-check**:
   - Source directory should be empty.
   - Total number of files moved should match the initial count.
   - Each target folder should contain files corresponding to its subject.

## Scripting for Success
Use a Python script to automate the extraction, classification, and moving in one pass to avoid errors.

```python
import os, shutil
# Define paths
src = '/root/papers/all/'
dst_folders = ['LLM', 'trapped_ion_and_qc', 'black_hole', 'DNA', 'music_history']
# ... extraction and classification logic ...
# Move file
shutil.move(src_path, os.path.join('/root/', target_folder, filename))
```
