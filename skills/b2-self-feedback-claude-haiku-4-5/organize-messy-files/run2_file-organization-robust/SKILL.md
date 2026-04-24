---
name: run2_file-organization-robust
description: Robust file organization with verification, cleanup, and comprehensive logging
---

# File Organization Skill (Robust)

## Overview
Enterprise-grade file organization with:
1. **Folder creation** with validation
2. **Safe file movement** with verification
3. **Duplicate handling** for idempotent operations
4. **Comprehensive logging** for audit trail
5. **Cleanup** of source directory

## Implementation

```python
import os
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class OrganizationStats:
    """Statistics for organization operation"""
    total_files: int
    successfully_moved: int
    failed_moves: int
    skipped_duplicates: int
    categories_distribution: Dict[str, int]

class FileOrganizer:
    """Robust file organization with logging"""

    def __init__(self, source_dir, base_path):
        self.source_dir = Path(source_dir)
        self.base_path = Path(base_path)
        self.stats = OrganizationStats(0, 0, 0, 0, {})
        self.move_log = []

    def create_category_folders(self, categories):
        """Create target folders for each category"""
        for category in categories:
            folder_path = self.base_path / category
            folder_path.mkdir(parents=True, exist_ok=True)
            self.stats.categories_distribution[category] = 0

    def move_file_safely(self, file_path, category):
        """
        Move file with verification and duplicate detection.
        Returns: (success: bool, message: str)
        """
        file_path = Path(file_path)
        dest_folder = self.base_path / category
        dest_path = dest_folder / file_path.name

        # Skip if already at destination
        if file_path == dest_path:
            self.move_log.append(f"SKIP: {file_path.name} already in {category}")
            self.stats.skipped_duplicates += 1
            return True, f"Already in {category}"

        # Check for duplicates in destination
        if dest_path.exists():
            self.move_log.append(f"SKIP: Duplicate found: {dest_path.name}")
            self.stats.skipped_duplicates += 1
            return False, f"Duplicate exists in {category}"

        # Move file
        try:
            shutil.move(str(file_path), str(dest_path))

            # Verify move
            if dest_path.exists() and not file_path.exists():
                self.move_log.append(f"OK: {file_path.name} → {category}")
                self.stats.successfully_moved += 1
                if category not in self.stats.categories_distribution:
                    self.stats.categories_distribution[category] = 0
                self.stats.categories_distribution[category] += 1
                return True, f"Moved to {category}"
            else:
                self.move_log.append(f"FAIL: Move incomplete: {file_path.name}")
                self.stats.failed_moves += 1
                return False, "Move verification failed"

        except Exception as e:
            self.move_log.append(f"ERROR: {file_path.name} - {str(e)}")
            self.stats.failed_moves += 1
            return False, str(e)

    def organize_all(self, category_map):
        """
        Organize all files based on category map.
        category_map: Dict[file_path_str, category]
        Returns: OrganizationStats
        """
        self.stats.total_files = len(category_map)

        for file_path, category in category_map.items():
            self.move_file_safely(file_path, category)

        return self.stats

    def save_log(self, log_file):
        """Save detailed move log to file"""
        with open(log_file, 'w') as f:
            f.write("FILE ORGANIZATION LOG\n")
            f.write("=" * 70 + "\n\n")
            for entry in self.move_log:
                f.write(entry + "\n")
```

## Verification Functions

```python
def verify_organization(base_path, categories, source_dir):
    """
    Verify organization completeness.
    Returns dict with verification results.
    """
    verification = {
        'folders_exist': {},
        'total_files': 0,
        'orphaned_files': []
    }

    # Check folders
    for category in categories:
        folder = Path(base_path) / category
        verification['folders_exist'][category] = folder.exists()
        if folder.exists():
            files = list(folder.glob('*'))
            verification['total_files'] += len(files)

    # Check source is empty
    orphaned = list(Path(source_dir).glob('*'))
    if orphaned:
        verification['orphaned_files'] = [str(f) for f in orphaned]

    return verification

def cleanup_empty_source(source_dir):
    """Remove empty source directory"""
    try:
        source_path = Path(source_dir)
        if source_path.exists() and not any(source_path.iterdir()):
            source_path.rmdir()
            return True
    except:
        pass
    return False
```

## Key Improvements from Run 1
1. **Verification**: Confirms files were actually moved
2. **Duplicate detection**: Prevents overwriting existing files
3. **Comprehensive logging**: Every action logged for audit
4. **Idempotent design**: Can run multiple times safely
5. **Statistics tracking**: Detailed breakdown of results
6. **Error recovery**: Graceful handling of failures

## Usage Pattern
```python
organizer = FileOrganizer(source_dir, base_path)
organizer.create_category_folders(categories)
stats = organizer.organize_all(category_map)
organizer.save_log('organization.log')

# Verify
verification = verify_organization(base_path, categories, source_dir)
cleanup_empty_source(source_dir)
```
