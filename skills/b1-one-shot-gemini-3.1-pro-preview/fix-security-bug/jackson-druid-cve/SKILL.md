---
name: jackson-druid-cve
description: Security and Jackson deserialization issues in Apache Druid, focusing on property bypasses.
---

# Jackson Deserialization Security in Druid

When dealing with Jackson, unknown properties or empty properties can sometimes be mapped to configuration objects or bypass validation if `@JsonCreator` is not carefully constrained. This can lead to security vulnerabilities.

In Apache Druid, configuration classes like `JavaScriptConfig` are often passed via dependency injection or default constructors, and mapped from JSON if not disabled.

## Techniques
- Restricting JSON properties using `@JsonIgnoreProperties`
- Throwing exceptions on unknown properties
- Ensuring that `@JacksonInject` or required properties cannot be overridden by user input like `""`.