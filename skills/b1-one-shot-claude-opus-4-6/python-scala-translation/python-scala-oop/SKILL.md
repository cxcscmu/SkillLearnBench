---
name: python-scala-oop
description: Guide for translating Python classes, inheritance, ABC, generics and builder patterns to idiomatic Scala.
---

# Python to Scala OOP Patterns

## Abstract Base Class -> Abstract Class or Trait
```scala
// Python: class BaseTokenizer(ABC, Generic[T])
// Scala:
abstract class BaseTokenizer[T] {
  def tokenize(value: T): Token
  def tokenizeBatch(values: Iterable[T]): Iterator[Token] =
    values.iterator.map(tokenize)
}
```

## Generic Classes with Variance
```scala
// Covariant container (produces T)
class TokenContainer[+T](items: Seq[T]) {
  private val _items: Vector[T] = items.toVector
  def getAll: Vector[T] = _items
}

// Contravariant sink (consumes T)
class TokenSink[-T] { ... }

// Invariant handler
class BivariantHandler[T](private var _value: T) { ... }
```

## Builder Pattern (Fluent Interface)
```scala
// Use `this.type` or return the class itself for chaining
class TokenizerBuilder[T] {
  def withNormalizer(f: String => String): TokenizerBuilder[T] = { ... ; this }
  def build(): T => Token = { ... }
}

// Companion object with apply for factory
object TokenizerBuilder {
  def apply[T](): TokenizerBuilder[T] = new TokenizerBuilder[T]
}
```

## Mutable State
```scala
// Python: @dataclass with mutable fields
// Scala: use var or mutable collections explicitly
import scala.collection.mutable

class MutableTokenBatch {
  private val _tokens = mutable.ListBuffer.empty[Token]
  private var _processed = false

  def add(token: Token): Unit =
    if (_processed) throw new RuntimeException("Batch already processed")
    else _tokens += token
}
```
