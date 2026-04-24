---
name: Scan Source Directory and Plan Organization
description: Use this skill at the start to scan the source directory, identify all files, create a processing plan, and establish the destination folder structure.
---

## When to use this skill
- At the beginning of the file organization task
- Before starting to extract content or classify files
- To set up the systematic workflow

## Source directory scanning

### Identify all supported files
```python
import os
from pathlib import Path
from collections import defaultdict

def scan_source_directory(source_path):
    supported_extensions = {'.pdf', '.pptx', '.docx'}
    files_by_type = defaultdict(list)
    total_count = 0
    
    for root, dirs, files in os.walk(source_path):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in supported_extensions:
                files_by_type[ext].append({
                    'name': file,
                    'full_path': os.path.join(root, file)
                })
                total_count += 1
    
    return files_by_type, total_count
```

### Report on file distribution
Note:
- Total PDF files
- Total PPTX files
- Total DOCX files
- Any files with unusual naming patterns (e.g., arXiv IDs)

## Create destination folder structure

### Setup 5 required folders
```python
def setup_destination_folders(base_destination_path):
    folders = [
        'LLM',
        'trapped_ion_and_qc',
        'black_hole',
        'DNA',
        'music_history'
    ]
    
    for folder in folders:
        folder_path = os.path.join(base_destination_path, folder)
        os.makedirs(folder_path, exist_ok=True)
    
    return {folder: os.path.join(base_destination_path, folder) 
            for folder in folders}
```

### Verify folder structure
Confirm all 5 folders exist and are empty before starting

## Create processing plan

### Document the workflow
1. Scan source directory → obtain file list and count
2. For each file: extract content (PDF, PPTX, or DOCX)
3. For each file: classify subject based on content
4. For each file: move to correct destination folder
5. After all files moved: verify count matches original

### Establish extraction priority
- Start with PDFs (most common for research papers)
- Then PPTX files (presentations)
- Finally DOCX files (documents)

### Track file groups
Organize processing by file type to batch similar extraction and classification tasks

## Logging setup

Create a master log file to record:
- Scan timestamp
- Total files found (by type)
- Files requiring manual review
- Processing start time