---
name: run2_scala-variance
description: Expressing variance annotations in Scala generics when translating from Python TypeVar covariant/contravariant types.
---

# Variance in Scala

## Mapping from Python TypeVar
- `TypeVar("T_co", covariant=True)` -> `[+T]` (covariant)
- `TypeVar("T_contra", contravariant=True)` -> `[-T]` (contravariant)
- `TypeVar("T")` -> `[T]` (invariant)

## Covariant Container
```scala
class TokenContainer[+T](items: Seq[T]) {
  // Can return T but not accept T as parameter in public methods
  def getAll: Vector[T] = items.toVector
}
```

## Contravariant Sink
```scala
class TokenSink[-T] {
  // Can accept T but not return T
  private val received = mutable.ListBuffer[Any]()
  def receive(item: T): Unit = received += item
  def drain(): List[Any] = { ... }
}
```

## Invariant Handler
```scala
class BivariantHandler[T](default: T) {
  // Both accepts and returns T
  def get: T = ...
  def set(value: T): Unit = ...
}
```
