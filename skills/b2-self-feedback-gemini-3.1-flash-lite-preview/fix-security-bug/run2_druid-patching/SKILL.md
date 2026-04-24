---
name: run2_druid-patching
description: Improved skill for creating and applying robust patches to the Druid source code, including verification steps.
---

# Druid Patching Skill

## Creating a Patch
Ensure the repository is clean before starting. Make changes, then create the patch:
```bash
cd /root/druid
# Verify changes
git status
# Create patch file
git diff > /root/patches/fix-vulnerability.patch
```

## Applying a Patch
Use `git apply --check` to dry-run the patch before applying.
```bash
cd /root/druid
# Dry-run
git apply --check /root/patches/fix-vulnerability.patch
# Apply
git apply /root/patches/fix-vulnerability.patch
```
