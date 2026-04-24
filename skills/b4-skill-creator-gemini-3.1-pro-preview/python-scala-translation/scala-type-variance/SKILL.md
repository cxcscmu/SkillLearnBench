---
name: scala-type-variance
description: Translating Python TypeVar variance to Scala. Use this skill whenever you see T_co or T_contra in Python and need to write equivalent Scala traits or classes.
---
# Scala Type Variance

- Python `TypeVar("T_co", covariant=True)` -> Scala `[+T]` (Covariant).
- Python `TypeVar("T_contra", contravariant=True)` -> Scala `[-T]` (Contravariant).
- Python `TypeVar("T")` -> Scala `[T]` (Invariant).

## Invariance, Covariance, Contravariance rules in Scala
- **Covariant types `[+T]`** can only appear in covariant positions (e.g., return types of methods). If you need to accept `T` in a method parameter, use a lower type bound: `def method[U >: T](val: U)`.
- **Contravariant types `[-T]`** can only appear in contravariant positions (e.g., arguments of methods). If you need to return `T`, use an upper type bound: `def method[U <: T](): U`.
- Mutable collections (like `ArrayBuffer` or `mutable.Map`) are invariant `[T]`. 
- Immutable collections (like `List`, `Vector`) are covariant `[+T]`.
- Scala functions `A => B` are contravariant in `A` and covariant in `B`: `[-A, +B]`.
