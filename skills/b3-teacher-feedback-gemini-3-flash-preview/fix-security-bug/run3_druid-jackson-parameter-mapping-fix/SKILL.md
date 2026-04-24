---
name: druid-jackson-parameter-mapping-fix
description: Securing Jackson deserialization in Druid to prevent user-supplied JSON keys from overriding system-injected security configurations.
---

1. **Analyze Constructor Annotations**:
   Examine the `@JsonCreator` constructors of JavaScript-related classes. Locate the `JavaScriptConfig` parameter.

2. **Identify the Bypass Mechanism**:
   The vulnerability exists because Jackson may map unexpected JSON keys (like the empty string `""`) to object properties if the mapping is ambiguous. If a `JavaScriptConfig` parameter is present in a constructor but not strictly bound to a specific property or is incorrectly handled by `@JacksonInject`, a malicious payload can provide its own "enabled: true" configuration.

3. **Apply Explicit Injection**:
   To fix the mapping, ensure the `JavaScriptConfig` parameter is purely injected and not mapped from JSON properties. 
   - Use `@JacksonInject` without a corresponding `@JsonProperty` for the config parameter.
   - If `@JsonProperty` is present on the config parameter, remove it or ensure it does not conflict with the system injection.
   - Example of a secure pattern:
     ```java
     @JsonCreator
     public JavaScriptDimFilter(
         @JsonProperty("dimension") String dimension,
         @JsonProperty("function") String function,
         ...
         @JacksonInject JavaScriptConfig config // No @JsonProperty here
     )
     ```

4. **Audit for Hidden Overrides**:
   Check if the class has a setter for `JavaScriptConfig` or a public field that Jackson might automatically discover. These must be removed or annotated with `@JsonIgnore`.