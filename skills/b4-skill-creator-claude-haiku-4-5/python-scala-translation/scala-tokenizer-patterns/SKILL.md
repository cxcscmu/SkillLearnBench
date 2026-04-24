---
name: scala-tokenizer-patterns
description: |
  Scala patterns specific to tokenizer implementations: builder pattern with generics, JSON handling with circe,
  temporal types (LocalDate/LocalDateTime), and functional tokenization pipelines.
  Use when implementing tokenizer classes, handling JSON structures, or building fluent APIs.
---

# Scala Tokenizer Implementation Patterns

## Builder Pattern with Fluent Interface

### Python TokenizerBuilder

```python
class TokenizerBuilder(Generic[T]):
    def __init__(self) -> None:
        self._normalizers: list[Callable[[str], str]] = []
        self._validators: list[Callable[[T], bool]] = []
        self._metadata: dict[str, Any] = {}

    def with_normalizer(self, normalizer: Callable[[str], str]) -> "TokenizerBuilder[T]":
        self._normalizers.append(normalizer)
        return self

    def with_validator(self, validator: Callable[[T], bool]) -> "TokenizerBuilder[T]":
        self._validators.append(validator)
        return self

    def with_metadata(self, **kwargs: Any) -> "TokenizerBuilder[T]":
        self._metadata.update(kwargs)
        return self

    def build(self) -> Callable[[T], Token]:
        """Build the final tokenizer function."""
        # Captures state in closure
        def tokenize(value: T) -> Token:
            # Validation, normalization, conversion...
        return tokenize
```

### Scala TokenizerBuilder

Use **mutable state during building**, then return immutable function:

```scala
class TokenizerBuilder[T] {
  private var normalizers: List[String => String] = List()
  private var validators: List[T => Boolean] = List()
  private var metadata: Map[String, Any] = Map()

  def withNormalizer(normalizer: String => String): TokenizerBuilder[T] = {
    normalizers = normalizers :+ normalizer
    this
  }

  def withValidator(validator: T => Boolean): TokenizerBuilder[T] = {
    validators = validators :+ validator
    this
  }

  def withMetadata(pairs: (String, Any)*): TokenizerBuilder[T] = {
    metadata = metadata ++ pairs.toMap
    this
  }

  def build(): T => Token = { (value: T) =>
    // Validate
    validators.foreach { validator =>
      if (!validator(value)) {
        throw new IllegalArgumentException(s"Validation failed for $value")
      }
    }

    // Convert to string
    var strValue = value.toString

    // Normalize
    normalizers.foreach { normalizer =>
      strValue = normalizer(strValue)
    }

    Token(strValue, TokenType.STRING, metadata)
  }
}
```

**Key pattern**: Builder returns a **function** `T => Token`, not a class. This allows functional composition.

### Using the Builder

```scala
val tokenizer = TokenizerBuilder[String]()
  .withNormalizer(_.toLowerCase)
  .withNormalizer(_.replace(" ", "_"))
  .withValidator(_.nonEmpty)
  .withMetadata("type" -> "custom")
  .build()

val token = tokenizer("Hello World")
// Token("hello_world", TokenType.STRING, Map("type" -> "custom"))
```

## Companion Object Pattern for Builder Construction

Make builder construction ergonomic:

```scala
object TokenizerBuilder {
  def apply[T](): TokenizerBuilder[T] = new TokenizerBuilder[T]()
}

// Usage
val builder = TokenizerBuilder[String]()
// More concise than: val builder = new TokenizerBuilder[String]()
```

## Temporal Types: Python datetime → Scala java.time

### Python Temporal

```python
from datetime import date, datetime

class TemporalTokenizer(BaseTokenizer[Union[datetime, date]]):
    ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT = "%Y-%m-%d"

    def tokenize(self, value: datetime | date) -> Token:
        if isinstance(value, datetime):
            fmt = self.ISO_FORMAT
        else:
            fmt = self.DATE_FORMAT
        return Token(value.strftime(fmt), TokenType.TEMPORAL)
```

### Scala java.time (Standard Library)

```scala
import java.time.{LocalDate, LocalDateTime, format}

object TemporalTokenizer extends BaseTokenizer[LocalDateTime | LocalDate] {
  val IsoFormatter = format.DateTimeFormatter.ISO_LOCAL_DATE_TIME
  val DateFormatter = format.DateTimeFormatter.ISO_LOCAL_DATE

  def tokenize(value: LocalDateTime | LocalDate): Token = value match {
    case dt: LocalDateTime => Token(dt.format(IsoFormatter), TokenType.TEMPORAL)
    case d: LocalDate => Token(d.format(DateFormatter), TokenType.TEMPORAL)
  }
}
```

**Note**: Scala uses `java.time.*` (from Java 8+), not custom datetime libraries.

## Union Types in Scala

**Python Union:**
```python
TemporalTokenizer(BaseTokenizer[Union[datetime, date]]):
    def tokenize(self, value: datetime | date) -> Token:
        # Pattern match by type
```

**Scala Union (using sealed trait or pattern match):**
```scala
type TemporalValue = LocalDateTime | LocalDate

abstract class TemporalTokenizer[T <: (LocalDateTime | LocalDate)] extends BaseTokenizer[T] {
  def tokenize(value: T): Token = value match {
    case dt: LocalDateTime => handleDateTime(dt)
    case d: LocalDate => handleDate(d)
    case _ => sys.error("Unexpected type")
  }
}
```

**Or use sealed traits for clarity:**
```scala
sealed trait TemporalValue
case class DateTimeValue(dt: LocalDateTime) extends TemporalValue
case class DateValue(d: LocalDate) extends TemporalValue

class TemporalTokenizer extends BaseTokenizer[TemporalValue] {
  def tokenize(value: TemporalValue): Token = value match {
    case DateTimeValue(dt) => Token(dt.format(IsoFormatter), TokenType.TEMPORAL)
    case DateValue(d) => Token(d.format(DateFormatter), TokenType.TEMPORAL)
  }
}
```

## JSON Handling with Circe

### Python JSON

```python
import json
from typing import Union

JsonValue = Union[str, int, float, bool, None, list["JsonValue"], dict[str, "JsonValue"]]

class JsonTokenizer:
    def tokenize(self, value: JsonValue) -> Token:
        if self.pretty:
            json_str = json.dumps(value, indent=2)
        else:
            json_str = json.dumps(value)
        return Token(json_str, TokenType.STRUCTURED, {"json": True})
```

### Scala with Circe

Circe is the idiomatic JSON library for Scala:

```scala
import io.circe.Json
import io.circe.syntax._

class JsonTokenizer(pretty: Boolean = false) {
  def tokenize(value: Json): Token = {
    val jsonStr = if (pretty) {
      value.spaces2
    } else {
      value.noSpaces
    }
    Token(jsonStr, TokenType.STRUCTURED, Map("json" -> true))
  }

  def tokenizePath(value: Json, path: String): Option[Token] = {
    val parts = path.split("\\.")
    var current: Option[Json] = Some(value)

    for (part <- parts) {
      current = current.flatMap { json =>
        if (json.isObject) {
          json.hcursor.downField(part).focus
        } else if (json.isArray && part.matches("\\d+")) {
          json.hcursor.downN(part.toInt).focus
        } else {
          None
        }
      }
    }

    current.map(tokenize)
  }
}
```

**Setup in build.sbt:**
```scala
libraryDependencies += "io.circe" %% "circe-core" % "0.14.5"
libraryDependencies += "io.circe" %% "circe-parser" % "0.14.5"
```

**Using in tests:**
```scala
import io.circe.parser._

val json = parse("""{"key": "value"}""").getOrElse(Json.Null)
val token = tokenizer.tokenize(json)
```

## WhitespaceTokenizer Pattern

### Python Implementation

```python
class WhitespaceTokenizer:
    def __init__(self, lowercase: bool = False, min_length: int = 0,
                 max_length: int | None = None, strip_punctuation: bool = False):
        self.lowercase = lowercase
        self.min_length = min_length
        self.max_length = max_length
        self.strip_punctuation = strip_punctuation
        self._punctuation = set(".,!?;:'\"()[]{}")

    def _process_token(self, word: str) -> str | None:
        if self.strip_punctuation:
            word = word.strip("".join(self._punctuation))
        if self.lowercase:
            word = word.lower()
        if len(word) < self.min_length:
            return None
        if self.max_length is not None and len(word) > self.max_length:
            word = word[: self.max_length]
        return word if word else None

    def tokenize(self, text: str) -> list[Token]:
        words = text.split()
        tokens: list[Token] = []
        for i, word in enumerate(words):
            processed = self._process_token(word)
            if processed is not None:
                token = Token(value=processed, token_type=TokenType.STRING,
                             metadata={"position": i, "original": word})
                tokens.append(token)
        return tokens
```

### Scala Implementation

```scala
class WhitespaceTokenizer(
  lowercase: Boolean = false,
  minLength: Int = 0,
  maxLength: Option[Int] = None,
  stripPunctuation: Boolean = false
) {
  private val punctuation = Set(".,!?;:'\"()[]{}".toCharArray: _*)

  private def processToken(word: String): Option[String] = {
    var processed = word

    if (stripPunctuation) {
      processed = processed.trim { c => punctuation.contains(c) }
    }

    if (lowercase) {
      processed = processed.toLowerCase
    }

    if (processed.length < minLength) {
      None
    } else if (maxLength.exists(processed.length > _)) {
      Some(processed.take(maxLength.get))
    } else if (processed.nonEmpty) {
      Some(processed)
    } else {
      None
    }
  }

  def tokenize(text: String): List[Token] = {
    text.split("\\s+").zipWithIndex.flatMap { case (word, i) =>
      processToken(word).map { processed =>
        Token(
          value = processed,
          tokenType = TokenType.STRING,
          metadata = Map("position" -> i, "original" -> word)
        )
      }
    }.toList
  }

  def tokenizeToStrings(text: String): List[String] =
    tokenize(text).map(_.value)

  def tokenizeWithPositions(text: String): List[(String, Int, Int)] = {
    var currentPos = 0
    text.split("\\s+").flatMap { word =>
      val start = text.indexOf(word, currentPos)
      val end = start + word.length
      val result = processToken(word).map { processed =>
        (processed, start, end)
      }
      currentPos = end
      result
    }.toList
  }

  def countTokens(text: String): Int = tokenize(text).length
}
```

**Key Scala idioms:**
- Use `split("\\s+")` instead of `split()`
- Use `zipWithIndex` for enumeration
- Use `Option.map` and `flatMap` instead of null checks
- Use `.trim { predicate }` for character set trimming
- `nonEmpty` instead of `!= ""`

## Type-Safe Numeric Tokenizer

### Python Numeric Tokenizer

```python
from decimal import Decimal

class NumericTokenizer(BaseTokenizer[NumericT]):
    def __init__(self, precision: int = 6, format_options: dict[str, Any] = {}):
        self.precision = precision
        self.format_options = format_options

    def tokenize(self, value: NumericT) -> Token:
        if isinstance(value, Decimal):
            str_value = f"{value:.{self.precision}f}"
        elif isinstance(value, float):
            str_value = f"{value:.{self.precision}f}"
        else:
            str_value = str(value)
        return Token(str_value, TokenType.NUMERIC, {"original_type": type(value).__name__})
```

### Scala Numeric Tokenizer

```scala
import scala.math.BigDecimal

class NumericTokenizer(
  precision: Int = 6,
  formatOptions: Map[String, Any] = Map()
) extends BaseTokenizer[Any] {
  def tokenize(value: Any): Token = {
    val (strValue, originalType) = value match {
      case d: BigDecimal => (f"$d%.${precision}f", "BigDecimal")
      case f: Float => (f"$f%.${precision}f", "Float")
      case d: Double => (f"$d%.${precision}f", "Double")
      case i: Int => (i.toString, "Int")
      case l: Long => (l.toString, "Long")
      case _ => (value.toString, value.getClass.getSimpleName)
    }

    Token(
      strValue,
      TokenType.NUMERIC,
      Map("original_type" -> originalType) ++ formatOptions
    )
  }
}
```

**Note**: Scala's `f""` string interpolation provides type-safe formatting.

## Iterator-Based Batch Processing

### Python (Generator)

```python
class BaseTokenizer(ABC, Generic[T]):
    def tokenize_batch(self, values: Iterable[T]) -> Iterator[Token]:
        """Lazy tokenization of multiple values."""
        for v in values:
            yield self.tokenize(v)
```

### Scala (Iterator)

```scala
abstract class BaseTokenizer[T] {
  def tokenize(value: T): Token

  def tokenizeBatch(values: Iterable[T]): Iterator[Token] =
    values.iterator.map(tokenize)
}
```

**Use case**: For large datasets, `Iterator` provides lazy evaluation without loading all tokens into memory.

## Registry Pattern with Generic Containers

### Python TokenRegistry

```python
class TokenRegistry(Generic[T]):
    def __init__(self) -> None:
        self._registry: dict[str, TokenContainer[T]] = {}
        self._handlers: list[Callable[[T], Token | None]] = []

    def register(self, key: str, container: TokenContainer[T]) -> None:
        self._registry[key] = container

    def add_handler(self, handler: Callable[[T], Token | None]) -> None:
        self._handlers.append(handler)

    def process(self, key: str) -> list[Token | None]:
        container = self._registry.get(key)
        if container is None:
            return []
        # Process all items through handlers...
```

### Scala TokenRegistry

```scala
class TokenRegistry[T] {
  private var registry: Map[String, TokenContainer[T]] = Map()
  private var handlers: List[T => Option[Token]] = List()

  def register(key: String, container: TokenContainer[T]): Unit =
    registry = registry + (key -> container)

  def addHandler(handler: T => Option[Token]): Unit =
    handlers = handlers :+ handler

  def process(key: String): List[Option[Token]] = {
    registry.get(key) match {
      case Some(container) =>
        container.getAll.toList.map { item =>
          handlers.collectFirst {
            case handler if handler(item).nonEmpty => handler(item).get
          }
        }
      case None => List()
    }
  }
}
```

**Key pattern**: Use `Map.get()` returning `Option`, then `match` or `flatMap`.

## Functor and Monad Operations

### Python Functor/Monad

```python
class TokenFunctor(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    def map(self, func: Callable[[T], Any]) -> "TokenFunctor[Any]":
        return TokenFunctor(func(self._value))

    def flat_map(self, func: Callable[[T], "TokenFunctor[Any]"]) -> "TokenFunctor[Any]":
        return func(self._value)

    def get_or_else(self, default: T) -> T:
        return self._value if self._value is not None else default
```

### Scala Equivalent (Wrapping Option)

```scala
class TokenFunctor[T](value: T) {
  def map[U](func: T => U): TokenFunctor[U] =
    new TokenFunctor(func(value))

  def flatMap[U](func: T => TokenFunctor[U]): TokenFunctor[U] =
    func(value)

  def getOrElse(default: T): T =
    if (value != null) value else default

  def get: T = value
}

object TokenFunctor {
  def pure[T](value: T): TokenFunctor[T] = new TokenFunctor(value)
}
```

**Better approach**: Use `Option[T]` directly:
```scala
// Instead of TokenFunctor
val result: Option[Token] = Some(token)
result.map(t => t.copy(value = t.value.toUpperCase))
       .flatMap(tokenize)
```

Scala's `Option` has `map`, `flatMap`, `getOrElse` built-in.
