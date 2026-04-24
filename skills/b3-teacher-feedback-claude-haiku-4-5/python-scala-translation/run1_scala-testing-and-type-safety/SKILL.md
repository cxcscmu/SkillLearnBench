---
name: scala-testing-and-type-safety
description: Scala's type system features, testing patterns, and integration with test specifications for ensuring correctness of translated code.
---

## Scala Type Safety

### Explicit Type Annotations
- Always annotate public method return types
- Use specific types, not `Any`
```scala
def tokenize(input: String): List[Token] = { ... }
```

### Generic Types
```scala
class Container[T](value: T) {
  def get: T = value
}
```

### Type Bounds
- Use upper bounds for constraints: `T <: BaseType`
- Use lower bounds when appropriate: `T >: BaseType`

## Reading Test Specifications

### Understanding Expected Signatures
- Review `/root/TokenizerSpec.scala` for method signatures
- Note parameter types and return types exactly
- Identify any builder patterns or fluent API requirements
- Check for implicit parameters or type classes

### Common Test Patterns
- Test construction: how objects are instantiated
- Test core functionality: main methods work as expected
- Test edge cases: empty input, special characters, boundary conditions
- Test composition: methods work together correctly

## Compilation and Type Checking

### Scala 2.13 Compatibility
- Avoid Scala 3-only features
- Use standard library features available in 2.13
- Be aware of deprecations and use stable APIs

### Compiler Errors
- Type mismatches are caught at compile time
- Use the Scala REPL or `scalac` to verify code
- Pay attention to implicit resolution errors

## Property-Based Testing Concepts
- Even though you won't write tests, understand that test specs often verify:
  - Invariants (properties that always hold)
  - Round-trip properties (encode/decode consistency)
  - Composition properties (f(g(x)) behaves correctly)