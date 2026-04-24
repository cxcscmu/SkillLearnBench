---
name: Locate Jackson Deserialization Entry Points in Druid
description: Find the exact code locations where user-supplied JSON is deserialized into DimFilter and other security-sensitive objects in Apache Druid's indexing pipeline, to identify where raw input validation must occur before Jackson processes it.
---

# Locating Jackson Deserialization Entry Points

## Search Strategy

1. **Find Filter Deserialization**
   - Search for `readValue.*DimFilter` across the codebase
   - Search for `objectMapper.readValue` in indexing-service module
   - Search for `transformSpec` parsing and filter extraction
   - Look in `DruidInputSource`, `InputSourceSampler`, and `SamplerResource`

2. **Trace the Request Path**
   - The exploit targets `/druid/indexer/v1/sampler` endpoint
   - Find the corresponding resource handler (likely `SamplerResource.java`)
   - Trace from HTTP request → JSON parsing → object deserialization
   - Identify where `spec.dataSchema.transformSpec.filter` is deserialized

3. **Identify the ObjectMapper Configuration**
   - Find the ObjectMapper instance used for this deserialization
   - Check if it has custom deserializers registered
   - Locate the default deserialization behavior for filters

## Expected Findings

The vulnerable flow should look similar to:
```java
// Somewhere in SamplerResource or InputSourceSampler
String jsonInput = request.getBody();  // Raw JSON from attacker
ObjectMapper mapper = new ObjectMapper();
DataSchema schema = mapper.readValue(jsonInput, DataSchema.class);
// At this point, the empty key "" has already bypassed security
DimFilter filter = schema.getTransformSpec().getFilter();
```

## Key Files to Examine

- `druid-indexing-service/src/main/java/org/apache/druid/indexing/overlord/sampler/SamplerResource.java`
- `druid-indexing-service/src/main/java/org/apache/druid/indexing/overlord/sampler/InputSourceSampler.java`
- `druid-core/src/main/java/org/apache/druid/segment/transform/TransformSpec.java`
- `druid-core/src/main/java/org/apache/druid/query/filter/DimFilter.java`

## Validation Approach

Once the entry point is found, the fix must:
1. **Validate raw JSON string** before passing to `ObjectMapper.readValue()`
2. **Reject empty keys** `""` at the input stream level
3. **Prevent bypass of JavaScript security** via malformed JSON structures