---
name: run2_scala-sealed-traits
description: Translating Python Enum and frozen dataclass to idiomatic Scala sealed ADTs and case classes, with precise metadata typing and withMetadata pattern.
---

# Scala Sealed ADTs and Value Types (vs Python Enums / Frozen Dataclasses)

## Python Enum → Scala Sealed Abstract Class

Python:
```python
class TokenType(Enum):
    STRING = "string"
    NUMERIC = "numeric"
    NULL = "null"
```

Idiomatic Scala 2.13:
```scala
sealed abstract class TokenType(val value: String)

object TokenType {
  case object STRING     extends TokenType("string")
  case object NUMERIC    extends TokenType("numeric")
  case object TEMPORAL   extends TokenType("temporal")
  case object STRUCTURED extends TokenType("structured")
  case object BINARY     extends TokenType("binary")
  case object NULL       extends TokenType("null")
}
```

**Why `sealed abstract class` instead of `sealed trait`?**
- `sealed abstract class` allows constructor parameters (`val value: String`)
- `sealed trait` does not have a primary constructor
- Companion object groups all case objects — compiler can exhaustively check pattern matches

## Python Frozen Dataclass → Scala Final Case Class

Python:
```python
@dataclass(frozen=True)
class Token:
    value: str
    token_type: TokenType
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_metadata(self, **kwargs: Any) -> "Token":
        new_meta = {**self.metadata, **kwargs}
        return Token(self.value, self.token_type, new_meta)
```

Scala:
```scala
final case class Token(
  value: String,
  tokenType: TokenType,
  metadata: Map[String, Any] = Map.empty
) {
  def withMetadata(entries: (String, Any)*): Token =
    copy(metadata = metadata ++ entries.toMap)
}
```

**Key design points:**
- `final case class` — immutable by default, structural equality, pattern matching
- `Map[String, Any]` — preserves mixed value types (String, Boolean, Int)
- `copy()` creates a modified clone — idiomatic, avoids manual constructor call
- `(String, Any)*` varargs replaces `**kwargs` — callers use `"key" -> "value"` tuple syntax
- `Map.empty` instead of mutable `{}` default
- Field names in camelCase: `tokenType` not `token_type`

## Metadata Type Choice: Map[String, Any]

When metadata holds mixed types (strings, booleans, integers), `Map[String, Any]` is appropriate.
ScalaTest can check map contents:
```scala
token.metadata shouldBe empty
token.metadata should contain ("key" -> "value")    // String value
token.metadata should contain ("json" -> true)      // Boolean value
token.metadata should contain ("position" -> 1)     // Int value
```

The `Any` type in Scala preserves runtime types; `==` comparison works correctly via Java's `equals`.

## Mutable Class Pattern (Python dataclass without frozen)

Python:
```python
@dataclass
class MutableTokenBatch:
    tokens: list[Token] = field(default_factory=list)
    _processed: bool = False

    def add(self, token: Token) -> None:
        if self._processed:
            raise RuntimeError("Batch already processed")
        self.tokens.append(token)
```

Scala:
```scala
final class MutableTokenBatch {
  private var _tokens: Vector[Token] = Vector.empty
  private var _processed: Boolean    = false

  def tokens: Vector[Token] = _tokens

  def add(token: Token): Unit = {
    if (_processed) throw new RuntimeException("Batch already processed")
    _tokens = _tokens :+ token
  }

  def markProcessed(): Unit = _processed = true
}
```

**Key points:**
- `private var` instead of `@dataclass` mutable fields
- Public getter `def tokens` exposes an immutable view
- `Vector` preferred over `List` for indexed access and performance
