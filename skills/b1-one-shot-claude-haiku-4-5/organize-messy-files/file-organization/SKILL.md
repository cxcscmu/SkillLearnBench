---
name: file-organization
description: Organize files into target directories based on classification results
---

# File Organization and Management

## Overview
Move/copy classified files into their respective subject folders with proper error handling.

## Directory Structure Setup

```python
import os
import shutil
from pathlib import Path

def create_target_folders(base_dir, folders):
    """Create target folders if they don't exist"""
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created/verified folder: {folder_path}")

# Usage
target_folders = [
    'LLM',
    'trapped_ion_and_qc',
    'black_hole',
    'DNA',
    'music_history'
]

create_target_folders('/path/to/base', target_folders)
```

## File Moving Strategy

```python
def move_file_to_folder(source_file, destination_folder):
    """Move file to destination folder, handling conflicts"""
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        filename = os.path.basename(source_file)
        dest_path = os.path.join(destination_folder, filename)

        # Handle filename conflicts
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(
                    destination_folder,
                    f"{base}_{counter}{ext}"
                )
                counter += 1

        shutil.move(source_file, dest_path)
        return True, dest_path
    except Exception as e:
        return False, str(e)

def organize_files(source_dir, classification_results, base_output_dir):
    """
    Organize files based on classification results

    Args:
        source_dir: Directory containing source files
        classification_results: Dict mapping file_path -> category
        base_output_dir: Base directory for output folders

    Returns:
        Dict with statistics about the operation
    """
    stats = {
        'total_files': len(classification_results),
        'moved': 0,
        'failed': 0,
        'errors': []
    }

    for file_path, category in classification_results.items():
        dest_folder = os.path.join(base_output_dir, category)
        success, result = move_file_to_folder(file_path, dest_folder)

        if success:
            stats['moved'] += 1
            print(f"✓ {os.path.basename(file_path)} → {category}")
        else:
            stats['failed'] += 1
            stats['errors'].append((file_path, result))
            print(f"✗ {os.path.basename(file_path)}: {result}")

    return stats
```

## Logging and Progress Tracking

```python
def log_organization_results(stats, log_file=None):
    """Log organization results to file or stdout"""
    summary = f"""
File Organization Summary
========================
Total files: {stats['total_files']}
Successfully moved: {stats['moved']}
Failed: {stats['failed']}

Failed files:
"""
    if stats['errors']:
        for file_path, error in stats['errors']:
            summary += f"  - {file_path}: {error}\n"

    print(summary)

    if log_file:
        with open(log_file, 'w') as f:
            f.write(summary)
```

## Best Practices
- Create output folders before moving files
- Handle filename conflicts (duplicates)
- Preserve original filenames
- Log all operations for verification
- Verify files don't already exist before moving
- Use proper error handling for permission issues
