---
name: druid-javascript-rce
description: Apache Druid JavaScript RCE vulnerability (CVE-2021-25646) fix via @JacksonInject hardening and constructor validation.
---

# Apache Druid JavaScript RCE Vulnerability

## Overview

Apache Druid 0.20.0 allows authenticated users to execute arbitrary server-side code through JavaScript-based features (filters, aggregators, extraction functions, etc.) even when JavaScript is disabled via `druid.javascript.enabled=false`.

## Root Cause

All JavaScript-related classes use `@JacksonInject JavaScriptConfig config` to receive the server-side JavaScript configuration. Jackson's default behavior allows JSON input to override injected values via an empty key `""`.

## Affected Classes

1. `JavaScriptDimFilter` - processing module
2. `JavaScriptAggregatorFactory` - processing module
3. `JavaScriptExtractionFn` - processing module
4. `JavaScriptPostAggregator` - processing module
5. `JavaScriptParseSpec` - core module
6. `JavaScriptTieredBrokerSelectorStrategy` - server module (already has constructor check)

## Fix Strategy

For each affected class:
1. Change `@JacksonInject` to `@JacksonInject(useInput = OptBoolean.FALSE)`
2. Add `Preconditions.checkState(config.isEnabled(), "JavaScript is disabled")` in constructors that don't already have it

## Exploit Payload Example

```json
{
  "type": "index",
  "spec": {
    "dataSchema": {
      "transformSpec": {
        "filter": {
          "type": "javascript",
          "dimension": "dim",
          "function": "function(x){java.lang.Runtime.getRuntime().exec('cmd')}",
          "": {"enabled": true}
        }
      }
    }
  }
}
```

## Modules Requiring Rebuild

- `druid-core` (JavaScriptParseSpec)
- `druid-processing` (JavaScriptDimFilter, JavaScriptAggregatorFactory, JavaScriptExtractionFn, JavaScriptPostAggregator)
- `druid-server` (JavaScriptTieredBrokerSelectorStrategy)
- `druid-indexing-service` (sampler endpoint, depends on above)
