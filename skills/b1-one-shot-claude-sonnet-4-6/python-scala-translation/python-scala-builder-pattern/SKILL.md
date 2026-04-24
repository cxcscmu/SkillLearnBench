---
name: python-scala-builder-pattern
description: Implementing immutable fluent builder pattern in Scala as a translation of Python classes with method chaining, emphasizing immutability and type safety.
---

# Builder Pattern in Scala

## Python Pattern (Mutable Builder)
```python
class TokenizerBuilder(Generic[T]):
    def __init__(self):
        self._normalizers = []
        self._metadata = {}

    def with_normalizer(self, normalizer):
        self._normalizers.append(normalizer)
        return self

    def build(self):
        ...
```

## Scala Idiomatic Translation (Immutable Builder)

In Scala, prefer **immutable builders** — each method creates a new builder instance:

```scala
class TokenizerBuilder[T] private (
  normalizers: List[String => String],
  validators:  List[T => Boolean],
  meta:        Map[String, Any]
) {
  def withNormalizer(f: String => String): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers :+ f, validators, meta)

  def withValidator(f: T => Boolean): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers, validators :+ f, meta)

  def withMetadata(pairs: (String, Any)*): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers, validators, meta ++ pairs)

  def build(): T => Token = { value =>
    validators.foreach { v =>
      if (!v(value)) throw new IllegalArgumentException(s"Validation failed for $value")
    }
    val str = normalizers.foldLeft(value.toString)((s, f) => f(s))
    Token(str, TokenType.STRING, meta)
  }
}

object TokenizerBuilder {
  def apply[T](): TokenizerBuilder[T] =
    new TokenizerBuilder[T](Nil, Nil, Map.empty)
}
```

## Usage
```scala
val tokenizer = TokenizerBuilder[String]()
  .withNormalizer(_.toLowerCase)
  .withNormalizer(_.replace(" ", "_"))
  .withValidator(_.nonEmpty)
  .withMetadata("type" -> "custom")
  .build()

val token = tokenizer("Hello World")
// token.value == "hello_world"
```

## Key Scala Conventions
- `private` constructor forces use of companion `apply` factory.
- `build()` returns a **function** `T => Token` (first-class function), not a new class.
- Use varargs `(String, Any)*` for key-value metadata pairs.
- `List` is immutable; use `:+` to append (creates new list).
- `Map ++ pairs` merges maps without mutation.

## Mutable vs Immutable
| Python (mutable) | Scala (immutable) |
|---|---|
| `self._list.append(x)` | `new Builder(list :+ x, ...)` |
| `self._dict.update(d)` | `new Builder(..., map ++ d)` |
| Returns `self` | Returns `new Builder(...)` |
