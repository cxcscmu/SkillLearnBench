---
name: python-scala-generics-mapping
description: Guidelines for translating Python TypeVars and Protocols to Scala Generics and Traits.
---

# Python to Scala Generics Mapping

## Variance
- **Invariant**: Python `TypeVar("T")` -> Scala `[T]`
- **Covariant**: Python `TypeVar("T_co", covariant=True)` -> Scala `[+T]`
- **Contravariant**: Python `TypeVar("T_contra", contravariant=True)` -> Scala `[-T]`

## Structural Typing (Protocols)
- Python `Protocol` -> Scala `trait`. 
- If structural typing is strictly required in Scala, use "duck typing" via `import scala.language.reflectiveCalls`, but standard `trait` with inheritance is preferred for performance and type safety.

## Type Bounds
- Python `TypeVar("T", bound=Class)` -> Scala `[T <: Class]`
- Python `TypeVar("T", int, float)` -> Scala doesn't have Union types in 2.13 in this specific way. Use `Either`, `sealed trait` hierarchies, or Type Classes (e.g., `Numeric[T]`).
