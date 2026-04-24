---
name: run2_jackson-security-patching
description: Creating and applying security patches for Jackson deserialization vulnerabilities in Java
---

# Jackson Security Patching

## Overview

Jackson is the de facto JSON serialization library in Java applications. Security vulnerabilities in Jackson deserialization require careful patching to maintain backward compatibility while improving security.

## Common Jackson Vulnerabilities

### 1. Unknown Property Injection
**Issue**: Classes accept unknown properties during JSON deserialization
**Fix**: Add `@JsonIgnoreProperties(ignoreUnknown = false)` annotation
**Impact**: Forces Jackson to reject unexpected JSON keys

### 2. Loose Type Handling
**Issue**: Flexible type coercion allowing unexpected conversions
**Fix**: Use `@JsonProperty(required = true)` for required fields
**Impact**: Ensures type safety during deserialization

### 3. Missing Validation
**Issue**: No validation of deserialized values
**Fix**: Add validation in constructor via Preconditions or custom validator
**Impact**: Catches malicious input early

## Security Patch Pattern

### Step 1: Identify Vulnerable Class

Look for:
- Classes with `@JsonCreator` but no property validation
- Classes accepting user input through JSON
- Classes without `@JsonIgnoreProperties` annotation
- Classes with `@JacksonInject` that could be bypassed

### Step 2: Create the Patch

For unknown property vulnerability:

```diff
import com.fasterxml.jackson.annotation.JacksonInject;
import com.fasterxml.jackson.annotation.JsonCreator;
+import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

+@JsonIgnoreProperties(ignoreUnknown = false)
public class VulnerableClass
{
  // ... existing code ...
}
```

### Step 3: Apply and Test

```bash
# Verify patch applies cleanly
git apply --check security-fix.patch

# Apply the patch
git apply security-fix.patch

# Verify changes
git diff

# Rebuild with security-focused flags
mvn clean package -DskipTests -Dcheckstyle.skip=true ...
```

## Patch File Format

A security patch for Jackson vulnerability:

```diff
--- a/src/main/java/MyFilter.java
+++ b/src/main/java/MyFilter.java
@@ -1,6 +1,7 @@

 import com.fasterxml.jackson.annotation.JacksonInject;
 import com.fasterxml.jackson.annotation.JsonCreator;
+import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
 import com.fasterxml.jackson.annotation.JsonProperty;

+@JsonIgnoreProperties(ignoreUnknown = false)
 public class MyFilter
```

## Validation Strategies

### Strategy 1: Explicit Property Rejection
```java
@JsonIgnoreProperties(ignoreUnknown = false)
public class MyClass { }
```

### Strategy 2: Constructor Validation
```java
@JsonCreator
public MyClass(
    @JsonProperty("field") String field
) {
    Preconditions.checkNotNull(field, "field must not be null");
    Preconditions.checkArgument(!field.isEmpty(), "field must not be empty");
    this.field = field;
}
```

### Strategy 3: Setter Validation
```java
public MyClass {
    @JsonProperty
    public void setField(String field) {
        if (field == null || field.isEmpty()) {
            throw new IllegalArgumentException("Invalid field");
        }
        this.field = field;
    }
}
```

## Testing the Security Fix

### Unit Test for Patch
```java
@Test(expected = UnrecognizedPropertyException.class)
public void testRejectsUnknownProperties() {
    String json = "{\"dimension\":\"test\",\"unknownField\":\"value\"}";
    ObjectMapper mapper = new ObjectMapper();
    mapper.readValue(json, JavaScriptDimFilter.class);
    // Should throw UnrecognizedPropertyException
}

@Test
public void testAcceptsKnownProperties() {
    String json = "{\"dimension\":\"test\",\"function\":\"function(x){return x>5;}\"}";
    ObjectMapper mapper = new ObjectMapper();
    JavaScriptDimFilter filter = mapper.readValue(json, JavaScriptDimFilter.class);
    assertNotNull(filter);
}
```

## Patch Application Order

When multiple security patches are needed:

1. **Jackson Configuration** patches first (global settings)
2. **Class-level** patches (annotations)
3. **Method-level** patches (validation)
4. **Integration** patches (endpoint security)

## Common Issues and Solutions

### Issue: Patch Doesn't Apply
```bash
# Cause: Different file paths or whitespace
# Solution: Check file path prefix
git apply -p0 patch.patch  # If paths are different

# Cause: File has been modified
# Solution: Rebase or recreate patch
git diff --no-index old/File.java new/File.java > fixed.patch
```

### Issue: Jackson Ignores Unknown Properties in Tests
```bash
# Cause: Test Jackson config differs from production
# Solution: Explicitly configure ObjectMapper for tests
ObjectMapper mapper = new ObjectMapper();
mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
// Only disable in tests, not production
```

### Issue: Properties Still Being Accepted
```bash
# Cause: @JsonIgnoreProperties applied to interface, not implementation
# Solution: Apply annotation to concrete class
@JsonIgnoreProperties(ignoreUnknown = false)
public class ConcreteImplementation implements Interface { }
```

## Jackson Security Checklist

- [ ] All user-input facing classes have `@JsonIgnoreProperties(ignoreUnknown = false)`
- [ ] Constructor arguments are validated with Preconditions
- [ ] @JsonProperty fields are explicitly defined
- [ ] Security-sensitive properties use `@JacksonInject`
- [ ] Tests verify rejection of unknown properties
- [ ] Patch applies cleanly without conflicts
- [ ] Build succeeds with security checks enabled
- [ ] Integration tests pass with patched code

## References

- Jackson Framework: https://github.com/FasterXML/jackson
- OWASP Deserialization: https://owasp.org/www-community/deserialization_of_untrusted_data
- Jackson Annotations: https://fasterxml.github.io/jackson-annotations/
