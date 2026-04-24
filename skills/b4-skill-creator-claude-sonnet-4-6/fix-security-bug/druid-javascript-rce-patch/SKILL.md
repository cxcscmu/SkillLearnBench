---
name: druid-javascript-rce-patch
description: How to patch Apache Druid JavaScript RCE vulnerabilities (CVE-2021-25646 and similar). Use this skill whenever patching Druid JavaScript filter/aggregator security bypass vulnerabilities, when the @JacksonInject config can be overridden via JSON, or when handling arbitrary code execution via JavaScript in Druid sampler/query endpoints.
---

# Apache Druid JavaScript RCE Patch

## Vulnerability Description

In Apache Druid 0.20.x, authenticated attackers can execute arbitrary code via JavaScript payloads in requests to endpoints like `/druid/indexer/v1/sampler`. The exploit uses an empty key `""` in JSON to override the `@JacksonInject JavaScriptConfig` with a custom config that has `enabled: true`, bypassing the server's JavaScript disable setting.

**Exploit pattern:**
```json
{
  "type": "javascript",
  "function": "function(){ java.lang.Runtime.getRuntime().exec('cmd'); }",
  "": { "enabled": true }
}
```

The `""` key triggers Jackson to override the `@JacksonInject`-annotated `JavaScriptConfig` parameter.

## Root Cause

Jackson's `@JacksonInject` by default allows JSON input to override injected values when an unknown key matches. The empty string `""` is treated as a fallback injection key by Jackson's annotation handling, allowing JSON to supply the otherwise-injected `JavaScriptConfig`.

## The Fix

Change all `@JacksonInject JavaScriptConfig config` annotations to:

```java
@JacksonInject(useInput = OptBoolean.FALSE) JavaScriptConfig config
```

The `useInput = OptBoolean.FALSE` tells Jackson to **never** use JSON input for this injected value — it always comes from the server-side injectable values (Guice/ObjectMapper configured `InjectableValues`).

**Required import:**
```java
import com.fasterxml.jackson.annotation.OptBoolean;
```

## Affected Files (Druid 0.20.0)

All 7 files use `@JacksonInject JavaScriptConfig config`:

1. `core/src/main/java/org/apache/druid/data/input/impl/JavaScriptParseSpec.java`
2. `indexing-service/src/main/java/org/apache/druid/indexing/overlord/setup/JavaScriptWorkerSelectStrategy.java`
3. `processing/src/main/java/org/apache/druid/query/aggregation/JavaScriptAggregatorFactory.java`
4. `processing/src/main/java/org/apache/druid/query/aggregation/post/JavaScriptPostAggregator.java`
5. `processing/src/main/java/org/apache/druid/query/extraction/JavaScriptExtractionFn.java`
6. `processing/src/main/java/org/apache/druid/query/filter/JavaScriptDimFilter.java`
7. `server/src/main/java/org/apache/druid/server/router/JavaScriptTieredBrokerSelectorStrategy.java`

## Patch Application Steps

1. For each file, find `@JacksonInject JavaScriptConfig config` in `@JsonCreator` constructor parameters
2. Replace with `@JacksonInject(useInput = OptBoolean.FALSE) JavaScriptConfig config`
3. Add `import com.fasterxml.jackson.annotation.OptBoolean;` if not already present
4. Rebuild affected modules (see druid-maven-build skill)

## Defense in Depth

The existing `Preconditions.checkState(config.isEnabled(), "JavaScript is disabled")` check in each class remains as a second layer of defense. The `useInput = OptBoolean.FALSE` fix prevents the bypass at deserialization time.
