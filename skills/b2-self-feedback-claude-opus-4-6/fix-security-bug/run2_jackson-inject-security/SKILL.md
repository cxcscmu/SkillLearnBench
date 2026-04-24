---
name: run2_jackson-inject-security
description: Preventing Jackson @JacksonInject bypass via empty JSON keys by using OptBoolean.FALSE to reject user-supplied input for injected parameters.
---

# Jackson @JacksonInject Security: Preventing Input Override

## Vulnerability
Jackson's `@JacksonInject` allows server-injected values to be overridden by JSON input. An attacker can use an empty key `""` in the JSON payload to inject a custom object that replaces the server-configured value.

### How the Empty Key Attack Works
When Jackson deserializes a class with `@JacksonInject`:
1. It first sets the injected value from `InjectableValues`
2. Then it processes JSON properties, including empty-string keys `""`
3. The empty key `""` can match the injectable parameter, overriding the server value

### Example Attack Payload
```json
{
  "type": "javascript",
  "dimension": "dim",
  "function": "function(x){java.lang.Runtime.getRuntime().exec('cmd')}",
  "": {"enabled": true}
}
```

## Fix: Use `OptBoolean.FALSE`

### Code Change
```java
// BEFORE (vulnerable):
import com.fasterxml.jackson.annotation.JacksonInject;

@JsonCreator
public MyClass(@JacksonInject MyConfig config) { ... }

// AFTER (secure):
import com.fasterxml.jackson.annotation.JacksonInject;
import com.fasterxml.jackson.annotation.OptBoolean;

@JsonCreator
public MyClass(@JacksonInject(useInput = OptBoolean.FALSE) MyConfig config) { ... }
```

### What `useInput = OptBoolean.FALSE` Does
- Tells Jackson to NEVER use JSON input for this parameter
- Only the server-injected value from `InjectableValues` is used
- Any JSON property (including empty key `""`) attempting to set this parameter is ignored

### Compatibility
- Requires Jackson 2.9+ (available in Jackson 2.10.2 used by Druid 0.20.0)
- `com.fasterxml.jackson.annotation.OptBoolean` import required

## Patch Generation Workflow
```bash
# 1. Make changes to source files
# 2. Generate unified diff patch
cd /root/druid && git diff > /root/patches/fix.patch

# 3. To apply on clean repo:
cd /root/druid && git apply /root/patches/fix.patch

# 4. Build specific module with all dependencies:
mvn clean package -DskipTests -Dcheckstyle.skip=true -Dpmd.skip=true \
  -Dforbiddenapis.skip=true -Dspotbugs.skip=true -Danimal.sniffer.skip=true \
  -Denforcer.skip=true -Djacoco.skip=true -Ddependency-check.skip=true \
  -pl '!web-console' -pl indexing-service -am
```
