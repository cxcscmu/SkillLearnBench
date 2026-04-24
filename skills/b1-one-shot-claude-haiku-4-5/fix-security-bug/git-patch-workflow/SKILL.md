---
name: git-patch-workflow
description: Creating, managing, and applying unified diff patches with Git for source code modifications.
---

# Git Patch Workflow

## Creating Patch Files

### Method 1: From Unstaged Changes
```bash
cd /path/to/repo
git diff path/to/file.java > /path/to/patch/fix.patch
```

### Method 2: From Staged Changes
```bash
git diff --cached > /path/to/patch/fix.patch
```

### Method 3: From Commits
```bash
# Create patch from last N commits
git format-patch -N HEAD

# Create patch from specific commit
git show COMMIT_HASH > /path/to/patch/fix.patch
```

## Patch File Structure

A unified diff patch looks like:
```
--- a/original/path/file.java
+++ b/modified/path/file.java
@@ -10,5 +10,6 @@ class MyClass {
     // context line
-    old code here
+    new code here
     // context line
```

Key components:
- `---` prefix: original file
- `+++` prefix: modified file
- `@@` markers: line numbers and context
- `-` prefix: removed lines
- `+` prefix: added lines
- No prefix: context lines

## Applying Patches

### Basic Application
```bash
cd /path/to/repo
patch -p1 < /path/to/patch/fix.patch
```

### With Error Handling
```bash
# Dry-run to test application
patch -p1 --dry-run < /path/to/patch/fix.patch

# Apply with strict checking
patch -p1 < /path/to/patch/fix.patch

# Apply with less strict checking
patch -p0 < /path/to/patch/fix.patch
```

## Best Practices

1. **Use Git Format**: Create patches via `git diff` or `git format-patch` for consistency
2. **Include Context**: Ensure adequate context lines (3+ lines around changes)
3. **Test Patches**: Always dry-run before applying to ensure compatibility
4. **Modular Patches**: Create separate patches for logically independent changes
5. **Clear Names**: Name patches descriptively (e.g., `fix-javascript-security-bypass.patch`)
6. **Document Changes**: Include explanation of what the patch fixes

## Verifying Application

```bash
# Check if patch was applied
git status
git diff HEAD

# Verify specific file was patched
git show HEAD:path/to/file.java | grep "your fix"
```

## Multiple Patches

For multiple related patches:
```bash
# Create patches in order
git diff HEAD~2 HEAD~1 > patch1.patch
git diff HEAD~1 HEAD > patch2.patch

# Apply in sequence
patch -p1 < patch1.patch
patch -p1 < patch2.patch
```
