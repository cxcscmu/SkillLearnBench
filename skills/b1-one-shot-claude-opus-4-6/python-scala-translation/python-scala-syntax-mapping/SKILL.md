---
name: python-scala-syntax-mapping
description: Reference for translating Python syntax constructs (enums, dataclasses, type vars, protocols) to Scala equivalents.
---

# Python to Scala Syntax Mapping

## Enums
Python `Enum` -> Scala sealed trait + case objects or `Enumeration`:

```scala
// Preferred: sealed trait for pattern matching exhaustiveness
sealed abstract class TokenType(val value: String)
object TokenType {
  case object STRING extends TokenType("string")
  case object NUMERIC extends TokenType("numeric")
}
```

## Dataclasses (frozen=True) -> Case Classes
```scala
// Python: @dataclass(frozen=True) with default fields
// Scala: case class (immutable by default)
case class Token(value: String, tokenType: TokenType, metadata: Map[String, Any] = Map.empty)
```

## TypeVar -> Type Parameters
```scala
// Python: T = TypeVar("T")           -> [T]
// Python: T_co = TypeVar(covariant)  -> [+T]
// Python: T_contra = TypeVar(contra) -> [-T]
// Python: NumericT = TypeVar("NumericT", int, float, Decimal) -> type class or union
```

## Protocol -> Trait (structural typing)
```scala
// Python Protocol -> Scala trait
trait Tokenizable {
  def toToken: String
}
```

## Optional / Union
```scala
// Python: Optional[X] -> Scala: Option[X]
// Python: X | None -> Scala: Option[X]
// Python: Union[A, B] -> Scala: Either[A, B] or sealed trait or overloaded methods
```

## Default Mutable Args
Python allows mutable defaults (anti-pattern). Scala avoids this:
```scala
// Python: def __init__(self, opts: dict = {}):
// Scala:  def this(opts: Map[String, Any] = Map.empty)
```
