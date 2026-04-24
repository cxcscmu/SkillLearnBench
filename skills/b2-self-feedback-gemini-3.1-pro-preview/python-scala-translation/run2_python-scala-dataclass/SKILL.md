---
name: run2_python-scala-dataclass
description: Translating Python @dataclass and Enum to Scala case class and Enumeration/Sealed Traits safely
---

# Dataclass and Enum to Scala Case Class and Sealed Trait

Python uses `@dataclass` for concise data records and `Enum` for enumerations. In Scala, we use `case class` and `sealed abstract class / trait` with `case object`.

## Python Enum
```python
class TokenType(Enum):
    STRING = "string"
    NUMERIC = "numeric"
```

## Scala Enum Equivalent (Scala 2.13)
While Scala 3 has `enum`, in Scala 2.13 we implement Algebraic Data Types explicitly using `sealed abstract class` (or `sealed trait`). Abstract class allows taking parameters in constructor.
```scala
sealed abstract class TokenType(val value: String)
object TokenType {
  case object STRING extends TokenType("string")
  case object NUMERIC extends TokenType("numeric")
}
```

## Python Dataclass
```python
@dataclass(frozen=True)
class Token:
    value: str
    token_type: TokenType
    metadata: dict[str, Any] = field(default_factory=dict)
```

## Scala Case Class
Case classes are immutable and come with an out-of-the-box `copy` method.
```scala
case class Token(
  value: String,
  tokenType: TokenType,
  metadata: Map[String, Any] = Map.empty
) {
  // Using .copy to create a modified clone
  def withMetadata(kwargs: (String, Any)*): Token = {
    this.copy(metadata = this.metadata ++ kwargs)
  }
}
```
## Notes
- Python's `default_factory` translates simply to `= Map.empty` as default parameters in Scala are evaluated dynamically upon invocation. 
- Python `dict` translates safely to Scala's immutable `Map`. For mutability, use `scala.collection.mutable.Map`.
