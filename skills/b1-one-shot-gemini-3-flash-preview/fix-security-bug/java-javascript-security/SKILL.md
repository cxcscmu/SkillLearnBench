---
name: java-javascript-security
description: Best practices for securing JavaScript execution in Java applications using ScriptEngines like Rhino or Nashorn.
---

# Java JavaScript Security

When executing JavaScript in a Java application, it is crucial to restrict the capabilities of the script to prevent Arbitrary Code Execution (ACE).

## Vulnerability: Access to Java Classes

By default, many JavaScript engines (like Rhino, which Druid uses) allow the script to access Java classes.

```javascript
var Runtime = java.lang.Runtime;
Runtime.getRuntime().exec("rm -rf /");
```

## Mitigation: Disabling JavaScript if not needed

The best defense is to disable JavaScript execution entirely if it is not required. Apache Druid provides a configuration `druid.javascript.enabled` to control this.

## Mitigation: Sandboxing

If JavaScript must be used, it should be sandboxed.

### Rhino Sandboxing

In Rhino, you can use a `ClassShutter` to restrict which Java classes the script can access.

```java
Context cx = Context.enter();
try {
    cx.setClassShutter(new ClassShutter() {
        @Override
        public boolean visibleToScripts(String fullClassName) {
            return fullClassName.startsWith("org.mycompany.safe.");
        }
    });
    // ...
} finally {
    Context.exit();
}
```

## Mitigation: Input Validation

Always validate the JSON structure and ensure that security-critical configurations (like whether JS is enabled) cannot be overridden by user input. In Druid, this often involves ensuring `@JacksonInject` values are not overridable by JSON properties.
