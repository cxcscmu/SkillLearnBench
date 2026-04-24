---
name: run2_jackson-security
description: Security considerations for Jackson JSON deserialization in Java, focusing on @JacksonInject bypass vulnerabilities via empty property names ("").
---
# Jackson Security: @JacksonInject Bypass Vulnerability

## Concept
In Jackson, `@JacksonInject` is used to inject values into properties or constructor parameters during deserialization without expecting those values to come from the JSON payload itself. However, due to how Jackson's `AnnotationIntrospector` and fallback behaviors work, if a `@JacksonInject` annotated parameter does not explicitly have a `@JsonProperty` annotation, an attacker may be able to supply a JSON property with an empty string key (`""`) and bypass the injection mechanism. 

This causes Jackson to deserialize the attacker's JSON value and bind it to the parameter instead of using the properly injected, trusted value.

## Real-world Example (CVE-2021-25646 in Apache Druid)
Apache Druid used `@JacksonInject` for a `JavaScriptConfig` object in its `JavaScriptDimFilter`. By supplying `"": {"enabled": true}`, an attacker overrode the globally disabled JS config with an enabled one, allowing arbitrary code execution.

```java
@JsonCreator
public JavaScriptDimFilter(
    @JsonProperty("dimension") String dimension,
    @JsonProperty("function") String function,
    // Vulnerable: no @JsonProperty, an empty string key "" will bind to this!
    @JacksonInject JavaScriptConfig config 
)
```

## Mitigation
To mitigate this class of vulnerabilities at the framework level, you can implement a custom `AnnotationIntrospector` that refuses to parse empty string property names for parameters that don't explicitly specify one using `@JsonProperty`.

```java
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.introspect.Annotated;
import com.fasterxml.jackson.databind.introspect.AnnotatedParameter;
import com.fasterxml.jackson.databind.introspect.NopAnnotationIntrospector;

public class SecureAnnotationIntrospector extends NopAnnotationIntrospector {
    @Override
    public JsonIgnoreProperties.Value findPropertyIgnorals(Annotated ac) {
        if (ac instanceof AnnotatedParameter) {
            final AnnotatedParameter ap = (AnnotatedParameter) ac;
            if (ap.hasAnnotation(JsonProperty.class)) {
                return JsonIgnoreProperties.Value.empty();
            }
        }
        // Deny empty string property names to prevent @JacksonInject bypasses
        return JsonIgnoreProperties.Value.forIgnoredProperties("");
    }
}
```

This `SecureAnnotationIntrospector` should then be registered with your `ObjectMapper` using an `AnnotationIntrospectorPair`.
