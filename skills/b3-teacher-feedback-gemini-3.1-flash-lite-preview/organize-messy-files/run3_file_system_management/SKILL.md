---
name: file_system_management
description: Safely moves files into target directories while preventing collisions, handling path logic, and maintaining state.
---
To handle the file system safely:
1. **Path Normalization**: Always convert relative paths to absolute paths using `os.path.abspath` to resolve location ambiguities.
2. **Verification**: Before moving a file, check `os.path.dirname(file_path)` against the target directory to determine if the file is already organized. If it resides in the correct folder, skip the move operation to prevent errors.
3. **Collision Avoidance**: If a file with the same name already exists in the target folder, append a unique timestamp or hash to the filename before moving, or log the duplicate for manual verification.
4. **Atomic Operation**: Execute file moves using `shutil.move` within a `try-except` block to catch OS-level errors (e.g., permission issues).