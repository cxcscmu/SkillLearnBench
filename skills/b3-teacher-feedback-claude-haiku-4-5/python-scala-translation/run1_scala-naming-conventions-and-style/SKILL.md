---
name: scala-naming-conventions-and-style
description: Scala-specific naming conventions, code organization patterns, and style guidelines that differ from Python conventions.
---

## Scala Naming Conventions

### Classes, Traits, and Objects
- **PascalCase** for class names: `TokenType`, `BaseTokenizer`, `UniversalTokenizer`
- **PascalCase** for trait names and sealed traits
- **camelCase** for object names if singleton: `TokenizerBuilder` (if companion object, use same name as class)
- **UPPER_SNAKE_CASE** for constants and enum-like values

### Functions and Variables
- **camelCase** for method and variable names: `tokenize`, `tokenizeBatch`, `toToken`, `withMetadata`
- **camelCase** for parameters: `input`, `maxLength`, `delimiter`
- Use descriptive names; avoid single letters except in lambda expressions or mathematical contexts

### Package Organization
- Lowercase package names: `com.example.tokenizer`
- Structure: separate classes/traits from utility objects
- One public class per file is conventional (but not required)

### Code Style
- No underscore prefix for private fields; use `private` modifier
- Prefer `val` over `var` (immutability first)
- Use method chaining and builder patterns for fluent APIs
- Indent with 2 spaces (Scala convention)

## Scala-Specific Patterns

### Sealed Traits for Enums
```scala
sealed trait TokenType
case object StringToken extends TokenType
case object NumericToken extends TokenType
```

### Case Classes for Data
```scala
case class Token(
  value: String,
  tokenType: TokenType,
  position: Int,
  metadata: Map[String, String] = Map.empty
)
```

### Builder Pattern
```scala
class TokenizerBuilder {
  private var config: Map[String, Any] = Map.empty
  def withOption(key: String, value: Any): TokenizerBuilder = {
    config = config + (key -> value)
    this
  }
  def build(): Tokenizer = new Tokenizer(config)
}
```