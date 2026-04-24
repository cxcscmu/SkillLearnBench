---
name: jackson-injection-security
description: Security considerations for Jackson @JacksonInject - preventing JSON input from overriding injected values, covering CVE patterns and defense strategies.
---

# Jackson @JacksonInject Security

## The Vulnerability Pattern

When a `@JsonCreator` constructor uses `@JacksonInject` without `useInput = OptBoolean.FALSE`,
Jackson can fall back to JSON input to provide the injectable value. This is exploitable when:
1. The injectable ID (default: empty string `""`) matches a JSON property key
2. The JSON property contains a deserializable value of the expected type
3. This overrides the server-configured injected value (e.g., security settings)

### Example Vulnerable Code
```java
@JsonCreator
public SomeFilter(
    @JsonProperty("dimension") String dimension,
    @JacksonInject SecurityConfig config  // VULNERABLE: can be overridden via JSON ""
)
```

### Exploit Pattern
```json
{
  "dimension": "value",
  "": {"securityEnabled": false}  // Empty key "" overrides @JacksonInject default id
}
```

## The Fix

### Option 1: useInput = OptBoolean.FALSE (Recommended for Jackson 2.9+)
```java
import com.fasterxml.jackson.annotation.OptBoolean;

@JsonCreator
public SomeFilter(
    @JsonProperty("dimension") String dimension,
    @JacksonInject(useInput = OptBoolean.FALSE) SecurityConfig config  // FIXED
)
```
This tells Jackson: NEVER use JSON to provide this value, ALWAYS use InjectableValues only.

### Option 2: Explicit Injectable ID (prevents empty string match)
```java
@JacksonInject("securityConfig")  // Named ID that won't match "" key
SecurityConfig config
```

### Option 3: Server-side validation before processing
```java
// Validate BEFORE Jackson deserialization or AFTER using Guice-injected config
@Inject
public MyService(SecurityConfig trustedConfig) {
    this.trustedConfig = trustedConfig;  // From Guice, not from Jackson
}
```

## @JacksonInject Behavior Summary

| `useInput` value | Behavior |
|---|---|
| `OptBoolean.DEFAULT` | Use InjectableValues if present; may fall back to JSON |
| `OptBoolean.TRUE` | JSON input takes precedence over InjectableValues |
| `OptBoolean.FALSE` | ONLY use InjectableValues; NEVER read from JSON |

## Druid-Specific Context

In Apache Druid, Jackson InjectableValues are configured via Guice's `GuiceInjectableValues`.
The injectable ID lookup uses the parameter type's class name by default.

When `@JacksonInject.value()` is `""` (empty string default), Jackson may use the empty string
as the lookup key, which fails to find the Guice-bound value, causing fallback to JSON.

## Detection
Look for `@JacksonInject` without `useInput = OptBoolean.FALSE` in `@JsonCreator` constructors
where the injected value controls security behavior.
