---
name: scala-functional-idioms
description: Idiomatic functional programming in Scala using sealed traits, pattern matching, and Option/Either for robust error handling.
---

## Key Patterns
- **Sealed Hierarchies:** Use `sealed trait` for domain models (e.g., ADTs) to enable exhaustiveness checking in pattern matching.
- **Option/Either:** Prefer `Option[T]` for missing values and `Either[E, T]` for operations that can fail, avoiding nulls and throwing exceptions.
- **Expression-Oriented:** Leverage Scala's expression-based style over imperative statements.
- **Pattern Matching:** Use `match` expressions for data decomposition and control flow.

## Example
```scala
sealed trait Result
case class Success(value: String) extends Result
case class Failure(reason: String) extends Result

def process(input: Option[String]): Result = input match {
  case Some(s) if s.nonEmpty => Success(s.toUpperCase)
  case _ => Failure("Invalid input")
}
```
