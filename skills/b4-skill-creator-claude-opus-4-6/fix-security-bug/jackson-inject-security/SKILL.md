---
name: jackson-inject-security
description: "Fixing Jackson @JacksonInject bypass vulnerabilities where attackers use empty JSON keys to override injected values. Use this skill whenever reviewing or patching Java code that uses @JacksonInject for security-sensitive configuration injection, especially in Apache projects."
---

# Jackson @JacksonInject Security Bypass

## The Vulnerability

When a Java class uses `@JacksonInject` without specifying `useInput`, Jackson's default behavior allows JSON input to override the injected value. An attacker can exploit this by providing an empty key `""` in the JSON payload, which Jackson maps to the `@JacksonInject` parameter (since it has no explicit property name).

```java
// VULNERABLE: JSON input can override the injected config
@JacksonInject JavaScriptConfig config
```

## The Fix

Use `useInput = OptBoolean.NEVER` to prevent JSON input from overriding injected values:

```java
// SECURE: JSON input is ignored for this parameter
@JacksonInject(useInput = com.fasterxml.jackson.annotation.OptBoolean.NEVER) JavaScriptConfig config
```

This requires Jackson 2.9+ (where `OptBoolean` was introduced).

## Key Points

- The empty key `""` is the default internal name Jackson uses for `@JacksonInject` parameters without `@JsonProperty`
- `useInput = OptBoolean.NEVER` tells Jackson to always use the injected value, never the JSON input
- This is a defense-in-depth fix — it prevents the bypass regardless of what JSON the attacker sends
- All `@JacksonInject` parameters used for security-sensitive configuration should use `useInput = OptBoolean.NEVER`
