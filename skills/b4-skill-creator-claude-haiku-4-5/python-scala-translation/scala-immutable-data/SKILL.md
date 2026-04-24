---
name: scala-immutable-data
description: |
  How to convert Python mutable dataclasses and enums to immutable Scala case classes, sealed traits, and sealed objects.
  Use when translating Python @dataclass, Enum, and mutable collection patterns to idiomatic Scala.
  Covers immutable-by-default patterns, copy with modifications, and sealed hierarchies.
---

# Scala Immutable Data Structures

## Enums: Python Enum → Scala Sealed Trait + Case Objects

### Python Enum Pattern

```python
class TokenType(Enum):
    STRING = "string"
    NUMERIC = "numeric"
    TEMPORAL = "temporal"
    STRUCTURED = "structured"
    BINARY = "binary"
    NULL = "null"
```

### Scala Sealed Trait + Case Objects Pattern

Scala prefers **sealed traits** over Java-style enums for better pattern matching and type safety:

```scala
sealed trait TokenType {
  def value: String
}

case object StringType extends TokenType {
  def value = "string"
}

case object NumericType extends TokenType {
  def value = "numeric"
}

case object TemporalType extends TokenType {
  def value = "temporal"
}

case object StructuredType extends TokenType {
  def value = "structured"
}

case object BinaryType extends TokenType {
  def value = "binary"
}

case object NullType extends TokenType {
  def value = "null"
}
```

**Or using a companion object with values** (more Python-like):**

```scala
sealed trait TokenType {
  def value: String
}

object TokenType {
  case object STRING extends TokenType { def value = "string" }
  case object NUMERIC extends TokenType { def value = "numeric" }
  case object TEMPORAL extends TokenType { def value = "temporal" }
  case object STRUCTURED extends TokenType { def value = "structured" }
  case object BINARY extends TokenType { def value = "binary" }
  case object NULL extends TokenType { def value = "null" }
}
```

### Pattern Matching on Sealed Traits

```scala
val tokenType: TokenType = TokenType.STRING
val message = tokenType match {
  case TokenType.STRING => "It's a string!"
  case TokenType.NUMERIC => "It's numeric!"
  case TokenType.TEMPORAL => "It's temporal!"
  case _ => "Something else"
}
```

**Sealed trait advantage**: Compiler checks exhaustiveness of pattern matches!

## Data Classes: Python @dataclass → Scala case class

### Python Dataclass (Mutable by Default)

```python
@dataclass(frozen=True)
class Token:
    """Immutable token representation."""
    value: str
    token_type: TokenType
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_metadata(self, **kwargs: Any) -> "Token":
        """Return new token with additional metadata."""
        new_meta = {**self.metadata, **kwargs}
        return Token(self.value, self.token_type, new_meta)
```

### Scala Case Class (Immutable by Default)

Case classes in Scala are **immutable by default** and have structural equality:

```scala
case class Token(
  value: String,
  tokenType: TokenType,
  metadata: Map[String, Any] = Map()
) {
  def withMetadata(pairs: (String, Any)*): Token =
    this.copy(metadata = metadata ++ pairs.toMap)
}
```

**Key differences:**
- Scala case classes are immutable by default (no `frozen=True` needed)
- Use `.copy()` method to create new instances with modified fields
- Named parameters work like Python
- Default factory becomes default value with `.toMap` conversion if needed

### Using `.copy()` for Immutability

```scala
// Python (manual copy)
token = Token("value", TokenType.STRING)
newToken = Token(token.value, token.token_type, {...})

// Scala (automatic .copy())
val token = Token("value", TokenType.STRING)
val newToken = token.copy(metadata = Map("key" -> "value"))

// Change multiple fields
val anotherToken = token.copy(
  value = "newValue",
  metadata = Map("updated" -> true)
)
```

## Mutable Collections → Immutable Collections

### Python Lists → Scala Vectors and Lists

**Python (mutable):**
```python
tokens: list[Token] = []
tokens.append(token)
tokens.extend(other_tokens)
```

**Scala (immutable):**
```scala
var tokens: Vector[Token] = Vector()
tokens = tokens :+ token           // Append (creates new vector)
tokens = tokens ++ otherTokens     // Extend (creates new vector)

// OR use var with List (both work)
var tokenList: List[Token] = List()
tokenList = tokenList :+ token
```

**When to use what:**
- **Vector**: O(log n) random access, good for large collections
- **List**: O(n) access but efficient for head/tail operations
- **ArrayBuffer**: mutable alternative if you need it

### Python Dicts → Scala Maps

**Python (mutable):**
```python
metadata: dict[str, Any] = {}
metadata["key"] = "value"
metadata.update({"more": "data"})
```

**Scala (immutable):**
```scala
var metadata: Map[String, Any] = Map()
metadata = metadata + ("key" -> "value")
metadata = metadata ++ Map("more" -> "data")

// Or use mutable.Map if you must mutate
import scala.collection.mutable
val mutableMetadata = mutable.Map[String, Any]()
mutableMetadata("key") = "value"
```

## Sealed Trait Hierarchies for Variants

### Python Union Types → Scala Sealed Traits

**Python (runtime union):**
```python
JsonValue = Union[str, int, float, bool, None, list["JsonValue"], dict[str, "JsonValue"]]

def process(value: JsonValue) -> None:
    if isinstance(value, str):
        handle_string(value)
    elif isinstance(value, int):
        handle_int(value)
    # ...
```

**Scala (compile-time union via sealed trait):**
```scala
sealed trait JsonValue

case class JsonString(value: String) extends JsonValue
case class JsonNumber(value: Double) extends JsonValue
case class JsonBool(value: Boolean) extends JsonValue
case object JsonNull extends JsonValue
case class JsonArray(values: Vector[JsonValue]) extends JsonValue
case class JsonObject(values: Map[String, JsonValue]) extends JsonValue

// Pattern matching is exhaustive at compile time
def process(value: JsonValue): Unit = value match {
  case JsonString(s) => handleString(s)
  case JsonNumber(n) => handleNumber(n)
  case JsonBool(b) => handleBool(b)
  case JsonNull => handleNull()
  case JsonArray(vs) => handleArray(vs)
  case JsonObject(vs) => handleObject(vs)
}
```

**Advantage**: Compiler enforces all cases are handled!

## Recursive Data Types

For recursive types like JSON, use abstract type alias in companion object:

```scala
sealed trait JsonValue
object JsonValue {
  case class JsonArray(values: Vector[JsonValue]) extends JsonValue
  case class JsonObject(values: Map[String, JsonValue]) extends JsonValue
  // ...
}
```

## Mutable State vs Immutable

### Python Mutable Batch (Anti-pattern, but required in spec)

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

### Scala Mutable (minimal, encapsulated)

```scala
class MutableTokenBatch {
  private var tokens: Vector[Token] = Vector()
  private var _processed: Boolean = false

  def add(token: Token): Unit = {
    if (_processed) throw new RuntimeException("Batch already processed")
    tokens = tokens :+ token
  }

  def markProcessed(): Unit = {
    _processed = true
  }

  def getTokens: Vector[Token] = tokens
}
```

**Key pattern**: Use `var` with private scope, immutable collection as internal state.

## Option[T] Instead of None/Null

### Python Optional

```python
def get_token(key: str) -> Token | None:
    if key in registry:
        return registry[key]
    return None

result = get_token("key")
if result is not None:
    process(result)
```

### Scala Option

```scala
def getToken(key: String): Option[Token] =
  registry.get(key)

val result = getToken("key")
result.foreach(process)

// Or pattern match
result match {
  case Some(token) => process(token)
  case None => handleMissing()
}

// Or use getOrElse
val token = getToken("key").getOrElse(defaultToken)
```

**Scala idiom**: Use `Option.map`, `Option.flatMap`, `Option.getOrElse` instead of null checks.

## Default Values

### Python Defaults (including mutable defaults—antipattern)

```python
def __init__(self, format_options: dict[str, Any] = {}):
    self.format_options = format_options
```

### Scala Defaults (immutable)

```scala
def apply(formatOptions: Map[String, Any] = Map()): NumericTokenizer =
  new NumericTokenizer(formatOptions)
```

**Rule**: Never use mutable collections as default values in either language. In Scala, prefer immutable defaults or `None`.

## Sealed Final Classes (When Needed)

For data types that shouldn't be extended:

```scala
sealed case class Token(
  value: String,
  tokenType: TokenType,
  metadata: Map[String, Any] = Map()
) {
  def withMetadata(pairs: (String, Any)*): Token =
    this.copy(metadata = metadata ++ pairs.toMap)
}

// Cannot extend Token outside this file—sealed is important!
```

Use `sealed case class` to prevent accidental extension while keeping immutability.
