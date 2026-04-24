---
name: scala-adt-enums
description: Translating Python Enums and Protocols to Scala sealed traits and algebraic data types
---

# Scala ADTs, Sealed Traits, and Enums for Python Developers

## Enums

### Python Enum
```python
from enum import Enum

class TokenType(Enum):
    STRING = "string"
    NUMERIC = "numeric"
    TEMPORAL = "temporal"
    STRUCTURED = "structured"
    BINARY = "binary"
    NULL = "null"

# Usage
t = TokenType.STRING
t.value  # "string"
t.name   # "STRING"
```

### Scala Enum (Scala 2.13 - using sealed trait + case objects)
```scala
sealed trait TokenType {
  def value: String
}
object TokenType {
  case object STRING extends TokenType { val value = "string" }
  case object NUMERIC extends TokenType { val value = "numeric" }
  case object TEMPORAL extends TokenType { val value = "temporal" }
  case object STRUCTURED extends TokenType { val value = "structured" }
  case object BINARY extends TokenType { val value = "binary" }
  case object NULL extends TokenType { val value = "null" }

  // Helper for pattern matching
  def all: List[TokenType] = List(STRING, NUMERIC, TEMPORAL, STRUCTURED, BINARY, NULL)
}

// Usage
val t: TokenType = TokenType.STRING
t.value  // "string"
```

## Algebraic Data Types (ADTs)

### Python Union Types
```python
from typing import Union

JsonValue = Union[str, int, float, bool, None, list["JsonValue"], dict[str, "JsonValue"]]

# Function handling multiple types
def process(value: Union[str, int]) -> str:
    if isinstance(value, str):
        return value
    else:
        return str(value)
```

### Scala Sealed Traits (Idiomatic ADT)
```scala
sealed trait JsonValue
case class JString(value: String) extends JsonValue
case class JNumber(value: Double) extends JsonValue
case class JBoolean(value: Boolean) extends JsonValue
case object JNull extends JsonValue
case class JArray(value: Vector[JsonValue]) extends JsonValue
case class JObject(value: Map[String, JsonValue]) extends JsonValue

// Pattern matching (exhaustive)
def process(json: JsonValue): String = json match {
  case JString(s) => s
  case JNumber(n) => n.toString
  case JBoolean(b) => b.toString
  case JNull => "null"
  case JArray(arr) => s"Array(${arr.size})"
  case JObject(obj) => s"Object(${obj.size})"
}
```

## Protocols → Scala Traits

### Python Protocol
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Tokenizable(Protocol):
    def to_token(self) -> str: ...

def process(obj: Tokenizable) -> str:
    return obj.to_token()
```

### Scala Trait (Type Class Pattern)
```scala
trait Tokenizable {
  def toToken: String
}

def process(obj: Tokenizable): String = obj.toToken

// Or as type class (more flexible, less invasive)
trait Tokenizable[T] {
  def toToken(value: T): String
}

object Tokenizable {
  implicit val stringTokenizable: Tokenizable[String] = new Tokenizable[String] {
    def toToken(value: String) = value
  }
}

def process[T](obj: T)(implicit ev: Tokenizable[T]): String = ev.toToken(obj)
```

## Abstract Classes and Inheritance

### Python ABC
```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class BaseTokenizer(ABC, Generic[T]):
    @abstractmethod
    def tokenize(self, value: T) -> Token:
        pass

    def tokenize_batch(self, values: Iterable[T]) -> Iterator[Token]:
        for v in values:
            yield self.tokenize(v)

class StringTokenizer(BaseTokenizer[str]):
    def tokenize(self, value: str) -> Token:
        return Token(value, TokenType.STRING)
```

### Scala Abstract Class
```scala
abstract class BaseTokenizer[T] {
  def tokenize(value: T): Token

  def tokenizeBatch(values: Iterable[T]): Iterator[Token] =
    values.toIterator.map(tokenize)
}

class StringTokenizer extends BaseTokenizer[String] {
  def tokenize(value: String): Token =
    Token(value, TokenType.STRING)
}
```

## Dataclasses → Case Classes

### Python Dataclass
```python
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Token:
    value: str
    token_type: TokenType
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_metadata(self, **kwargs: Any) -> "Token":
        new_meta = {**self.metadata, **kwargs}
        return Token(self.value, self.token_type, new_meta)
```

### Scala Case Class
```scala
case class Token(
  value: String,
  tokenType: TokenType,
  metadata: Map[String, Any] = Map()
) {
  def withMetadata(pairs: (String, Any)*): Token = {
    val newMeta = metadata ++ pairs.toMap
    copy(metadata = newMeta)
  }
}
```

## Mutable Dataclasses → Regular Classes

### Python Mutable Dataclass
```python
@dataclass
class MutableTokenBatch:
    tokens: list[Token] = field(default_factory=list)
    _processed: bool = False

    def add(self, token: Token) -> None:
        if self._processed:
            raise RuntimeError("Batch already processed")
        self.tokens.append(token)

    def mark_processed(self) -> None:
        self._processed = True
```

### Scala Class
```scala
class MutableTokenBatch {
  private val tokens = scala.collection.mutable.ListBuffer[Token]()
  private var processed = false

  def add(token: Token): Unit = {
    if (processed) throw new RuntimeException("Batch already processed")
    tokens += token
  }

  def markProcessed(): Unit = {
    processed = true
  }

  def getTokens: List[Token] = tokens.toList
}
```

## Pattern Matching for Type Narrowing

Scala pattern matching is more powerful than Python's isinstance checks:

```scala
// Python equivalent:
if isinstance(value, str):
    return value
elif isinstance(value, int):
    return value.toString()

// Scala pattern matching:
value match {
  case s: String => s
  case i: Int => i.toString
  case _ => "unknown"
}

// Even better with case classes:
value match {
  case Token(v, TokenType.STRING, _) => v
  case Token(v, TokenType.NUMERIC, _) => s"[NUM]$v"
  case _ => "other"
}
```

## Best Practices

1. **Use sealed traits for sum types** - ensures exhaustive pattern matching
2. **Prefer case classes over regular classes** - automatic equals, hashCode, toString, copy
3. **Use case objects for singleton ADT members**
4. **Leverage pattern matching** - more concise than isinstance chains
5. **Consider type classes for ad-hoc polymorphism** - instead of duck typing
6. **Use Option[T] instead of None/null** - more type-safe
