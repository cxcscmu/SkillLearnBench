---
name: druid-javascript-security
description: Specific guidance for securing JavaScript execution in Apache Druid. Use this when working with JavaScriptDimFilter, JavaScriptExtractionFn, JavaScriptAggregatorFactory, and other JS-enabled components.
---

# Druid JavaScript Security

## Core Components
The following classes are primary targets for JavaScript-based attacks:
- `JavaScriptDimFilter`
- `JavaScriptExtractionFn`
- `JavaScriptAggregatorFactory`
- `JavaScriptPostAggregator`
- `JavaScriptParseSpec`
- `JavaScriptTieredBrokerSelectorStrategy`
- `JavaScriptWorkerSelectStrategy`

## Hardening Pattern
1. **Disable Input for Config Injection**: Use `@JacksonInject(useInput = OptBoolean.FALSE) JavaScriptConfig config` in constructors.
2. **Explicit Creator Mode**: Use `@JsonCreator(mode = JsonCreator.Mode.PROPERTIES)` to be explicit about how Jackson should treat the constructor.
3. **Late Validation**: Ensure `config.isEnabled()` is checked right before script compilation or execution.

## Example of a Patched Constructor
```java
  @JsonCreator
  public JavaScriptDimFilter(
      @JsonProperty("dimension") String dimension,
      @JsonProperty("function") String function,
      @JsonProperty("extractionFn") @Nullable ExtractionFn extractionFn,
      @JsonProperty("filterTuning") @Nullable FilterTuning filterTuning,
      @JacksonInject(useInput = OptBoolean.FALSE) JavaScriptConfig config
  )
```
