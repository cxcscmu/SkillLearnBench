---
name: run2_scala-builder
description: Implementing an immutable fluent builder in Scala with companion object apply, varargs metadata, and a build() method returning a function — translating Python's mutable builder class.
---

# Scala Immutable Fluent Builder Pattern

## Python Mutable Builder → Scala Immutable Builder

Python accumulates state by mutating lists/dicts:
```python
class TokenizerBuilder(Generic[T]):
    def __init__(self):
        self._normalizers: list[Callable[[str], str]] = []
        self._validators: list[Callable[[T], bool]] = []
        self._metadata: dict[str, Any] = {}

    def with_normalizer(self, norm) -> "TokenizerBuilder[T]":
        self._normalizers.append(norm)  # mutates
        return self

    def build(self) -> Callable[[T], Token]:
        normalizers = self._normalizers.copy()  # defensive copy needed!
        ...
```

Scala uses an immutable builder — each `with*` call returns a **new** instance:
```scala
final class TokenizerBuilder[T] private (
  normalizers: List[String => String],
  validators:  List[T => Boolean],
  meta:        Map[String, Any]
) {
  def withNormalizer(f: String => String): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers :+ f, validators, meta)    // creates new instance

  def withValidator(p: T => Boolean): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers, validators :+ p, meta)

  def withMetadata(entries: (String, Any)*): TokenizerBuilder[T] =
    new TokenizerBuilder(normalizers, validators, meta ++ entries.toMap)

  def build(): T => Token = { value =>
    validators.foreach { v =>
      if (!v(value)) throw new IllegalArgumentException(s"Validation failed for $value")
    }
    val str = normalizers.foldLeft(value.toString)((s, norm) => norm(s))
    Token(str, TokenType.STRING, meta)
  }
}
```

**Benefits of immutable builder:**
- No defensive copy needed in `build()` — captured state is already immutable
- Thread-safe by default — no shared mutable state
- Each intermediate builder is a valid value (can branch/share)

## Companion Object for Clean API

Python: `builder = TokenizerBuilder()`
Scala companion:
```scala
object TokenizerBuilder {
  def apply[T](): TokenizerBuilder[T] =
    new TokenizerBuilder[T](Nil, Nil, Map.empty)
}
```

Usage (calling convention matches Python):
```scala
val tokenizer = TokenizerBuilder[String]()   // apply() invoked implicitly
  .withNormalizer(_.toLowerCase)
  .withNormalizer(_.replace(" ", "_"))
  .withValidator(_.nonEmpty)
  .withMetadata("type" -> "custom")          // varargs tuple syntax
  .build()

val token = tokenizer("Hello World")
// token.value    == "hello_world"
// token.metadata == Map("type" -> "custom")
```

## Key Design Choices

| Python                    | Scala                          | Reason                              |
|---------------------------|--------------------------------|-------------------------------------|
| Mutable `list.append`     | `list :+ elem` → new list      | Immutability, thread safety          |
| `**kwargs` in withMetadata| `(String, Any)*` varargs       | Scala convention for map-like params |
| `dict.update`             | `map ++ other.toMap`           | Immutable map merge                  |
| `Callable[[T], Token]`    | `T => Token` (function type)   | Scala first-class function type      |
| `for v in validators`     | `foldLeft` for normalizers     | Functional pipeline                  |

## WhitespaceTokenizer — Practical Tokenizer with Options

```scala
final class WhitespaceTokenizer(
  lowercase:        Boolean     = false,
  minLength:        Int         = 0,
  maxLength:        Option[Int] = None,
  stripPunctuation: Boolean     = false
) {
  private val punctuation: Set[Char] =
    Set('.', ',', '!', '?', ';', ':', '\'', '"', '(', ')', '[', ']', '{', '}')

  // Python's str.strip(chars) equivalent: drop from both ends
  private def processWord(word: String): Option[String] = {
    val stripped =
      if (stripPunctuation)
        word.dropWhile(punctuation).reverse.dropWhile(punctuation).reverse
      else word
    val lowered = if (lowercase) stripped.toLowerCase else stripped
    if (lowered.length < minLength) None
    else {
      val truncated = maxLength.filter(_ < lowered.length).fold(lowered)(lowered.take)
      if (truncated.isEmpty) None else Some(truncated)
    }
  }

  def tokenize(text: String): List[Token] = {
    val words = if (text.trim.isEmpty) Array.empty[String] else text.trim.split("\\s+")
    words.zipWithIndex.toList.flatMap { case (word, idx) =>
      processWord(word).map(Token(_, TokenType.STRING, Map("position" -> idx, "original" -> word)))
    }
  }
}
```

**Python `str.strip(chars)` → Scala pattern:**
```scala
word.dropWhile(charSet).reverse.dropWhile(charSet).reverse
```
This correctly removes any characters from `charSet` at both the start and end of the string.
