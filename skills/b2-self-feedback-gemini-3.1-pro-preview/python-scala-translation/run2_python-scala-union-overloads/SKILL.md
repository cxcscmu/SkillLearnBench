---
name: run2_python-scala-union-overloads
description: Translating Python Union types and @overload to Scala method overloads, type classes, and pattern matching
---

# Translating Python Union types and @overloads

Python uses `@overload` to document signatures, and `Union` or `|` to represent mixed types, handling them at runtime with `isinstance`.
Scala natively supports method overloading and offers pattern matching for dynamic type checking.

## Python
```python
class UniversalTokenizer:
    @overload
    def tokenize(self, value: str) -> Token: ...
    @overload
    def tokenize(self, value: int) -> Token: ...
    
    def tokenize(self, value: Any) -> Token:
        if isinstance(value, str):
            return Token(value, TokenType.STRING)
        # fallback ...
```

## Scala Translation
In Scala, statically-typed overloading is straightforward:
```scala
class UniversalTokenizer {
  def tokenize(value: String): Token = Token(value, TokenType.STRING)
  def tokenize(value: Int): Token = Token(value.toString, TokenType.NUMERIC)
  def tokenizeNull: Token = Token("NULL", TokenType.NULL)
}
```

If you must handle a generic `Any` fallback or a heterogeneous collection, use Pattern Matching:
```scala
def tokenize(value: Any): Token = {
  if (value == null) {
    tokenizeNull
  } else {
    value match {
      case s: String => tokenize(s)
      case i: Int => tokenize(i)
      case t: Tokenizable => Token(t.toToken, TokenType.STRUCTURED)
      case _ => Token(value.toString, TokenType.STRING, Map("fallback" -> true))
    }
  }
}
```

## Idiomatic Scala
Using `Any` is generally discouraged in Scala as it defeats type safety. A more idiomatic approach involves **Type Classes**:
```scala
trait Tokenizer[T] {
  def tokenize(value: T): Token
}
object Tokenizer {
  implicit val stringTokenizer: Tokenizer[String] = (v: String) => Token(v, TokenType.STRING)
}
// Usage: def tokenize[T: Tokenizer](value: T) = implicitly[Tokenizer[T]].tokenize(value)
```
However, direct pattern matching on `Any` is appropriate when translating dynamically-typed legacy systems precisely.
