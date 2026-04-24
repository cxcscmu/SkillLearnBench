---
name: scala-functional-builders
description: Guide for creating functional fluent builders in Scala.
---

# Functional Builders in Scala

Python's fluent builder pattern often mutates internal state (`self._validators.append(...)`). In Scala, it is idiomatic to use immutable case classes that return copies of themselves with updated state. However, a mutable builder is also acceptable for exact translations or performance optimizations.

## Immutable Builder Pattern (Idiomatic Scala)

```scala
case class TokenizerBuilder[T](
  normalizers: List[String => String] = Nil,
  validators: List[T => Boolean] = Nil,
  metadata: Map[String, Any] = Map.empty
) {

  def withNormalizer(n: String => String): TokenizerBuilder[T] =
    this.copy(normalizers = normalizers :+ n)

  def withValidator(v: T => Boolean): TokenizerBuilder[T] =
    this.copy(validators = validators :+ v)

  def withMetadata(md: (String, Any)*): TokenizerBuilder[T] =
    this.copy(metadata = metadata ++ md)

  def build(): T => Token = { value =>
    // Run validators
    if (!validators.forall(v => v(value))) {
      throw new IllegalArgumentException(s"Validation failed for $value")
    }

    // Process and return token
    val strValue = normalizers.foldLeft(value.toString)((acc, n) => n(acc))
    Token(strValue, TokenType.STRING, metadata)
  }
}
```
This cleanly maps to Python's generic generic builder pattern, using Scala 2.13 collections like `List` and `Map`.
