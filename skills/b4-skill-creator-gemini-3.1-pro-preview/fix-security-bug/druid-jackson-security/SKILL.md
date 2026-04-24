---
name: druid-jackson-security
description: Securing Apache Druid's JavaScriptConfig deserialization. Use this skill whenever patching or securing Jackson deserialization in Druid, especially regarding the empty key ("") bypass.
---

# Druid Jackson Deserialization Security

## The Vulnerability

In Apache Druid 0.20.0, a vulnerability exists where authenticated attackers can execute arbitrary code by passing malicious JavaScript payloads. The vulnerability exploits a known Jackson deserialization behavior: when a class constructor uses `@JacksonInject` without specifying a property name or disabling user input, Jackson defaults the property name to `""` (empty string).

Attackers can provide an empty key (`""`) in the JSON payload to override the safely injected `JavaScriptConfig` instance with a malicious one where `enabled` is set to `true`. This bypasses Druid's internal check that disables JavaScript by default.

Example Payload Fragment:
```json
{
  "type": "javascript",
  "function": "function(){java.lang.Runtime.getRuntime().exec('malicious_command');}",
  "": {
    "enabled": true
  }
}
```

## The Fix

To remediate this vulnerability, we must prevent JSON input from overriding the injected `JavaScriptConfig`. Jackson provides the `OptBoolean.FALSE` value for the `useInput` attribute of the `@JacksonInject` annotation precisely for this purpose.

For every occurrence of `@JacksonInject JavaScriptConfig` inside a `@JsonCreator` constructor, modify the annotation to explicitly reject input data:

```java
import com.fasterxml.jackson.annotation.OptBoolean;

// ...

@JsonCreator
public MyJavaScriptComponent(
    // ...
    @JacksonInject(useInput = OptBoolean.FALSE) JavaScriptConfig config
)
```

By adding `useInput = OptBoolean.FALSE`, Jackson will ignore any JSON property (including `""`) that attempts to bind to the `config` parameter, and will exclusively use the `JavaScriptConfig` instance provided by the Guice injector.

## Affected Classes

You should locate and patch the following classes that inject `JavaScriptConfig`:
1. `JavaScriptWorkerSelectStrategy.java`
2. `JavaScriptPostAggregator.java`
3. `JavaScriptAggregatorFactory.java`
4. `JavaScriptExtractionFn.java`
5. `JavaScriptDimFilter.java`
6. `JavaScriptParseSpec.java`
7. `JavaScriptTieredBrokerSelectorStrategy.java`
