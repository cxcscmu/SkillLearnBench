---
name: Track and Verify File Organization
description: Use this skill to systematically track all files before and after sorting to ensure no files are lost, duplicated, or left out during the organization process.
---

## When to use this skill
- Before starting the sorting process: scan and count all source files
- During sorting: log each file as it is processed and moved
- After sorting: verify that all files are accounted for in the destination folders
- If discrepancies are found: locate missing or misplaced files

## File tracking process

### Pre-sorting inventory
```python
import os
from pathlib import Path

def inventory_source_files(source_directory):
    file_list = []
    file_count = 0
    
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith(('.pdf', '.pptx', '.docx')):
                full_path = os.path.join(root, file)
                file_list.append({
                    'filename': file,
                    'path': full_path,
                    'size': os.path.getsize(full_path),
                    'processed': False,
                    'destination': None
                })
                file_count += 1
    
    return file_list, file_count
```

### Tracking during sorting
- Create a log file (CSV or JSON) with columns: filename, source_path, destination_folder, classification_confidence, keywords_matched
- Update the log as each file is processed
- Record any files that are difficult to classify

### Post-sorting verification
```python
def verify_sorted_files(destination_dirs, original_count):
    total_sorted = 0
    folder_counts = {}
    
    for folder_name, folder_path in destination_dirs.items():
        count = len([f for f in os.listdir(folder_path) 
                     if f.endswith(('.pdf', '.pptx', '.docx'))])
        folder_counts[folder_name] = count
        total_sorted += count
    
    if total_sorted == original_count:
        return True, folder_counts
    else:
        return False, folder_counts
```

### Verification checklist
- [ ] Original file count recorded
- [ ] Source directory fully scanned for .pdf, .pptx, .docx files
- [ ] Processing log created and updated for each file
- [ ] All files moved to destination folders
- [ ] Final count matches original count
- [ ] No files remain in source directory (except non-supported file types)
- [ ] No duplicate files in destination folders
- [ ] File names unchanged, file contents unchanged

### If discrepancies found
1. **Files missing from destinations**: Check source directory again, verify processing log
2. **Count mismatch**: Review processing log to find which files were skipped
3. **Extra files in destinations**: Verify these files were part of original inventory
4. **Duplicates**: Check if file was processed twice with different names

### Create summary report
Document:
- Total files processed
- Count per folder
- Any files requiring manual review
- Classification confidence statistics