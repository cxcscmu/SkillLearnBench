---
name: batch-organizer
description: Efficiently organizes large numbers of files into directories.
---

# Batch Organizer Skill

This skill provides methods for safely and efficiently moving many files into a structured directory hierarchy.

## Best Practices

1.  **Directory Creation:** Ensure destination directories exist before moving.
    ```bash
    mkdir -p subject_folder
    ```
2.  **Safe Moving:** Use `mv` and verify the destination.
3.  **Validation:** After moving, count the files to ensure none were lost.
    ```bash
    ls -1 source_dir | wc -l
    ls -1 dest_dir_1 dest_dir_2 ... | wc -l
    ```

## Pattern for Automation
1.  Iterate through a list of file-to-category mappings.
2.  Perform the move for each file.
3.  Log any errors for manual review.
