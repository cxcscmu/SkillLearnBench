---
name: python-scala-sealed-enum
description: Translating Python Enum classes to Scala sealed abstract classes or sealed traits with companion objects, preserving value fields and exhaustive pattern matching.
---

# Python Enum → Scala Sealed Traits

## Python Pattern
```python
class TokenType(Enum):
    STRING = "string"
    NUMERIC = "numeric"
    NULL = "null"
```

## Scala Idiomatic Translation

Use `sealed abstract class` (not `Enum`) with a companion `object` holding `case object` members:

```scala
sealed abstract class TokenType(val value: String)

object TokenType {
  case object STRING  extends TokenType("string")
  case object NUMERIC extends TokenType("numeric")
  case object NULL    extends TokenType("null")
}
```

**Why `sealed abstract class` over `sealed trait`?**
- Use `sealed abstract class` when members need constructor parameters (like `value: String`).
- Use `sealed trait` for purely marker/tag types with no data.

## Key Differences from Python
| Python | Scala |
|--------|-------|
| `TokenType.STRING.value` | `TokenType.STRING.value` (same API) |
| `isinstance(x, TokenType)` | Pattern match on sealed type |
| Can iterate `list(TokenType)` | Use `Set(STRING, NUMERIC, ...)` manually |
| `TokenType["STRING"]` | Not needed; use `TokenType.STRING` directly |

## Exhaustive Pattern Matching (Bonus)
```scala
def describe(t: TokenType): String = t match {
  case TokenType.STRING  => "A string token"
  case TokenType.NUMERIC => "A numeric token"
  case TokenType.NULL    => "A null token"
  // Compiler warns if a case is missing (because sealed)
}
```

## Companion Object `values` List (if needed)
```scala
object TokenType {
  case object STRING  extends TokenType("string")
  case object NUMERIC extends TokenType("numeric")
  case object NULL    extends TokenType("null")

  val values: List[TokenType] = List(STRING, NUMERIC, NULL)

  def fromString(s: String): Option[TokenType] =
    values.find(_.value == s)
}
```
