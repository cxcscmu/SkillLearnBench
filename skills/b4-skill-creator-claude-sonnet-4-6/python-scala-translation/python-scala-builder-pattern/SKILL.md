---
name: python-scala-builder-pattern
description: Guide for translating Python fluent builder patterns and mutable accumulator objects to idiomatic immutable Scala builders with companion objects. Use this skill when converting Python classes with method chaining (returning self), mutable state accumulation, or factory/build() methods to Scala.
---

# Python Fluent Builder → Scala Immutable Builder

Python builders often use mutable `self` and return `self` for chaining. Scala's idiomatic approach uses immutable value objects — each `with*` method returns a new builder instance.

## Pattern

```python
class TokenizerBuilder(Generic[T]):
    def __init__(self) -> None:
        self._normalizers: list[Callable[[str], str]] = []
        self._validators: list[Callable[[T], bool]] = []
        self._metadata: dict[str, Any] = {}

    def with_normalizer(self, norm) -> "TokenizerBuilder[T]":
        self._normalizers.append(norm)
        return self

    def with_metadata(self, **kwargs) -> "TokenizerBuilder[T]":
        self._metadata.update(kwargs)
        return self

    def build(self) -> Callable[[T], Token]:
        ...
```

```scala
// Scala: immutable builder; each method returns a NEW instance
class TokenizerBuilder[T] private (
  normalizers: List[String => String],
  validators:  List[T => Boolean],
  metadata:    Map[String, Any]
) {
  def withNormalizer(f: String => String): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers :+ f, validators, metadata)

  def withValidator(f: T => Boolean): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers, validators :+ f, metadata)

  def withMetadata(pairs: (String, Any)*): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers, validators, metadata ++ pairs.toMap)

  def build(): T => Token = { value =>
    validators.foreach { v =>
      if (!v(value)) throw new IllegalArgumentException(s"Validation failed for $value")
    }
    val str = normalizers.foldLeft(value.toString)((s, f) => f(s))
    Token(str, TokenType.STRING, metadata)
  }
}

// Companion object provides the public constructor
object TokenizerBuilder {
  def apply[T](): TokenizerBuilder[T] =
    new TokenizerBuilder[T](Nil, Nil, Map.empty)
}
```

## Why immutable?

- Thread-safe by default — no shared mutable state
- Enables easy rollback (keep a reference to an old builder)
- Composable: builders can be passed around without defensive copying

## Vararg Metadata

Python uses `**kwargs` for keyword metadata. In Scala, use `(String, Any)*` tuple varargs:

```scala
builder.withMetadata("type" -> "custom", "version" -> 1)
// Inside: metadata ++ pairs.toMap
```

## Mutable Internal State → `ListBuffer` / `mutable.Map`

For cases where mutation is genuinely needed (e.g., `MutableTokenBatch`), use `scala.collection.mutable`:

```python
class MutableTokenBatch:
    def __init__(self):
        self.tokens = []
        self._processed = False

    def add(self, token):
        if self._processed:
            raise RuntimeError("Batch already processed")
        self.tokens.append(token)
```

```scala
class MutableTokenBatch {
  private val _tokens     = scala.collection.mutable.ListBuffer.empty[Token]
  private var _processed  = false

  def tokens: List[Token] = _tokens.toList

  def add(token: Token): Unit = {
    if (_processed) throw new RuntimeException("Batch already processed")
    _tokens += token
  }

  def markProcessed(): Unit = { _processed = true }
}
```

## Python `dict` default argument anti-pattern → Scala safe defaults

```python
# DANGER: mutable default in Python
def __init__(self, format_options: dict = {}): ...
```

In Scala, default parameter expressions are evaluated fresh each call:

```scala
class NumericTokenizer(
  precision:     Int                 = 6,
  formatOptions: Map[String, Any]    = Map.empty   // safe — Map.empty is immutable
)
```

## Build Output as a Function

Python `build()` returns a `Callable`. In Scala, the result is a plain function value:

```scala
val tokenize: T => Token = builder.build()
val result = tokenize("Hello World")
// or equivalently: builder.build()("Hello World")
```
