---
name: scala-domain-modeling
description: Translating Python dynamic structures into type-safe Scala ADTs and case classes.
---

### Domain Modeling Strategy
- **Enums vs Sealed Traits**: Use `sealed trait` for `TokenType` to ensure exhaustive pattern matching.
- **Immutability**: Use `case class` for `Token` to represent immutable data containers.
- **Naming Conventions**: Convert Python's `snake_case` methods/variables to `camelCase` to adhere to Scala idiomatic standards (e.g., `tokenize_batch` becomes `tokenizeBatch`).
- **Data Structures**: Use Scala's `Option[T]` for handling potentially missing metadata or values instead of `None` or `null` checks.