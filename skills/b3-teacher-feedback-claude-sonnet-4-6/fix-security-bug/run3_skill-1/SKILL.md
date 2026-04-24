[SKILL]
---
name: apache-druid-cve-javascript-patch
description: Patches Apache Druid 0.20.0 JavaScript RCE vulnerability by fixing JavaScriptConfig injection in all JavaScript filter/function/aggregator classes. Use when you need to remediate the CVE where authenticated users bypass JavaScript security via empty-string JSON key.
---

# Apache Druid JavaScript RCE Patch

## Overview

The vulnerability allows bypassing `JavaScriptConfig` security by using an empty-string JSON key `""` which Jackson treats as an override, enabling JavaScript execution even when disabled. Fix requires:

1. Adding `@JacksonInject(useInput = OptBoolean.FALSE)` to JavaScriptConfig fields in all affected classes
2. Removing any `@JsonProperty("")` that could be exploited
3. Adding null-safety guards in execution paths

## Step 1: Find All Affected Classes

```bash
cd /root/druid
# Find all Java files that use JavaScriptConfig
grep -r "JavaScriptConfig" --include="*.java" -l
# Find all files with javascript in the name
find . -name "JavaScript*.java" | grep -v test | grep -v Test
```

## Step 2: Create Patch Directory

```bash
mkdir -p /root/patches
```

## Step 3: Examine Key Files

```bash
# Check the main filter file
cat processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java

# Check extraction function
cat processing/src/main/java/org/apache/druid/query/extraction/JavaScriptExtractionFn.java

# Check aggregator
cat processing/src/main/java/org/apache/druid/query/aggregation/JavaScriptAggregatorFactory.java

# Check JavaScriptConfig itself
cat processing/src/main/java/org/apache/druid/js/JavaScriptConfig.java

# Check extensions
find extensions-core -name "JavaScript*.java" | grep -v test
```

## Step 4: Write the Patch for JavaScriptConfig

```bash
cat > /root/patches/JavaScriptConfig.patch << 'PATCHEOF'
--- a/processing/src/main/java/org/apache/druid/js/JavaScriptConfig.java
+++ b/processing/src/main/java/org/apache/druid/js/JavaScriptConfig.java
@@ ... @@
PATCHEOF
```

**The actual patch must use `git diff` format. Generate it as follows:**

```bash
cd /root/druid

# First make the changes to JavaScriptConfig.java to prevent empty-key bypass
# View the file to understand current structure
cat processing/src/main/java/org/apache/druid/js/JavaScriptConfig.java
```

## Step 5: Apply Fixes Programmatically

Since patches must match exact line numbers, use sed/python to make changes then generate diffs:

```bash
cd /root/druid

# ---- Fix JavaScriptConfig.java ----
# Ensure it doesn't have @JsonProperty("") and has proper validation
python3 << 'PYEOF'
import re

filepath = "processing/src/main/java/org/apache/druid/js/JavaScriptConfig.java"
with open(filepath, 'r') as f:
    content = f.read()

print("=== Current JavaScriptConfig.java ===")
print(content)
PYEOF
```

```bash
cd /root/druid

# Fix JavaScriptDimFilter.java
python3 << 'PYEOF'
filepath = "processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java"
with open(filepath, 'r') as f:
    content = f.read()
print("=== JavaScriptDimFilter.java ===")
print(content)
PYEOF
```

## Step 6: Make the Actual Code Changes

```bash
cd /root/druid

python3 << 'PYEOF'
import re
import os

def fix_javascript_config_injection(filepath, classname):
    """Add @JacksonInject(useInput = OptBoolean.FALSE) to JavaScriptConfig field"""
    if not os.path.exists(filepath):
        print(f"SKIP (not found): {filepath}")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Add import for JacksonInject if not present
    if 'JacksonInject' not in content:
        # Add after existing Jackson imports or after last import
        content = re.sub(
            r'(import com\.fasterxml\.jackson\.annotation\.JsonProperty;)',
            r'\1\nimport com.fasterxml.jackson.annotation.JacksonInject;\nimport com.fasterxml.jackson.annotation.OptBoolean;',
            content
        )
        if 'JacksonInject' not in content:
            # Try adding after any com.fasterxml import
            content = re.sub(
                r'(import com\.fasterxml\.jackson\.[^;]+;)',
                r'\1\nimport com.fasterxml.jackson.annotation.JacksonInject;\nimport com.fasterxml.jackson.annotation.OptBoolean;',
                content, count=1
            )
    
    # Remove @JsonProperty("") if present (the exploit vector)
    content = re.sub(r'@JsonProperty\(""\)\s*\n\s*', '', content)
    
    # Add @JacksonInject annotation before JavaScriptConfig field/parameter in constructor
    # Pattern: find JavaScriptConfig config parameter in @JsonCreator constructor
    # Add @JacksonInject(useInput = OptBoolean.FALSE) before it
    
    # Fix constructor parameter
    if '@JacksonInject' not in content:
        # Replace JavaScriptConfig config parameter in constructor
        content = re.sub(
            r'(@JsonProperty\([^)]*\)\s+JavaScriptConfig\s+\w+)',
            r'@JacksonInject(useInput = OptBoolean.FALSE) JavaScriptConfig config',
            content
        )
        # Also handle case where it's just JavaScriptConfig without @JsonProperty
        if '@JacksonInject' not in content:
            content = re.sub(
                r'(?<!@JacksonInject\(useInput = OptBoolean\.FALSE\)\s)JavaScriptConfig\s+(config)',
                r'@JacksonInject(useInput = OptBoolean.FALSE) JavaScriptConfig \1',
                content
            )
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"MODIFIED: {filepath}")
        return True
    else:
        print(f"NO CHANGE: {filepath}")
        return False

# Process all known JavaScript classes
files = [
    ("processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java", "JavaScriptDimFilter"),
    ("processing/src/main/java/org/apache/druid/query/extraction/JavaScriptExtractionFn.java", "JavaScriptExtractionFn"),
    ("processing/src/main/java/org/apache/druid/query/aggregation/JavaScriptAggregatorFactory.java", "JavaScriptAggregatorFactory"),
]

# Find additional files
import subprocess
result = subprocess.run(['grep', '-r', 'JavaScriptConfig', '--include=*.java', '-l', '.'], 
                      capture_output=True, text=True)
for line in result.stdout.strip().split('\n'):
    if line and 'test' not in line.lower() and 'Test' not in line:
        found = (line.lstrip('./'), line.split('/')[-1].replace('.java',''))
        if found not in files:
            files.append(found)

for filepath, classname in files:
    fix_javascript_config_injection(filepath, classname)

PYEOF
```

## Step 7: Fix JavaScriptConfig itself to block empty-key bypass

```bash
cd /root/druid

python3 << 'PYEOF'
import re

filepath = "processing/src/main/java/org/apache/druid/js/JavaScriptConfig.java"
with open(filepath, 'r') as f:
    content = f.read()

print("Current content:")
print(content)
print("\n\n")

# Remove any @JsonProperty("") 
if '@JsonProperty("")' in content:
    content = content.replace('@JsonProperty("")', '')
    print("Removed @JsonProperty(\"\")")
    with open(filepath, 'w') as f:
        f.write(content)
PYEOF
```

## Step 8: Direct File Patching with Exact Knowledge of Druid 0.20.0

```bash
cd /root/druid

# Show exact content of JavaScriptDimFilter to understand structure
grep -n "JavaScriptConfig\|@JsonProperty\|@JacksonInject\|JsonCreator\|import" \
    processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java | head -50
```

```bash
cd /root/druid

# Write a comprehensive Python script that reads, modifies, and writes back each file
python3 << 'PYEOF'
import re
import os
import subprocess

def get_files_with_javascript_config():
    result = subprocess.run(
        ['grep', '-r', 'JavaScriptConfig', '--include=*.java', '-l', '.'],
        capture_output=True, text=True, cwd='/root/druid'
    )
    files = []
    for f in result.stdout.strip().split('\n'):
        if f and '/test' not in f and 'Test.java' not in f:
            files.append(f.lstrip('./'))
    return files

def patch_file(filepath):
    full_path = os.path.join('/root/druid', filepath)
    if not os.path.exists(full_path):
        print(f"NOT FOUND: {full_path}")
        return
    
    with open(full_path, 'r') as f:
        content = f.read()
    
    original = content
    changed = False
    
    # 1. Remove @JsonProperty("") - this is the exploit vector
    if '@JsonProperty("")' in content:
        content = re.sub(r'\s*@JsonProperty\(""\)', '', content)
        print(f"  Removed @JsonProperty(\"\") from {filepath}")
        changed = True
    
    # 2. Add necessary imports if not present
    needs_jackoninject = 'JacksonInject' not in content
    needs_optboolean = 'OptBoolean' not in content
    
    if needs_jackoninject or needs_optboolean:
        # Find position after last import statement
        import_section_end = 0
        for m in re.finditer(r'^import .*;$', content, re.MULTILINE):
            import_section_end = m.end()
        
        if import_section_end > 0:
            imports_to_add = ''
            if needs_jackoninject:
                imports_to_add += '\nimport com.fasterxml.jackson.annotation.JacksonInject;'
            if needs_optboolean:
                imports_to_add += '\nimport com.fasterxml.jackson.annotation.OptBoolean;'
            content = content[:import_section_end] + imports_to_add + content[import_section_end:]
            print(f"  Added imports to {filepath}")
            changed = True
    
    # 3. Add @JacksonInject(useInput = OptBoolean.FALSE) before JavaScriptConfig parameter
    # in @JsonCreator constructors
    if '@JacksonInject' not in content:
        # Pattern: JavaScriptConfig varname in constructor parameters
        # Could have @JsonProperty or nothing before it
        new_content = re.sub(
            r'(\s+)(@JsonProperty\([^)]*\)\s+)?JavaScriptConfig(\s+\w+)',
            r'\1@JacksonInject(useInput = OptBoolean.FALSE)\n\1JavaScriptConfig\3',
            content
        )
        if new_content != content:
            content = new_content
            print(f"  Added @JacksonInject to JavaScriptConfig param in {filepath}")
            changed = True
    
    if changed:
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"  Written: {filepath}")
    else:
        print(f"  No changes needed: {filepath}")

files = get_files_with_javascript_config()
print("Files to patch:")
for f in files:
    print(f"  {f}")
    patch_file(f)

PYEOF
```

## Step 9: Also Fix JavaScriptConfig to add null check

```bash
cd /root/druid

python3 << 'PYEOF'
import os

filepath = '/root/druid/processing/src/main/java/org/apache/druid/js/JavaScriptConfig.java'
with open(filepath, 'r') as f:
    content = f.read()

print(content)
PYEOF
```

## Step 10: Generate Patch Files from Git Diff

```bash
cd /root/druid
git diff > /root/patches/javascript-rce-fix.patch
echo "Patch file created:"
cat /root/patches/javascript-rce-fix.patch
```

## Step 11: Verify the Changes

```bash
cd /root/druid

# Check that @JacksonInject is now present in key files
echo "=== Checking JavaScriptDimFilter ==="
grep -n "JacksonInject\|OptBoolean\|JsonProperty\|JavaScriptConfig" \
    processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java

echo "=== Checking JavaScriptExtractionFn ==="
grep -n "JacksonInject\|OptBoolean\|JsonProperty\|JavaScriptConfig" \
    processing/src/main/java/org/apache/druid/query/extraction/JavaScriptExtractionFn.java

echo "=== Checking JavaScriptAggregatorFactory ==="
grep -n "JacksonInject\|OptBoolean\|JsonProperty\|JavaScriptConfig" \
    processing/src/main/java/org/apache/druid/query/aggregation/JavaScriptAggregatorFactory.java
```

## Step 12: Build Druid

```bash
cd /root/druid
mvn clean package -DskipTests \
    -Dcheckstyle.skip=true \
    -Dpmd.skip=true \
    -Dforbiddenapis.skip=true \
    -Dspotbugs.skip=true \
    -Danimal.sniffer.skip=true \
    -Denforcer.skip=true \
    -Djacoco.skip=true \
    -Ddependency-check.skip=true \
    -pl '!web-console' \
    -pl indexing-service -am 2>&1 | tail -50
```

## Step 13: Verify Build Output

```bash
# Check the built JAR exists
find /root/druid -name "druid-indexing-service-*.jar" -not -path "*/original-*" 2>/dev/null
find /root/druid -name "druid-processing-*.jar" -not -path "*/original-*" 2>/dev/null

# Verify the patch is in the built classes
jar tf $(find /root/druid/processing/target -name "druid-processing-*.jar" | head -1) | grep JavaScript
```

## Step 14: Alternative - Write New Files Directly if Patching Fails

If the above regex-based approach doesn't work, write replacement files directly:

```bash
cd /root/druid

# Get exact line structure
cat -n processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java
```

```bash
# Use a targeted Python approach with line-by-line replacement
python3 << 'PYEOF'
import re

def patch_javascript_dim_