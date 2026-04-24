---
name: run2_jackson-inject-bypass
description: Security guide for Jackson @JacksonInject vulnerabilities - how attackers override injectable values via JSON and how to prevent it
---

# Jackson @JacksonInject Security Bypass - Complete Reference

## What is @JacksonInject?

`@JacksonInject` marks a Java constructor parameter or field to receive its value from the
`ObjectMapper`'s `InjectableValues` rather than from the deserialized JSON. This is used in
frameworks like Apache Druid to inject server-side configuration that should not be controllable
by external JSON input (e.g., `druid.javascript.enabled` from server properties).

## The Vulnerability Pattern

```java
@JsonCreator
public SomeFilter(
    @JsonProperty("function") String function,
    @JacksonInject SomeConfig config  // VULNERABLE
)
```

When `useInput` is `OptBoolean.DEFAULT` (the default), Jackson:
- **For `@JsonCreator` constructor params:** Uses JSON input if available, falls back to injectable
- The JSON key used to match is the injection ID (empty string `""` if no ID specified)
- An attacker can include `"": {"enabled": true}` in JSON to create a new `SomeConfig` object

## OptBoolean Values Reference

| Value | Behavior | Security |
|-------|----------|----------|
| `OptBoolean.DEFAULT` | Context-dependent; `@JsonCreator` params prefer JSON | VULNERABLE |
| `OptBoolean.TRUE` | Always prefers JSON input over injectable | VULNERABLE |
| `OptBoolean.FALSE` | Never reads from JSON; always uses injectable | SECURE |

## The Fix

```java
import com.fasterxml.jackson.annotation.OptBoolean;

// SECURE: JSON can never override the server-injected config
@JacksonInject(useInput = OptBoolean.FALSE) SomeConfig config
```

## How to Identify Vulnerable Code

Search for: `@JacksonInject` in constructor parameters for security-sensitive types.

Signs of vulnerability:
1. The injected type controls security behavior (enabled/disabled flags, permissions)
2. No explicit `useInput = OptBoolean.FALSE`
3. JSON deserialization accepts user-controlled input (REST API endpoints)

## Injection ID Mechanics

When no `value` is specified in `@JacksonInject`, Jackson uses either:
- The fully-qualified class name as the injection ID, OR
- The empty string `""` as a fallback injection ID for certain Jackson versions

The exploit uses `""` as the property name in JSON to supply the "injected" value:
```json
{ "": { "enabled": true } }
```

## Testing the Fix

A correctly patched endpoint should return a 500 error with "JavaScript is disabled"
when receiving the exploit payload, even if `"": {"enabled": true}` is present.

## Other Vulnerable Patterns to Audit

Any use of `@JacksonInject` in:
- `@JsonCreator`-annotated constructors that accept user-controlled JSON
- REST API request/response DTOs
- Jackson polymorphic type handling with `@JsonTypeInfo`
