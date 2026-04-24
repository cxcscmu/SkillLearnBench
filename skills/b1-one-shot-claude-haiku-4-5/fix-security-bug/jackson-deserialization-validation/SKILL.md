---
name: jackson-deserialization-validation
description: Securing Jackson JSON deserialization by validating input before processing and preventing unknown properties.
---

# Jackson Deserialization Validation

## Vulnerability Pattern

When Jackson deserializes JSON with unknown properties, if not handled properly, malicious extra properties can bypass validation logic:

```json
{
  "validProperty": "legitimate value",
  "": {
    "enabled": true,
    "other": "malicious"
  }
}
```

The empty key `""` can be overlooked by simple property checks.

## Jackson Configuration

### 1. Fail on Unknown Properties
```java
@JsonIgnoreProperties(ignoreUnknown = false)
public class MyFilter {
    @JsonProperty
    private String function;

    // This will throw exception on unknown properties
}
```

### 2. Custom Deserialization
```java
@JsonDeserialize(using = CustomDeserializer.class)
public class MyFilter {
    // Custom logic during deserialization
}
```

### 3. @JsonAnySetter for Validation
```java
public class MyFilter {
    @JsonProperty
    private String function;

    @JsonAnySetter
    public void handleUnknown(String key, Object value) {
        if (key == null || key.isEmpty()) {
            throw new IllegalArgumentException("Empty property keys not allowed");
        }
        // Validate other unknown properties
    }
}
```

## Validation Strategies

### Strategy 1: Whitelist Allowed Keys
```java
private static final Set<String> ALLOWED_KEYS =
    Set.of("function", "type", "name");

@JsonAnySetter
public void handleProperty(String key, Object value) {
    if (!ALLOWED_KEYS.contains(key)) {
        throw new IllegalArgumentException(
            "Unknown property: " + key);
    }
}
```

### Strategy 2: Reject Empty/Null Keys
```java
@JsonAnySetter
public void validateKey(String key, Object value) {
    if (key == null || key.trim().isEmpty()) {
        throw new IllegalArgumentException(
            "Property keys cannot be empty or null");
    }
}
```

### Strategy 3: Post-Deserialization Validation
```java
@JsonProperty
private Map<String, Object> properties;

@PostConstruct
public void validate() {
    for (String key : properties.keySet()) {
        if (key == null || key.isEmpty()) {
            throw new IllegalArgumentException(
                "Empty keys not allowed");
        }
    }
}
```

## Implementation in Druid

### Finding Vulnerable Classes
1. Search for `@JsonTypeName("javascript")`
2. Look for JavaScript filter/transform specs
3. Check deserialization of filter objects

### Key Locations
- `JavaScriptFilter.java` - Main JavaScript filter class
- Filter spec handlers in indexing-service
- Transform spec deserialization

### Fix Pattern
```java
@JsonIgnoreProperties(ignoreUnknown = false)
public class JavaScriptFilter {
    @JsonProperty
    private String function;

    @JsonAnySetter
    public void handleUnknown(String key, Object value) {
        throw new IllegalArgumentException(
            "Unknown property '" + key +
            "' in JavaScript filter specification");
    }
}
```

## Testing the Fix

### Test Case 1: Valid Request
```java
String json = "{\"type\":\"javascript\",\"function\":\"function(){return true;}\"}";
JavaScriptFilter filter = mapper.readValue(json, JavaScriptFilter.class);
// Should succeed
```

### Test Case 2: Empty Key (Should Fail)
```java
String json = "{\"type\":\"javascript\",\"function\":\"...\",\"\":{\"enabled\":true}}";
assertThrows(JsonMappingException.class, () ->
    mapper.readValue(json, JavaScriptFilter.class));
// Should throw exception
```

### Test Case 3: Null Key (Should Fail)
```java
String json = "{\"type\":\"javascript\",null:{\"value\":\"bad\"}}";
assertThrows(JsonMappingException.class, () ->
    mapper.readValue(json, JavaScriptFilter.class));
```

## Druid-Specific Considerations

1. **Custom ObjectMapper**: Druid may use custom ObjectMapper configuration
2. **Multiple Filter Types**: Fix may need to apply to multiple filter classes
3. **Backward Compatibility**: Ensure legitimate requests still work
4. **Nested Specs**: Check if transformSpec or other nested objects also need fixes

## Recommended Approach

1. Use `@JsonIgnoreProperties(ignoreUnknown = false)` to detect unknown properties
2. Add `@JsonAnySetter` to validate property names
3. Reject any empty string keys explicitly
4. Test both via HTTP API and direct deserialization
