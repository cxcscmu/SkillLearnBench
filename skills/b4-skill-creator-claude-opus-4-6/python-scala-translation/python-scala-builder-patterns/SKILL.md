---
name: python-scala-builder-patterns
description: >
  Translating Python builder patterns, fluent interfaces, and factory functions
  to Scala. Use when converting Python classes with method chaining, __init__
  with mutable lists/dicts, or builder/factory patterns to idiomatic Scala with
  immutable state and companion objects.
---

# Python Builder & Factory Patterns to Scala

## Fluent Builder with Immutable State

Python builder uses mutable lists and returns `self`:
```python
class TokenizerBuilder(Generic[T]):
    def __init__(self):
        self._normalizers = []
    def with_normalizer(self, n):
        self._normalizers.append(n)
        return self
```

Scala idiomatic approach — use a case class with `copy()`:
```scala
case class TokenizerBuilder[T](
  normalizers: List[String => String] = Nil,
  validators: List[T => Boolean] = Nil,
  metadata: Map[String, Any] = Map.empty
) {
  def withNormalizer(f: String => String): TokenizerBuilder[T] =
    copy(normalizers = normalizers :+ f)
  def build(): T => Token = { value =>
    // validate, convert, normalize
  }
}
```

Companion object provides `apply`:
```scala
object TokenizerBuilder {
  def apply[T](): TokenizerBuilder[T] = new TokenizerBuilder[T]()
}
```

## Python __init__ with default mutable args

Python `def __init__(self, opts: dict = {})` — the mutable default is a bug-prone pattern.
Scala case class defaults are evaluated fresh each time, so `Map.empty` is safe.

## Method chaining return types

Python returns `self` for chaining. In Scala, if using mutable style, return `this`.
If using immutable case class style, return `copy(...)` — this is preferred.

## Companion Objects for Factory Methods

Python `@classmethod` → Scala companion object method:
```scala
object TokenMonad {
  def pure[A](value: A): TokenMonad[A] = new TokenMonad(value)
}
```
