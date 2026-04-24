---
name: Disable JavaScript Execution in Druid Filters
description: Configure and enforce a security policy that completely disables JavaScript filter evaluation in Apache Druid, preventing arbitrary code execution through the javascript filter type even if structural validation is bypassed.
---

# Disabling JavaScript Filter Execution

## Problem
Even if empty key validation is in place, the `"type": "javascript"` filter capability itself is a code execution vector. The security sandbox can be disabled or bypassed.

## Solution: Disable JavaScript Filters at Configuration Level

### Implementation Strategy

1. **Identify JavaScript Filter Registration**
   - Find `JavaScriptDimFilter` class and its factory registration
   - Locate where filter types are registered (likely in a filter registry or module)
   - Find where JavaScript evaluation is initialized

2. **Create Security Configuration**
   - Add a Druid configuration property to disable JavaScript filters
   - Default to **disabled** (secure-by-default)
   - Prevent re-enabling via ObjectMapper annotations or runtime configuration

3. **Enforcement Approach**

   **Option A: Remove from Filter Registry**
   - Unregister `JavaScriptDimFilter` from the factory
   - During module initialization, skip registration of JavaScript filter type
   - Returns 400 Bad Request if client attempts to use it

   **Option B: Reject at Deserialization**
   - Create a custom deserializer for filter JSON
   - If `type == "javascript"`, throw `JsonMappingException` immediately
   - Prevents any JavaScript filter from being instantiated

4. **Configuration Property**
   ```
   druid.javascript.enabled=false  (default, required for security)
   ```

### Code Pattern

```java
// In filter factory or deserializer
if ("javascript".equals(filterType)) {
    if (!isJavaScriptEnabled()) {
        throw new IllegalArgumentException(
            "JavaScript filters are disabled. " +
            "Set druid.javascript.enabled=true to enable (not recommended)."
        );
    }
}

private static boolean isJavaScriptEnabled() {
    // Check configuration, default false
    return config.getBoolean("druid.javascript.enabled", false);
}
```

### Defense in Depth

- Even if an attacker bypasses empty key validation, they cannot execute JavaScript
- JavaScript evaluation engine should not be initialized if disabled
- Configuration should be immutable once the server starts