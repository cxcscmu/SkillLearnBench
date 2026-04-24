---
name: batch-file-organizer
description: Organize large collections of files into categorized folders. Use this skill when you need to move or copy 100+ files into multiple destination folders based on classification data. Handles PDF, DOCX, PPTX and other file types while preserving original filenames and content.
---

# Batch File Organizer

## Overview

This skill provides a systematic approach to organizing large numbers of files into multiple destination folders based on a classification mapping. It ensures all files are processed, no files are lost, and original content/names are preserved.

## Key Principles

1. **Non-destructive**: Never modify file content or names
2. **Complete coverage**: Every file must be assigned to exactly one destination folder
3. **Verification**: Track which files have been moved to prevent duplicates or omissions
4. **Efficiency**: Use batch operations to handle hundreds of files

## Process Workflow

### Phase 1: Preparation
1. Create all destination folders if they don't exist
2. Verify write permissions to destination directories
3. Create a manifest file tracking all source files
4. Document the classification mapping (source file → destination folder)

### Phase 2: Migration
1. Process files in batches to prevent overwhelming the system
2. Use move (not copy) operations to save space
3. Verify each file arrives at destination
4. Log any failures for manual intervention

### Phase 3: Verification
1. Count files in each destination folder
2. Compare against classification manifest
3. Confirm no files remain in source directory
4. Verify no files are corrupt or missing

## Implementation Details

### Destination Folder Structure
```
/root/LLM/
/root/trapped_ion_and_qc/
/root/black_hole/
/root/DNA/
/root/music_history/
```

### Classification Mapping Format
Create a mapping that associates each source file with a destination folder:
```
filename1.pdf → LLM
filename2.pdf → trapped_ion_and_qc
filename3.docx → black_hole
filename4.pptx → DNA
filename5.pdf → music_history
```

### Batch Processing
- Process 10-20 files at a time to allow for verification
- After each batch, verify destination folders received the files
- Log any errors and retry failed files

## Error Handling

**File already exists in destination**: Skip or rename with timestamp suffix
**Permission denied**: Report and request elevated privileges
**File in use**: Wait briefly and retry
**Corrupted file**: Log and continue; flag for manual review

## Verification Commands

After organizing:
```bash
ls -la /root/LLM/ | wc -l
ls -la /root/trapped_ion_and_qc/ | wc -l
ls -la /root/black_hole/ | wc -l
ls -la /root/DNA/ | wc -l
ls -la /root/music_history/ | wc -l
```

Compare totals against original file count to ensure complete migration.

## Special Considerations

- **Symlinks**: If symlinks are encountered, move the actual file, not the link
- **Hidden files**: Include hidden files in the migration if they match classification
- **Case sensitivity**: Be aware of case-sensitive filenames in Linux
- **File extensions**: Preserve original extensions even if unexpected (e.g., .txt files should be classified by content, not extension)
