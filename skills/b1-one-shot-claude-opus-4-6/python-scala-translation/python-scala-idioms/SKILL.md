---
name: python-scala-idioms
description: Guide for writing idiomatic Scala including naming conventions, error handling, and pattern matching.
---

# Scala Idioms and Conventions

## Naming Conventions
- Classes/Traits: `PascalCase`
- Methods/Fields: `camelCase` (not `snake_case`)
- Constants: `PascalCase` in companion objects or `UPPER_CASE` for enum-like
- Package: `lowercase`
- Type parameters: single uppercase letter `T`, `A`, `B`

## Error Handling
```scala
// Python: raise ValueError -> Scala: throw or Either/Try
// Prefer Option for absence, Either/Try for errors
def tokenizePath(value: Json, path: String): Option[Token]
```

## Pattern Matching (replaces isinstance chains)
```scala
// Python: if isinstance(value, str): ...
// Scala:
value match {
  case s: String => ...
  case i: Int    => ...
  case _         => ...
}
```

## String Interpolation
```scala
// Python: f"{value:.6f}" -> Scala: f"$value%.6f" or s"$value"
```

## Companion Objects
```scala
// Factory methods, constants go in companion objects
object TemporalTokenizer {
  val IsoFormat = "yyyy-MM-dd'T'HH:mm:ss"
  val DateFormat = "yyyy-MM-dd"
}
```
