---
name: run2_druid-javascript-deserialization-security
description: Securing Apache Druid JavaScript filters against unknown property injection attacks
---

# Apache Druid JavaScript Filter Deserialization Security

## The Vulnerability

**CVE-2026-XXXXX**: Unknown Property Injection in JavaScriptDimFilter

Apache Druid versions up to 0.20.0 accept unknown JSON properties during deserialization of the JavaScriptDimFilter. An authenticated attacker can exploit this to inject malicious configuration through unknown properties, potentially bypassing JavaScript security restrictions.

### Vulnerable Payload Example
```json
POST /druid/indexer/v1/sampler HTTP/1.1
Content-Type: application/json

{
  "type": "index",
  "spec": {
    "dataSchema": {
      "transformSpec": {
        "filter": {
          "type": "javascript",
          "function": "function(){java.lang.Runtime.getRuntime().exec('cmd');}",
          "": {"enabled": true},
          "malicious": "property"
        }
      }
    }
  }
}
```

### Root Cause

1. **Jackson Default Behavior**: By default, Jackson ignores unknown JSON properties during deserialization
2. **No Explicit Validation**: The JavaScriptDimFilter class didn't explicitly reject unknown properties
3. **Injection Vector**: An attacker could include unexpected properties like empty strings (`""`) or other unknown fields
4. **Potential Impact**: While current Jackson versions ignore these, they could potentially be exploited in future versions or with custom Jackson configurations

## The Fix

Add the `@JsonIgnoreProperties(ignoreUnknown = false)` annotation to the JavaScriptDimFilter class:

```java
@JsonIgnoreProperties(ignoreUnknown = false)
public class JavaScriptDimFilter extends AbstractOptimizableDimFilter implements DimFilter
{
  // ... existing code ...
}
```

### Why This Works

1. **Explicit Failure Mode**: Sets Jackson to throw an exception when unknown properties are encountered
2. **Whitelisting Approach**: Only allows properties explicitly defined with `@JsonProperty` annotations:
   - `dimension`
   - `function`
   - `extractionFn`
   - `filterTuning`
3. **Defense in Depth**: Prevents any unexpected configuration injection
4. **Forward Compatibility**: Protects against future Jackson configuration changes

## Implementation Details

### JavaScriptDimFilter Known Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `dimension` | String | Yes | The dimension to filter on |
| `function` | String | Yes | JavaScript function as string |
| `extractionFn` | ExtractionFn | No | Optional extraction function |
| `filterTuning` | FilterTuning | No | Optional filter tuning parameters |

### Property Validation Flow

1. **Deserialization**: Jackson receives JSON payload
2. **Property Matching**: Jackson matches JSON keys to `@JsonProperty` annotations
3. **Unknown Property Check**: If `ignoreUnknown = false`, unknown properties cause exception
4. **Injection Prevention**: Malicious properties like `""`, `"enabled"`, etc. are rejected

## Testing the Fix

### Valid Request (Should Pass)
```json
{
  "type": "javascript",
  "dimension": "user_id",
  "function": "function(x) { return x > 100; }"
}
```

### Invalid Request (Should Fail)
```json
{
  "type": "javascript",
  "dimension": "user_id",
  "function": "function(x) { return x > 100; }",
  "unknownProperty": "value"
}
```

Error: `UnrecognizedPropertyException: Unrecognized field "unknownProperty"...`

## Security Implications

### Before Fix
- Attackers could send unknown properties in JSON
- Properties were silently ignored
- Created uncertainty about what was being processed
- Potential for future exploitation with different Jackson versions

### After Fix
- Only whitelisted properties are accepted
- Explicit rejection of malicious payloads
- Clear API contract for JavaScriptDimFilter
- Protection against property injection attacks

## Related Vulnerabilities

This fix addresses the broader category of **deserialization vulnerabilities** in Java applications:
- OWASP: Deserialization of Untrusted Data
- Jackson: Unknown Property Handling
- Jackson Framework: @JsonIgnoreProperties documentation

## Best Practices

For similar Jackson-based classes:
1. Always use `@JsonIgnoreProperties(ignoreUnknown = false)` to be explicit about accepted properties
2. Validate all @JsonProperty fields in constructors
3. Use @JacksonInject for security-sensitive configuration
4. Document the expected JSON structure
5. Consider using @JsonPropertyOrder for clarity
