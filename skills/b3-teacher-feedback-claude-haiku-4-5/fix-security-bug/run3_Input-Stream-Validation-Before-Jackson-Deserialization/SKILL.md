---
name: Input Stream Validation Before Jackson Deserialization
description: Validate and sanitize raw JSON input at the point where it enters Jackson's deserialization pipeline, before any ObjectMapper.readValue() call processes it, to prevent bypass attacks using empty keys.
---

# Pre-Deserialization JSON Input Validation

## Problem
The empty key `""` attack occurs during Jackson's deserialization phase. Post-deserialization validation (on the resulting Java object) cannot catch structural JSON attacks because the damage is already done once the object is created.

## Solution: Raw JSON Stream Validation

### Validation Rules

Before JSON enters `ObjectMapper.readValue()`, apply these checks:

1. **Empty Key Detection**
   ```
   Reject any JSON object containing a key with zero length: ""
   This includes nested objects in transformSpec, filter, and all child structures
   ```

2. **Scope**
   - Applied to all HTTP request bodies targeting indexing endpoints
   - Applied to `/druid/indexer/v1/sampler` POST requests
   - Applied to any endpoint that accepts DataSchema with TransformSpec

3. **Implementation Approach**
   - Create a JSON validator that walks the parsed JSON tree (using a lightweight parser like `JsonNode`)
   - Check all object keys recursively for empty strings
   - Reject the entire request if any empty key is found
   - Return HTTP 400 Bad Request with clear error message

### Validator Pseudocode

```
function validateJsonNoEmptyKeys(jsonString):
    jsonTree = parseJson(jsonString)
    if hasEmptyKeyRecursive(jsonTree):
        throw ValidationException("Empty keys not allowed in JSON")
    return true

function hasEmptyKeyRecursive(node):
    if node is ObjectNode:
        for each key in node.fieldNames():
            if key == "":
                return true
            if hasEmptyKeyRecursive(node.get(key)):
                return true
    else if node is ArrayNode:
        for each element in node:
            if hasEmptyKeyRecursive(element):
                return true
    return false
```

### Placement in Request Flow

The validation must occur:
1. **Early** — immediately after the HTTP request body is received
2. **Before ObjectMapper.readValue()** — in the resource handler or via a servlet filter
3. **For all indexing endpoints** — not just sampler, to prevent similar bypasses elsewhere