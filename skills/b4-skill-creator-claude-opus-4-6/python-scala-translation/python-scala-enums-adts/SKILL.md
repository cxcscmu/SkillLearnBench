---
name: python-scala-enums-adts
description: >
  Translating Python enums, dataclasses, and union types to Scala sealed traits,
  case classes, and ADTs. Use when converting Python Enum classes to Scala enumerations,
  Python dataclasses to Scala case classes, or Python Union/Optional types to Scala
  Option/Either/sealed hierarchies.
---

# Python Enums & Dataclasses to Scala ADTs

## Python Enum → Scala sealed abstract class + case objects

Python:
```python
class TokenType(Enum):
    STRING = "string"
    NUMERIC = "numeric"
```

Scala (2.13 idiomatic):
```scala
sealed abstract class TokenType(val value: String)
object TokenType {
  case object STRING extends TokenType("string")
  case object NUMERIC extends TokenType("numeric")
}
```

Why sealed abstract class: Scala 2.13 doesn't have `enum` (that's Scala 3). A sealed hierarchy gives exhaustive match checking and is the standard Scala 2 pattern.

## Python dataclass(frozen=True) → Scala case class

Python:
```python
@dataclass(frozen=True)
class Token:
    value: str
    token_type: TokenType
    metadata: dict[str, Any] = field(default_factory=dict)
```

Scala:
```scala
case class Token(
  value: String,
  tokenType: TokenType,
  metadata: Map[String, Any] = Map.empty
)
```

Key differences:
- Case classes are immutable by default (no `frozen` needed)
- `field(default_factory=dict)` becomes `= Map.empty` — Scala's default args are evaluated fresh each call
- Use `camelCase` for field names per Scala convention
- `copy()` is auto-generated and replaces manual `with_metadata` style methods, though a convenience method can wrap it

## Python @dataclass (mutable) → Scala class with vars or mutable buffer

For mutable state, use `var` fields or mutable collections, and throw `IllegalStateException` for state violations:
```scala
class MutableTokenBatch {
  private val _tokens = scala.collection.mutable.ListBuffer.empty[Token]
  private var _processed = false

  def add(token: Token): Unit = {
    if (_processed) throw new IllegalStateException("Batch already processed")
    _tokens += token
  }
}
```

## Python Optional/Union → Scala Option/Either

- `Optional[X]` / `X | None` → `Option[X]`
- `Union[A, B]` → `Either[A, B]` or a sealed trait hierarchy
- `dict[str, Any]` → `Map[String, Any]`
