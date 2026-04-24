---
name: jackson-inject-security
description: Preventing Jackson @JacksonInject override attacks where JSON input can replace server-side injected values.
---

# Jackson @JacksonInject Security

## The Vulnerability

When using `@JacksonInject` in Jackson `@JsonCreator` constructors, JSON input can override server-side injected values by default. This happens because `@JacksonInject` defaults to `useInput = OptBoolean.DEFAULT`, which allows JSON properties to take precedence over injected values.

## Attack Mechanism

If a class has:
```java
@JsonCreator
public MyClass(@JacksonInject MyConfig config) { ... }
```

An attacker can send JSON with `"": {"enabled": true}` to override the injected `config` value. The empty string key `""` maps to inject parameters that have no explicit ID.

Combined with `FAIL_ON_UNKNOWN_PROPERTIES = false` (common in many frameworks), the attack payload passes silently.

## Fix: useInput = OptBoolean.FALSE

Jackson 2.9+ introduced `OptBoolean` for `@JacksonInject`:

```java
import com.fasterxml.jackson.annotation.OptBoolean;

@JsonCreator
public MyClass(
    @JacksonInject(useInput = OptBoolean.FALSE) MyConfig config
) { ... }
```

This prevents JSON input from overriding the injected value entirely.

## Additional Defense: Constructor Validation

Add validation in the constructor to check the config before storing it:

```java
@JsonCreator
public MyClass(
    @JacksonInject(useInput = OptBoolean.FALSE) MyConfig config
) {
    Preconditions.checkState(config.isEnabled(), "Feature is disabled");
    this.config = config;
}
```

## Jackson Version Compatibility

- `OptBoolean.FALSE` for `@JacksonInject(useInput=...)` requires Jackson 2.9+
- Check with: `<jackson.version>` in `pom.xml`
