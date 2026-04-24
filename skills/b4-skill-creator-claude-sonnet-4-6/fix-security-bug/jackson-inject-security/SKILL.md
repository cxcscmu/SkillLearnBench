---
name: jackson-inject-security
description: Security considerations for Jackson @JacksonInject annotation in Java applications. How to prevent JSON input from overriding server-injected values. Use this skill whenever reviewing code that uses @JacksonInject, when an attacker could supply JSON to override configuration objects, or when fixing deserialization vulnerabilities related to injectable values.
---

# Jackson @JacksonInject Security

## The Problem

`@JacksonInject` is used to inject server-side values (from Guice or ObjectMapper `InjectableValues`) into deserialized objects. By default, Jackson **allows JSON input to override** injected values if a matching key is found in the JSON.

This creates a vulnerability: an attacker can supply a crafted JSON field (often using the empty string key `""`) to override what should be a trusted server-side configuration value.

## Safe vs Unsafe Usage

**Unsafe (default behavior):**
```java
@JsonCreator
public MyClass(
    @JsonProperty("name") String name,
    @JacksonInject MyConfig config  // JSON can override this!
) { ... }
```

**Safe:**
```java
@JsonCreator
public MyClass(
    @JsonProperty("name") String name,
    @JacksonInject(useInput = OptBoolean.FALSE) MyConfig config  // JSON cannot override
) { ... }
```

## The `useInput` Parameter

| Value | Behavior |
|-------|----------|
| `OptBoolean.TRUE` | Allow JSON input to provide/override the injected value |
| `OptBoolean.FALSE` | **Never** use JSON input; always use server-injected value |
| `OptBoolean.DEFAULT` | Jackson decides (usually allows input override) |

## Required Import

```java
import com.fasterxml.jackson.annotation.OptBoolean;
```

## Empty String Key Attack

The empty key `""` is a Jackson quirk where it can match `@JacksonInject` parameters without explicit IDs:

```json
{
  "normalField": "value",
  "": { "enabled": true }   // overrides @JacksonInject'd config
}
```

Jackson versions prior to 2.13 were particularly susceptible when `@JacksonInject` had no explicit ID specified.

## When to Apply This Fix

- Any `@JacksonInject` parameter that holds security-sensitive config (enabled/disabled flags, auth configs)
- When JSON payload comes from untrusted external sources (HTTP requests, user input)
- When deserialized objects control security behavior (feature flags, access control)

## Audit Checklist

Search for `@JacksonInject` in the codebase:
```bash
grep -r "@JacksonInject" --include="*.java" -l
```

For each occurrence, verify:
1. Is `useInput = OptBoolean.FALSE` set?
2. If not, can an attacker-controlled JSON payload reach this deserializer?
3. Does overriding the injected value change security behavior?
