---
name: druid-javascript-security
description: Securing Apache Druid's JavaScript execution engine against code injection and security bypass attacks.
---

# Apache Druid JavaScript Security

## Vulnerability Context

Apache Druid versions up to 0.20.0 have a critical vulnerability in JavaScript expression handling where an empty key (`""`) can bypass security settings, allowing arbitrary code execution through the `java.lang.Runtime` API.

## Key Components

### 1. JavaScript Transform Spec
- Located in indexing service modules
- Handles JavaScript expressions for data transformation
- Uses GraalVM or Nashorn engine for JavaScript execution

### 2. Security Filter Structure
The vulnerable structure looks like:
```json
{
  "filter": {
    "type": "javascript",
    "function": "function(){...}",
    "": {
      "enabled": true
    }
  }
}
```

The empty key `""` is the bypass vector.

## Patching Strategy

### 1. Input Validation
- Reject filter/transform specs with empty string keys
- Validate all keys in security configuration objects
- Enforce strict schema validation before passing to JavaScript engine

### 2. Security Configuration Enforcement
- Ensure `enabled` flag is only checked for known, valid keys
- Implement whitelist of allowed configuration keys
- Reject any configuration with unexpected keys

### 3. Code Changes Needed
- Typically in classes handling JavaScript filter/transform deserialization
- Common classes: `JavaScriptFilter`, `JavaScriptExpressionValidator`, JavaScript spec handlers
- May need to add validation in both request parsing and execution phases

## Testing the Fix

### Exploit Request (should fail)
```http
POST /druid/indexer/v1/sampler
{
  "type": "index",
  "spec": {
    "dataSchema": {
      "transformSpec": {
        "filter": {
          "type": "javascript",
          "function": "function(){java.lang.Runtime.getRuntime().exec('malicious_command');}",
          "": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

### Legitimate Request (should work)
```http
POST /druid/indexer/v1/sampler
{
  "type": "index",
  "spec": {
    "dataSchema": {
      "transformSpec": {
        "filter": {
          "type": "javascript",
          "function": "function(row){return true;}"
        }
      }
    }
  }
}
```

## Common Druid File Locations

- JavaScript filter implementation: `processing/src/main/java/org/apache/druid/query/filter/JavaScriptFilter.java`
- Indexing service: `indexing-service/src/main/java/org/apache/druid/indexing/`
- Transform specs: Related to dataSchema handling

## Jackson Deserialization Considerations

The vulnerability likely involves improper validation during Jackson deserialization. Use raw `@JsonAnySetter` or similar mechanisms to catch unexpected properties and validate them strictly before further processing.
