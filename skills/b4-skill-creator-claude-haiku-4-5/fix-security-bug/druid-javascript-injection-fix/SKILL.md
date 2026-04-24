---
name: druid-javascript-injection-fix
description: How to patch the Apache Druid 0.20.0 JavaScript sandbox bypass vulnerability. Use this skill when fixing CVE in Druid where authenticated attackers can execute arbitrary code through malicious JavaScript payloads via the sampler endpoint. The vulnerability allows empty key "" in filter specifications to bypass JavaScript security settings.
---

# Fixing Apache Druid JavaScript Injection Vulnerability

## Vulnerability Overview

Apache Druid 0.20.0 contains a critical vulnerability where authenticated attackers can execute arbitrary Java code through malicious JavaScript payloads. The vulnerability exists in the `/druid/indexer/v1/sampler` endpoint where the empty key `""` in filter specifications can bypass JavaScript security settings.

**Affected Component:** Druid indexer sampler - specifically the `JavaScriptFilter` validation

**Root Cause:** Insufficient validation of filter specification keys before JavaScript execution

## Identifying the Vulnerable Code

The vulnerability is typically found in:
- `druid-core/src/main/java/org/apache/druid/query/filter/JavaScriptFilter.java`
- Filter parsing/validation logic that processes the `transformSpec.filter` JSON

Look for:
1. JavaScript filter implementations that execute user-provided functions
2. Lack of validation on the filter specification keys
3. Missing checks for suspicious keys (especially empty strings `""`)

## Patch Strategy

### 1. Validate Filter Specification Keys

Add validation to reject or sanitize suspicious keys in the filter specification:

```java
// Reject empty keys or keys that bypass security
if (filterSpec.containsKey("") || filterSpec.containsKey(null)) {
    throw new IllegalArgumentException("Invalid filter specification: contains empty or null keys");
}
```

### 2. Strengthen JavaScript Context Setup

Ensure the JavaScript execution context:
- Explicitly disables dangerous Java interop
- Validates function syntax before execution
- Runs in a restricted scope

```java
// Example: Check for java.lang.Runtime references
String function = getFunction();
if (function.contains("java.lang.Runtime") ||
    function.contains("java.lang.ProcessBuilder")) {
    throw new IllegalArgumentException("JavaScript functions cannot access Java runtime");
}
```

### 3. Validate Filter Configuration Structure

Before executing any JavaScript filter, validate the complete filter specification:
- All keys should be expected, known keys
- Nested objects should follow the documented schema
- Reject any non-standard keys

## Testing the Patch

After patching, verify:

1. **Legitimate requests work:**
   - Standard JavaScript filters execute correctly
   - Filters with valid syntax pass validation
   - Normal sampler operations complete successfully

2. **Exploit attempts are blocked:**
   - Requests with empty key `""` are rejected
   - Java Runtime calls in JavaScript are blocked
   - Invalid filter specifications throw clear errors
   - Error messages don't leak sensitive information

## Common Patch Locations in Druid

- `druid-core/src/main/java/org/apache/druid/query/filter/JavaScriptFilter.java`
- `druid-indexing-service/src/main/java/org/apache/druid/indexing/*/SamplerResource.java`
- `druid-core/src/main/java/org/apache/druid/query/filter/FilterJsonHolder.java` (if parsing logic here)

## Patch File Format

Create patches using `git diff` to generate unified diff format:

```bash
git diff > fix-javascript-injection.patch
```

Patches should be applied to the repository with:
```bash
cd /root/druid
git apply /root/patches/fix-javascript-injection.patch
```

or

```bash
cd /root/druid
git am /root/patches/fix-javascript-injection.patch
```
