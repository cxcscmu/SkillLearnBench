---
name: scala-data-modeling
description: Modeling domain entities and transformations using case classes, companion objects, and type-safe hierarchies.
---

## Modeling Strategies
- **Case Classes:** Use `case class` for immutable data structures. They provide structural equality, pattern matching support, and a concise syntax.
- **Companion Objects:** Place factory methods, default values, and related logic in a `companion object`.
- **ADT (Algebraic Data Types):** Combine `sealed trait` with `case class`/`case object` for type-safe modeling of heterogeneous data.
- **Type Aliases:** Use `type` for simplifying complex types.

## Example
```scala
sealed trait TokenValue
case class StringVal(s: String) extends TokenValue
case class NumericVal(n: Double) extends TokenValue

case class Token(value: TokenValue, metadata: Map[String, String] = Map.empty)

object Token {
  def apply(s: String): Token = new Token(StringVal(s))
}
```
