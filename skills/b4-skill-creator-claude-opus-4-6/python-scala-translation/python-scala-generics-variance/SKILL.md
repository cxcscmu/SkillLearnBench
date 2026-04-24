---
name: python-scala-generics-variance
description: >
  Translating Python generics, variance annotations, protocols, and type variables
  to Scala type parameters, variance annotations, and traits. Use when converting
  Python Generic[T], TypeVar with covariant/contravariant, Protocol classes, or
  higher-kinded type simulations to Scala.
---

# Python Generics & Variance to Scala

## Python Generic[T] → Scala trait/class with type parameter

Python:
```python
T = TypeVar("T")
class BaseTokenizer(ABC, Generic[T]):
    @abstractmethod
    def tokenize(self, value: T) -> Token: ...
```

Scala:
```scala
trait BaseTokenizer[T] {
  def tokenize(value: T): Token
  def tokenizeBatch(values: Iterable[T]): Iterator[Token] =
    values.iterator.map(tokenize)
}
```

Key: Python's `ABC + Generic[T]` becomes a Scala `trait[T]`. Abstract methods need no `abstract` keyword in traits — just leave them unimplemented.

## Variance Annotations

Python:
```python
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
```

Scala:
```scala
class TokenContainer[+A](items: Seq[A])     // covariant
class TokenSink[-A]                          // contravariant
class BivariantHandler[A](default: A)        // invariant
```

## Python Protocol → Scala trait (structural typing)

Python protocols are structural types. In Scala, use regular traits:
```scala
trait Tokenizable {
  def toToken: String
}
```

## Bounded TypeVars → Scala type bounds or overloading

Python `TypeVar("NumericT", int, float, Decimal)` constrains to specific types. In Scala, use overloaded methods, union-style sealed traits, or context bounds depending on context.

For `TypeVar("StrOrBytes", str, bytes)`:
- If runtime dispatch is needed, use pattern matching on `Any` or overloaded methods

## Higher-Kinded Type Simulation → Scala class with type param

Python's `TokenFunctor` simulation translates naturally:
```scala
class TokenFunctor[A](private val value: A) {
  def map[B](f: A => B): TokenFunctor[B] = new TokenFunctor(f(value))
  def flatMap[B](f: A => TokenFunctor[B]): TokenFunctor[B] = f(value)
  def get: A = value
}
```

Note: `getOrElse` with null-checking becomes Option-based in idiomatic Scala.
