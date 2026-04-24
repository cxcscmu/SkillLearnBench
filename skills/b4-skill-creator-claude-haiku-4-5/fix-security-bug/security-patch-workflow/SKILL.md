---
name: security-patch-workflow
description: How to create, apply, and verify security patches for git repositories. Use this skill when creating patches from code changes, applying patches to source code, or validating that patches correctly address vulnerabilities.
---

# Security Patch Workflow

## Overview

Security patches are created as unified diff files that can be transported and applied to source code repositories. This workflow covers creating patches from changes and applying them to Druid or other git repositories.

## Creating Patches

### Method 1: Creating Patch from Uncommitted Changes

If you've edited files directly:

```bash
cd /root/druid
git diff > /root/patches/fix-vulnerability.patch
```

### Method 2: Creating Patch from Committed Changes

If changes are already committed:

```bash
cd /root/druid
git format-patch -1 HEAD -o /root/patches/
```

This creates a patch file named like `0001-fix-vulnerability.patch`

### Method 3: Creating Patch from Multiple Commits

```bash
cd /root/druid
git format-patch HEAD~3..HEAD -o /root/patches/
```

Creates patches for the last 3 commits.

## Understanding Patch File Format

A unified diff patch file contains:
- File paths with `a/` and `b/` prefixes
- Hunk headers showing line numbers
- Lines prefixed with `-` (removed), `+` (added), or ` ` (context)

Example:
```diff
--- a/src/main/java/org/apache/druid/query/filter/JavaScriptFilter.java
+++ b/src/main/java/org/apache/druid/query/filter/JavaScriptFilter.java
@@ -45,6 +45,12 @@
     public void init() {
         // initialization code
+        // Add validation for filter specification
+        if (filterSpec.containsKey("")) {
+            throw new IllegalArgumentException(
+                "Invalid filter specification: contains empty keys");
+        }
     }
```

## Applying Patches

### Method 1: Using `git apply`

Non-interactive application, good for automation:

```bash
cd /root/druid
git apply /root/patches/fix-vulnerability.patch
```

### Method 2: Using `git am` (Recommended for Commits)

If the patch was created with `git format-patch`:

```bash
cd /root/druid
git am /root/patches/0001-fix-vulnerability.patch
```

### Method 3: Using `patch` Command

Direct application with the `patch` utility:

```bash
cd /root/druid
patch -p1 < /root/patches/fix-vulnerability.patch
```

## Verifying Patch Application

After applying a patch, verify:

### 1. Check Git Status
```bash
cd /root/druid
git status
```

You should see modified files (if using `git apply`) or new commits (if using `git am`).

### 2. Review Changed Files
```bash
cd /root/druid
git diff HEAD~1..HEAD  # if patch was committed
# or
git diff              # if patch was applied but not committed
```

### 3. Verify Specific Fixes
Look for:
- Expected files were modified
- Validation logic was added
- Security checks are in place
- No unintended changes

## Handling Patch Conflicts

If a patch doesn't apply cleanly:

```bash
cd /root/druid
git apply --reject /root/patches/fix-vulnerability.patch
```

This creates `.rej` files showing conflicts. Manually merge them:

```bash
# View the .rej files
find . -name "*.rej" -exec cat {} \;

# Manually fix the conflicts in the source files
# Then remove the .rej files
find . -name "*.rej" -delete

# Apply remaining patches
git add .
git commit -m "Apply security patch (manual resolution)"
```

## Patch Best Practices

1. **Minimal changes:** Patches should contain only the necessary fixes
2. **Clear context:** Include sufficient context lines for reliable application
3. **No unrelated changes:** Don't mix security fixes with refactoring
4. **Test before patching:** Verify the original code builds and runs
5. **Test after patching:** Verify the patched code builds and runs correctly
6. **Document the patch:** Include a description of the vulnerability and fix

## Creating a Patch Series

For multiple related patches:

```bash
# Create numbered patches
git format-patch -3 -o /root/patches/

# List them
ls /root/patches/*.patch

# Apply all in order
cd /root/druid
git am /root/patches/*.patch
```

## Validating Patch Content

Before applying, review the patch to ensure it's legitimate:

```bash
cat /root/patches/fix-vulnerability.patch | head -50
```

Check for:
- Appropriate file modifications
- No suspicious code patterns
- Clear change descriptions
- Expected syntax and structure
