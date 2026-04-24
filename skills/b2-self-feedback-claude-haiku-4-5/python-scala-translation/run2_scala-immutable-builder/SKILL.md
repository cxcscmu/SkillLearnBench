---
name: scala-immutable-builder
description: Building immutable configurations with fluent method chaining in Scala
---

# Fluent Builder Pattern in Scala

## Method Chaining with `this.type`

The `this.type` singleton type enables proper method chaining while maintaining type safety.

```scala
class TokenizerBuilder[T] {
  private var normalizers: List[String => String] = List()
  private var metadata: Map[String, Any] = Map()

  def withNormalizer(normalizer: String => String): this.type = {
    normalizers = normalizers :+ normalizer
    this
  }

  def withMetadata(entries: (String, Any)*): this.type = {
    metadata = metadata ++ entries.toMap
    this
  }
}

// Usage - returns actual type, not generic Builder
val builder: TokenizerBuilder[String] = TokenizerBuilder[String]()
  .withNormalizer(_.toLowerCase)
  .withMetadata("key" -> "value")
```

## Immutable Builder Alternative

For true immutability, create new instances (heavier but safer):

```scala
case class Config[T](
  normalizers: List[String => String] = List(),
  metadata: Map[String, Any] = Map()
) {
  def withNormalizer(f: String => String) = copy(
    normalizers = normalizers :+ f
  )
}
```

## Converting to Immutable Result

```scala
def build(): T => Token = { value =>
  // Capture current state (immutable snapshot)
  val capturedNormalizers = normalizers
  val capturedMetadata = metadata

  { v =>
    var str = v.toString
    for (norm <- capturedNormalizers) {
      str = norm(str)
    }
    Token(str, STRING, capturedMetadata)
  }
}
```

## Validation During Build

```scala
def build(): T => Token = { value =>
  val errors = mutable.ArrayBuffer[String]()

  for (validator <- validators) {
    if (!validator(value)) {
      errors += s"Validation failed for $value"
    }
  }

  if (errors.nonEmpty) {
    throw new IllegalArgumentException(errors.mkString("; "))
  }

  // Build tokenizer function
  val capturedMetadata = metadata
  v => Token(v.toString, STRING, capturedMetadata)
}
```

## Factory Object Companion

```scala
class TokenizerBuilder[T] { ... }

object TokenizerBuilder {
  def apply[T](): TokenizerBuilder[T] = new TokenizerBuilder[T]
}

// Usage
TokenizerBuilder[String]()
  .withNormalizer(_.trim)
  .build()
```
