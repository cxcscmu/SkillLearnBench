---
name: run2_scala-idiomatic-patterns
description: Idiomatic Scala patterns for translating Python code including enums, case classes, and naming conventions.
---

# Idiomatic Scala Patterns

## Enums (Scala 2.13)
Use `sealed abstract class` with companion object containing `case object`s:
```scala
sealed abstract class TokenType(val value: String)
object TokenType {
  case object STRING extends TokenType("string")
}
```

## Case Classes for Immutable Data
- Python `@dataclass(frozen=True)` -> Scala `case class`
- Use `copy()` for creating modified instances
- Default params replace `field(default_factory=...)`

## Naming Conventions
- camelCase for methods/fields: `tokenize_batch` -> `tokenizeBatch`
- PascalCase for types: same in both languages
- Avoid `_` prefix for private fields; use `private` modifier

## Avoid `var` and `return`
- Use `Option` chains, `match`, and `foldLeft` instead of mutable vars
- Use expression-oriented style: every block returns a value
- Prefer `val` over `var` wherever possible

## Pattern Matching over isinstance
Python `isinstance(value, (str, bytes))` becomes Scala pattern matching:
```scala
value match {
  case s: String => ...
  case d: Double => ...
}
```
