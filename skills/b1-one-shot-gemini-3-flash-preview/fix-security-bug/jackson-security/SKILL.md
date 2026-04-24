---
name: jackson-security
description: Security considerations for Jackson JSON deserialization, specifically regarding `@JacksonInject` and unintended property overrides.
---

# Jackson Security: `@JacksonInject` and Property Overrides

In Jackson, `@JacksonInject` is used to inject values from the `InjectableValues` of the `ObjectMapper`. However, by default, if a property with the same name exists in the JSON, it might override the injected value, or Jackson might try to bind the JSON property to that parameter.

## Vulnerability: Injected Value Override

If an attacker can provide a property in the JSON that matches the name of an injected parameter, they might be able to control that parameter.

### Example

```java
public class MyObject {
  private final String secret;
  private final boolean enabled;

  @JsonCreator
  public MyObject(
    @JsonProperty("secret") String secret,
    @JacksonInject boolean enabled
  ) {
    this.secret = secret;
    this.enabled = enabled;
  }
}
```

If the `InjectableValues` has `enabled = false`, but the JSON is `{"secret": "foo", "enabled": true}`, Jackson might set `enabled` to `true`.

## Mitigation: useInput = false

To prevent this, you should set `useInput = false` in the `@JacksonInject` annotation.

```java
  @JsonCreator
  public MyObject(
    @JsonProperty("secret") String secret,
    @JacksonInject(useInput = false) boolean enabled
  ) {
    // ...
  }
```

When `useInput = false`, Jackson will ONLY use the injected value and will ignore any value for this property in the JSON input.

## The Empty Key `""` Bypass

In some versions of Jackson or specific configurations, an empty key `""` might be treated specially, sometimes being mapped to the "default" or "root" of some internal structure, potentially bypassing name-based checks or matching unnamed injected parameters.

If a `@JacksonInject` is used without a name, Jackson might use the type name or parameter name. If an attacker uses `""`, it might under certain circumstances be matched to an unnamed or specifically named injectable.
