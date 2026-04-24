---
name: scala-method-overloading
description: Guide for translating Python @overload and dynamic typing (Any, Union) to Scala method overloading and type matching.
---

# Method Overloading and Type Matching

Python uses `@overload` for static type checking but implements dispatch dynamically checking `isinstance()` at runtime. Scala natively supports method overloading and pattern matching for safe dynamic dispatches.

## Translating Union/Overloads

Python:
```python
@overload
def tokenize(self, value: str) -> Token: ...
@overload
def tokenize(self, value: int) -> Token: ...
def tokenize(self, value: Any) -> Token:
    if isinstance(value, str): return Token(value)
    if isinstance(value, int): return Token(str(value))
    return Token(str(value))
```

Scala:
```scala
// Option 1: True method overloading (Preferred when possible)
def tokenize(value: String): Token = Token(value)
def tokenize(value: Int): Token = Token(value.toString)

// Option 2: Pattern Matching on Any (When a generic dispatch method is required)
def tokenize(value: Any): Token = value match {
  case s: String => Token(s)
  case i: Int => Token(i.toString)
  case t: Tokenizable => Token(t.toToken)
  case null => Token("NULL")
  case other => Token(other.toString)
}
```

### Dealing with `None` and `Null`
In Scala, `null` is a bottom type, but it's not idiomatic. However, when interfacing with raw `Any` parameters, handling `null` via `case null =>` is common. Otherwise, use `Option[T]`. To represent a Python parameter that can be `None`, use an `Option` type or a default argument.
