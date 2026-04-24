---
name: scala-213-type-hierarchy-and-modeling
description: Define idiomatic Scala 2.13 type hierarchies and domain models, replacing Python's class structures and Enums with traits and case classes.
---

### Sealed Traits and Case Objects for Enums
Scala 2.13 does not support the `enum` keyword. To represent a fixed set of types (like `TokenType`):
1. Define a `sealed trait` as the base type.
2. Define `case object` instances for each specific type.
This ensures exhaustiveness checking during pattern matching.

### Class Hierarchies
Replace Python base classes with a `sealed trait` or `abstract class` for the `BaseTokenizer`.
- Use a `trait` if you only define an interface.
- Use an `abstract class` if you need to provide common constructor parameters or shared logic for all tokenizers.

### Data Representation
Use `case class` for the `Token` model. Case classes provide:
- Immutability by default.
- Built-in `equals`, `hashCode`, and `toString`.
- A `.copy()` method, which is essential for the `withMetadata` pattern.

### The `withMetadata` Pattern
To implement `withMetadata` idiomatically, leverage the `.copy()` method of the `Token` case class. This allows you to return a new instance with updated fields without mutating the original object, maintaining functional purity.