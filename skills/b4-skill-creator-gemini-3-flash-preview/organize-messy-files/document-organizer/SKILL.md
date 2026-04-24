name: document-organizer
description: Safely and efficiently organizes a collection of academic papers and documents into a specified directory structure. Use this skill when moving over 100 files into categorized folders, ensuring no files are left out or misnamed.

# Document Organizer Skill

## Workflow

### 1. Preparation
- Identify the source directory and the target subdirectories.
- Create the target subdirectories if they do not exist.
- List all files in the source directory to maintain an inventory.

### 2. Batch Processing
- Group files by their intended target category.
- Use `mv` command to move files in batches whenever possible to minimize shell calls.
- Avoid renaming or modifying files during the move.

### 3. Verification
- Verify that the total number of files in the target subdirectories matches the original inventory count.
- Ensure the source directory is empty of any papers or documents.

## Directory Structure
Target subdirectories for the current task:
- `LLM`
- `trapped_ion_and_qc`
- `black_hole`
- `DNA`
- `music_history`

## Troubleshooting
- If a file move fails, log the error and retry or investigate file permissions.
- If the file counts don't match, re-run the inventory and classification process.
