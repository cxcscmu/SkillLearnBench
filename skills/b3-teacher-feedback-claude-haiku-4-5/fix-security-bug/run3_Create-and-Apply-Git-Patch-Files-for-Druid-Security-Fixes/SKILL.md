---
name: Create and Apply Git Patch Files for Druid Security Fixes
description: Generate proper git-compatible patch files that address the empty key validation and JavaScript filter disabling vulnerabilities, then apply them to the Druid 0.20.0 source repository.
---

# Creating and Applying Security Patch Files

## Patch File Structure

Each patch must be a valid git diff that can be applied with `git apply` or `patch` command.

### Patch 1: Input Validation for Empty Keys

**File:** `/root/patches/001-validate-empty-keys.patch`

Content format:
```
diff --git a/path/to/file.java b/path/to/file.java
index <old-hash>..<new-hash> 100644
--- a/path/to/file.java
+++ b/path/to/file.java
@@ <line-number>,<count> +<line-number>,<count> @@
 existing context line
-removed line
+added line
 existing context line
```

**Targets:**
- The resource handler that receives `/druid/indexer/v1/sampler` POST requests
- Inject validation before `ObjectMapper.readValue()` is called
- Add utility method to recursively check for empty keys in JSON

### Patch 2: Disable JavaScript Filters

**File:** `/root/patches/002-disable-javascript-filters.patch`

Content format:
- Modify the filter factory or deserializer to reject `"type": "javascript"`
- Add configuration property default `druid.javascript.enabled=false`
- Modify module initialization to conditionally register JavaScript filter

### Patch 3: Add Validation Utility Class (if needed)

**File:** `/root/patches/003-add-json-validator.patch`

Content format:
- New file addition in patch format
- Utility class for recursive JSON validation
- Used by Patch 1

## Application Process

```bash
# Navigate to Druid repository
cd /root/druid

# Apply patches in order
git apply /root/patches/001-validate-empty-keys.patch
git apply /root/patches/002-disable-javascript-filters.patch
git apply /root/patches/003-add-json-validator.patch

# Verify patches applied
git status
git diff HEAD~3
```

## Patch Creation from Working Code

If developing new code:
```bash
cd /root/druid

# Start with clean state
git checkout <file>

# Make security modifications to file
# (add validation code, etc.)

# Generate patch
git diff <file> > /root/patches/001-validate-empty-keys.patch

# Or with more context
git diff -U5 <file> > /root/patches/001-validate-empty-keys.patch
```

## Validation Rules for Patches

Each patch file must:
1. Be valid unified diff format
2. Apply cleanly without merge conflicts (`git apply --check`)
3. Target specific files in the indexing-service module
4. Include adequate context lines (usually 3 lines before/after changes)
5. Have clear, descriptive headers

## Testing Patch Application

```bash
# Before applying
cd /root/druid
git apply --check /root/patches/001-validate-empty-keys.patch

# Apply
git apply /root/patches/001-validate-empty-keys.patch

# Verify build
mvn clean package -DskipTests -Dcheckstyle.skip=true \
  -Dpmd.skip=true -Dforbiddenapis.skip=true -Dspotbugs.skip=true \
  -Danimal.sniffer.skip=true -Denforcer.skip=true -Djacoco.skip=true \
  -Ddependency-check.skip=true -pl '!web-console' -pl indexing-service -am
```