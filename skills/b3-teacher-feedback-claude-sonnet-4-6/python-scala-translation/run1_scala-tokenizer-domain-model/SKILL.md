---
name: scala-tokenizer-domain-model
description: Use when implementing tokenizer abstractions in Scala 2.13 — covers Token/TokenType ADTs, tokenizer traits, builder pattern, and batch processing conventions
---

# Scala Tokenizer Domain Model

## Core Data Types

### TokenType ADT
```scala
sealed trait TokenType {
  def value: String
}
object TokenType {
  case object String   extends TokenType { val value = "string"   }
  case object Numeric  extends TokenType { val value = "numeric"  }
  case object Temporal extends TokenType { val value = "temporal" }
  case object Whitespace extends TokenType { val value = "whitespace" }
  case object Unknown  extends TokenType { val value = "unknown"  }

  // Lookup by string name
  def fromString(s: String): Option[TokenType] = s.toLowerCase match {
    case "string"     => Some(String)
    case "numeric"    => Some(Numeric)
    case "temporal"   => Some(Temporal)
    case "whitespace" => Some(Whitespace)
    case "unknown"    => Some(Unknown)
    case _            => None
  }
}
```

### Token Case Class
```scala
case class Token(
  value: String,
  tokenType: TokenType,
  metadata: Map[String, Any] = Map.empty
) {
  def withMetadata(key: String, v: Any): Token =
    copy(metadata = metadata + (key -> v))

  def withMetadata(pairs: (String, Any)*): Token =
    copy(metadata = metadata ++ pairs)
}
```

Key design: `copy()` enables immutable updates — never mutate the token.

## BaseTokenizer Trait

```scala
trait BaseTokenizer {
  /** Tokenize a single text input */
  def tokenize(text: String): List[Token]

  /** Tokenize a batch; default delegates to tokenize per element */
  def tokenizeBatch(texts: Seq[String]): List[List[Token]] =
    texts.toList.map(tokenize)
}
```

## Concrete Tokenizers

### StringTokenizer
```scala
class StringTokenizer(
  lowercase: Boolean = false,
  stripPunctuation: Boolean = false
) extends BaseTokenizer {

  override def tokenize(text: String): List[Token] = {
    val processed = if (lowercase) text.toLowerCase else text
    val cleaned   = if (stripPunctuation) processed.replaceAll("[^\\w\\s]", "") else processed
    cleaned.split("\\s+")
      .filter(_.nonEmpty)
      .map(w => Token(w, TokenType.String))
      .toList
  }
}
```

### NumericTokenizer
```scala
class NumericTokenizer extends BaseTokenizer {
  private val numericPattern = """-?\d+(\.\d+)?""".r

  override def tokenize(text: String): List[Token] =
    numericPattern.findAllIn(text).toList
      .map(n => Token(n, TokenType.Numeric))
}
```

### TemporalTokenizer
Uses regex to find dates/times:
```scala
class TemporalTokenizer extends BaseTokenizer {
  private val datePattern =
    """\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}""".r

  override def tokenize(text: String): List[Token] =
    datePattern.findAllIn(text).toList
      .map(d => Token(d, TokenType.Temporal))
}
```

### WhitespaceTokenizer
```scala
class WhitespaceTokenizer extends BaseTokenizer {
  override def tokenize(text: String): List[Token] =
    text.split("\\s+")
      .filter(_.nonEmpty)
      .map(w => Token(w, TokenType.Whitespace))
      .toList
}
```

### UniversalTokenizer
Delegates to multiple tokenizers and merges/deduplicates:
```scala
class UniversalTokenizer(tokenizers: List[BaseTokenizer]) extends BaseTokenizer {
  override def tokenize(text: String): List[Token] =
    tokenizers.flatMap(_.tokenize(text))
}
```

## Builder Pattern

```scala
class TokenizerBuilder {
  private var tokenizers: List[BaseTokenizer] = List.empty

  def withStringTokenizer(
    lowercase: Boolean = false,
    stripPunctuation: Boolean = false
  ): TokenizerBuilder = {
    tokenizers = tokenizers :+ new StringTokenizer(lowercase, stripPunctuation)
    this
  }

  def withNumericTokenizer(): TokenizerBuilder = {
    tokenizers = tokenizers :+ new NumericTokenizer()
    this
  }

  def withTemporalTokenizer(): TokenizerBuilder = {
    tokenizers = tokenizers :+ new TemporalTokenizer()
    this
  }

  def withWhitespaceTokenizer(): TokenizerBuilder = {
    tokenizers = tokenizers :+ new WhitespaceTokenizer()
    this
  }

  def build(): UniversalTokenizer = new UniversalTokenizer(tokenizers)
}

object TokenizerBuilder {
  def apply(): TokenizerBuilder = new TokenizerBuilder()
}
```

## Top-Level Functions

These are placed in a package object or standalone object:

```scala
object Tokenizer {
  /** Tokenize a single text with the given tokenizer */
  def tokenize(text: String, tokenizer: BaseTokenizer): List[Token] =
    tokenizer.tokenize(text)

  /** Batch tokenize */
  def tokenizeBatch(
    texts: Seq[String],
    tokenizer: BaseTokenizer
  ): List[List[Token]] =
    tokenizer.tokenizeBatch(texts)

  /** Convert a raw string to a Token with inferred type */
  def toToken(value: String, tokenType: TokenType): Token =
    Token(value, tokenType)

  /** Add metadata to a token */
  def withMetadata(token: Token, key: String, v: Any): Token =
    token.withMetadata(key, v)
}
```

## Idiomatic Scala Patterns for Tokenizers

### Use `Regex` from `scala.util.matching`
```scala
import scala.util.matching.Regex
val pattern: Regex = """\d+""".r
pattern.findAllIn(text).toList
```

### Avoid `null` — use `Option`
```scala
def safeTokenize(text: String): Option[List[Token]] =
  Option(text).filter(_.nonEmpty).map(tokenize)
```

### Use `flatMap` / `collect` for filtering-with-transform
```scala
tokens.collect { case t if t.tokenType == TokenType.Numeric => t.value }
```

### Immutability by Default
- All `Token` fields are `val` (enforced by `case class`)  
- Builder accumulates with `:+` and returns `this` for chaining  
- `copy()` for "modification"

## Error Handling in Tokenization

```scala
import scala.util.{Try, Success, Failure}

def safeParse(text: String): Try[List[Token]] =
  Try(tokenize(text)).recoverWith {
    case e: IllegalArgumentException =>
      Failure(new RuntimeException(s"Bad input: $text", e))
  }
```