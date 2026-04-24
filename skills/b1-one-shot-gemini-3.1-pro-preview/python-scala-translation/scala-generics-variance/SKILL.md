---
name: scala-generics-variance
description: Guide for translating Python TypeVars and generics to Scala covariant and contravariant types.
---

# Generics and Variance in Scala

Python's typing module provides `TypeVar` to represent generics, including covariant and contravariant parameters. Scala has built-in support for declaration-site variance.

## Type Parameters
- **Invariant**: `class MyClass[A]` (Must be exact type, like Python `TypeVar("T")`)
- **Covariant**: `class MyClass[+A]` (Can be subtype, like Python `TypeVar("T_co", covariant=True)`)
- **Contravariant**: `class MyClass[-A]` (Can be supertype, like Python `TypeVar("T_contra", contravariant=True)`)

### Example: Covariant Container
Python:
```python
T_co = TypeVar("T_co", covariant=True)
class Container(Generic[T_co]):
    def __init__(self, items: Sequence[T_co]):
        self._items = tuple(items)
    def get_all(self) -> tuple[T_co, ...]:
        return self._items
```
Scala:
```scala
class Container[+A](items: Seq[A]) {
  private val _items: Vector[A] = items.toVector
  def getAll: Vector[A] = _items
}
```

### Protocols vs Traits
Python `Protocol` allows duck-typing, but Scala requires nominal typing via `trait`.
Python:
```python
class Tokenizable(Protocol):
    def to_token(self) -> str: ...
```
Scala:
```scala
trait Tokenizable {
  def toToken: String
}
```
If an object needs to implement this, it must explicitly `extend Tokenizable`.
