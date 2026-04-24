---
name: scala-trait-and-class-design
description: How to structure abstract base classes, trait hierarchies, and inheritance patterns in Scala for the tokenizer domain.
---

## Trait vs Class Design

### When to Use Traits
- Define contracts/interfaces: `BaseTokenizer` should likely be a trait
- Mix multiple behaviors: traits allow multiple inheritance of type and behavior
- Create sealed trait hierarchies: `sealed trait TokenType`

### When to Use Classes
- When you need constructor parameters that aren't part of the type contract
- When you need mutable state (rare in Scala, but sometimes necessary)
- For concrete implementations that extend traits

## Proper Abstraction for Tokenizer Hierarchy

### Base Abstraction
```scala
trait BaseTokenizer {
  def tokenize(input: String): List[Token]
  // Other abstract methods
}
```

### Concrete Implementations
```scala
class StringTokenizer extends BaseTokenizer {
  override def tokenize(input: String): List[Token] = {
    // implementation
  }
}
```

### Factory/Builder Pattern
- Use companion object's `apply` method for construction
- Use builder for complex configuration
- Avoid passing too many parameters to constructors

## Extension Methods
- For adding utility functions, use Scala 3 extension methods or implicit classes (Scala 2.13)
- Example: add methods to existing classes without inheritance