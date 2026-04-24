---
name: apache-druid-security
description: Security patching for Apache Druid - covers JavaScript execution vulnerabilities, sampler endpoint protection, and filter validation patterns.
---

# Apache Druid Security Patching

## Overview
Apache Druid is a real-time analytics database. Key security concern: JavaScript execution via
filter/transform specs in ingestion tasks and the sampler endpoint.

## CVE-2021-25646 - JavaScript Filter RCE

### Vulnerability Mechanism
- `JavaScriptDimFilter` uses `@JacksonInject JavaScriptConfig config` to get JavaScript enabled status
- `@JacksonInject` with default `value=""` allows Jackson to fall back to JSON input when the
  injectable value isn't found or when `useInput=OptBoolean.DEFAULT`
- Exploit: Send `"": {"enabled": true}` in the filter JSON to inject a permissive `JavaScriptConfig`
- This bypasses the server-level `druid.javascript.enabled=false` setting
- The Rhino JS engine has no `ClassShutter` → full Java class access → `Runtime.exec()` possible

### Affected Files
- `processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java`
- `indexing-service/src/main/java/org/apache/druid/indexing/overlord/sampler/InputSourceSampler.java`
- `core/src/main/java/org/apache/druid/js/JavaScriptConfig.java`

### Fix 1: Block JSON Override of @JacksonInject (Root Cause)
```java
// In JavaScriptDimFilter constructor, add useInput = OptBoolean.FALSE:
import com.fasterxml.jackson.annotation.OptBoolean;

@JsonCreator
public JavaScriptDimFilter(
    @JsonProperty("dimension") String dimension,
    @JsonProperty("function") String function,
    @JsonProperty("extractionFn") @Nullable ExtractionFn extractionFn,
    @JsonProperty("filterTuning") @Nullable FilterTuning filterTuning,
    @JacksonInject(useInput = OptBoolean.FALSE) JavaScriptConfig config  // KEY FIX
)
```

### Fix 2: Server-Side Validation in Sampler (Defense in Depth)
```java
// In InputSourceSampler.java - inject JavaScriptConfig via Guice:
import com.google.inject.Inject;
import org.apache.druid.js.JavaScriptConfig;
import org.apache.druid.query.filter.JavaScriptDimFilter;

public class InputSourceSampler {
    private final JavaScriptConfig javascriptConfig;

    @Inject
    public InputSourceSampler(JavaScriptConfig javascriptConfig) {
        this.javascriptConfig = javascriptConfig;
    }

    public SamplerResponse sample(...) {
        // Add BEFORE processing:
        if (!javascriptConfig.isEnabled()) {
            validateNoJavaScriptFilter(nonNullDataSchema.getTransformSpec().getFilter());
        }
    }

    private void validateNoJavaScriptFilter(@Nullable DimFilter filter) {
        if (filter instanceof JavaScriptDimFilter) {
            throw new SamplerException("JavaScript is disabled. Set druid.javascript.enabled=true to enable.");
        }
        // Also handle composite filters (AND/OR/NOT)
    }
}
```

## Key Architecture Notes

### JavaScript Execution Path
1. `POST /druid/indexer/v1/sampler` → `SamplerResource.post()`
2. → `IndexTaskSamplerSpec.sample()` → `InputSourceSampler.sample()`
3. → `dataSchema.getTransformSpec().decorate(reader)`
4. → `TransformingInputSourceReader` → `Transformer`
5. → `filter.toFilter()` → `JavaScriptDimFilter.getPredicateFactory()` ← security check is here

### Guice-Managed Components
- `InputSourceSampler` is bound as `Singleton` in `SamplerModule`
- `JavaScriptConfig` is bound in `JavaScriptModule` from `druid.javascript` config
- Jackson `@JacksonInject` uses Guice's `InjectableValues` when available

## Build Command
```bash
cd /root/druid
mvn clean package -DskipTests -Dcheckstyle.skip=true -Dpmd.skip=true \
  -Dforbiddenapis.skip=true -Dspotbugs.skip=true -Danimal.sniffer.skip=true \
  -Denforcer.skip=true -Djacoco.skip=true -Ddependency-check.skip=true \
  -pl '!web-console' -pl indexing-service -am
```
