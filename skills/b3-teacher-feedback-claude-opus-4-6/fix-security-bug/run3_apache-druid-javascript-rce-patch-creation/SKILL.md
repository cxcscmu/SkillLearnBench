---
name: apache-druid-javascript-rce-patch-creation
description: Step-by-step instructions for creating and applying patches to fix the JavaScript RCE vulnerability in Apache Druid 0.20.0. Covers inspecting actual source code patterns, creating correct sed replacements or patch files, and verifying the fix. Use this when you need to patch and build Druid.
---

## Step-by-Step Patching Process

### Step 1: Inspect the actual source files to find exact annotation patterns

```bash
# First, find all files with @JacksonInject and JavaScriptConfig
cd /root/druid
grep -rn "@JacksonInject" --include="*.java" | grep -i javascript
grep -rn "@JacksonInject" --include="*.java" | grep -i "JavaScriptConfig"
```

Also inspect each specific file to see the exact pattern (whitespace, newlines, existing attributes):

```bash
# Check each known file
for f in \
  "processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java" \
  "processing/src/main/java/org/apache/druid/query/aggregation/JavaScriptAggregatorFactory.java" \
  "processing/src/main/java/org/apache/druid/query/extraction/JavaScriptExtractionFn.java" \
  "processing/src/main/java/org/apache/druid/data/input/impl/JavaScriptParseSpec.java" \
  "processing/src/main/java/org/apache/druid/query/aggregation/post/JavaScriptPostAggregator.java"; do
  echo "=== $f ==="
  grep -n -A2 -B2 "@JacksonInject" "$f" 2>/dev/null || echo "FILE NOT FOUND"
  echo ""
done
```

### Step 2: Understand common annotation patterns in the source

The annotations may appear in these forms:
- `@JacksonInject JavaScriptConfig config` (bare, no parentheses)
- `@JacksonInject("someKey") JavaScriptConfig config`
- Could span multiple lines between annotation and parameter

### Step 3: Create the patch using a Python script for reliability

Using Python instead of sed provides more reliable multi-line pattern matching:

```bash
mkdir -p /root/patches

cat > /root/patches/fix_javascript_rce.py << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
"""
Fix Apache Druid 0.20.0 JavaScript RCE vulnerability.

Changes @JacksonInject annotations on JavaScriptConfig parameters to use
useInput = OptBoolean.FALSE, preventing JSON input from overriding the
server-side JavaScriptConfig.
"""

import os
import re
import sys

DRUID_ROOT = sys.argv[1] if len(sys.argv) > 1 else "/root/druid"

FILES_TO_PATCH = [
    "processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java",
    "processing/src/main/java/org/apache/druid/query/aggregation/JavaScriptAggregatorFactory.java",
    "processing/src/main/java/org/apache/druid/query/extraction/JavaScriptExtractionFn.java",
    "processing/src/main/java/org/apache/druid/data/input/impl/JavaScriptParseSpec.java",
    "processing/src/main/java/org/apache/druid/query/aggregation/post/JavaScriptPostAggregator.java",
]

IMPORT_LINE = "import com.fasterxml.jackson.annotation.JacksonInject;\n"
OPT_BOOLEAN_IMPORT = "import com.fasterxml.jackson.annotation.OptBoolean;\n"


def patch_file(filepath):
    full_path = os.path.join(DRUID_ROOT, filepath)
    if not os.path.exists(full_path):
        print(f"WARNING: File not found: {full_path}")
        return False

    with open(full_path, 'r') as f:
        content = f.read()

    original_content = content

    # Add OptBoolean import if not present
    if "import com.fasterxml.jackson.annotation.OptBoolean;" not in content:
        # Insert after the JacksonInject import line
        if IMPORT_LINE in content:
            content = content.replace(
                IMPORT_LINE,
                IMPORT_LINE + OPT_BOOLEAN_IMPORT
            )
        else:
            # Try to find any jackson annotation import to insert after
            jackson_import_match = re.search(
                r'(import com\.fasterxml\.jackson\.annotation\.\w+;\n)',
                content
            )
            if jackson_import_match:
                insert_after = jackson_import_match.group(0)
                content = content.replace(
                    insert_after,
                    insert_after + OPT_BOOLEAN_IMPORT,
                    1
                )
            else:
                # Insert after package declaration
                content = re.sub(
                    r'(package [^;]+;\n)',
                    r'\1\n' + OPT_BOOLEAN_IMPORT,
                    content,
                    count=1
                )

    # Replace @JacksonInject annotations that are followed (possibly with whitespace/newlines)
    # by JavaScriptConfig. Handle multiple forms:
    
    # Pattern 1: @JacksonInject JavaScriptConfig (bare annotation)
    # Pattern 2: @JacksonInject("...") JavaScriptConfig (with value)
    # We need to handle newlines between annotation and parameter type
    
    # This regex matches @JacksonInject with optional (...) followed eventually by JavaScriptConfig
    # and replaces with @JacksonInject(useInput = OptBoolean.FALSE)
    
    # First handle: @JacksonInject(...) JavaScriptConfig
    content = re.sub(
        r'@JacksonInject\s*\([^)]*\)(\s+)JavaScriptConfig\b',
        r'@JacksonInject(useInput = OptBoolean.FALSE)\1JavaScriptConfig',
        content
    )
    
    # Then handle bare: @JacksonInject JavaScriptConfig (no parentheses)
    # Must not match ones we already replaced (which now have parentheses)
    content = re.sub(
        r'@JacksonInject(\s+)JavaScriptConfig\b',
        r'@JacksonInject(useInput = OptBoolean.FALSE)\1JavaScriptConfig',
        content
    )

    if content != original_content:
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"PATCHED: {filepath}")
        return True
    else:
        print(f"NO CHANGES NEEDED: {filepath}")
        return False


def main():
    print(f"Patching Druid source at: {DRUID_ROOT}")
    patched_count = 0
    for filepath in FILES_TO_PATCH:
        if patch_file(filepath):
            patched_count += 1
    
    # Also search for any other files that might have @JacksonInject with JavaScriptConfig
    print("\nSearching for additional files with @JacksonInject and JavaScriptConfig...")
    for root, dirs, files in os.walk(DRUID_ROOT):
        # Skip hidden dirs and target dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'target']
        for fname in files:
            if fname.endswith('.java'):
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, DRUID_ROOT)
                if rel_path not in FILES_TO_PATCH:
                    with open(fpath, 'r') as f:
                        content = f.read()
                    if '@JacksonInject' in content and 'JavaScriptConfig' in content:
                        print(f"  Additional file found: {rel_path}")
                        if patch_file(rel_path):
                            patched_count += 1
    
    print(f"\nTotal files patched: {patched_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYTHON_SCRIPT

chmod +x /root/patches/fix_javascript_rce.py
```

### Step 4: Apply the patch

```bash
python3 /root/patches/fix_javascript_rce.py /root/druid
```

### Step 5: Verify the patches were applied correctly

```bash
# Verify each file has the correct annotation
for f in \
  "processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java" \
  "processing/src/main/java/org/apache/druid/query/aggregation/JavaScriptAggregatorFactory.java" \
  "processing/src/main/java/org/apache/druid/query/extraction/JavaScriptExtractionFn.java" \
  "processing/src/main/java/org/apache/druid/data/input/impl/JavaScriptParseSpec.java" \
  "processing/src/main/java/org/apache/druid/query/aggregation/post/JavaScriptPostAggregator.java"; do
  echo "=== $f ==="
  grep -n "JacksonInject" "/root/druid/$f"
  grep -n "OptBoolean" "/root/druid/$f"
  echo ""
done
```

### Step 6: Build with Maven

**Important:** Use a single `-pl` flag with comma-separated values to properly exclude web-console while building indexing-service and all dependencies:

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
  -am 2>&1 | tail -50
```

Note: Using `-pl '!web-console' -am` builds ALL modules except web-console. This is safer than trying to specify individual modules, as it ensures all dependent JARs (processing, indexing-service, etc.) are built.

If the build uses too much memory, try with a more targeted build:

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
  -pl 'processing,indexing-service' \
  -am 2>&1 | tail -50
```

### Step 7: Verify the build output

```bash
# Check build success
echo "Build exit code: $?"

# Find the built JARs
find /root/druid/processing/target -name "druid-processing-*.jar" -not -name "*sources*" -not -name "*tests*" 2>/dev/null
find /root/druid/indexing-service/target -name "druid-indexing-service-*.jar" -not -name "*sources*" -not -name "*tests*" 2>/dev/null

# Verify the class files contain the fix
cd /root/druid
jar tf processing/target/druid-processing-0.20.0.jar | grep JavaScriptDimFilter
# Use javap to verify the annotation if possible
mkdir -p /tmp/verify_class
cd /tmp/verify_class
jar xf /root/druid/processing/target/druid-processing-0.20.0.jar org/apache/druid/query/filter/JavaScriptDimFilter.class 2>/dev/null
javap -v org/apache/druid/query/filter/JavaScriptDimFilter.class 2>/dev/null | grep -A5 "JacksonInject"
```

### Step 8: Deploy the patched JARs

```bash
# Copy patched JARs to Druid lib directory
cp /root/druid/processing/target/druid-processing-0.20.0.jar /opt/druid/lib/ 2>/dev/null
cp /root/druid/indexing-service/target/druid-indexing-service-0.20.0.jar /opt/druid/lib/ 2>/dev/null

# Also check for any other modules that might contain affected classes
find /root/druid -path "*/target/druid-*.jar" -not -name "*sources*" -not -name "*tests*" -not -name "*javadoc*" | head -20
```

### Jackson Version Compatibility Note

The `useInput = OptBoolean.FALSE` parameter was added in Jackson 2.9+. Apache Druid 0.20.0 uses Jackson 2.10.x, so this is fully compatible.