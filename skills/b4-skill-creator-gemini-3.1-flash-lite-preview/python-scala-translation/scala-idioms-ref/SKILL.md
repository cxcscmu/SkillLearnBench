name: scala-idioms-ref
description: Idiomatic Scala patterns for common Python idioms. Use this to translate Pythonic code into idiomatic Scala 2.13. Covers case classes, Option/Either, pattern matching, collections, and higher-order functions.
---

## Idiomatic Translations (Python -> Scala)

### 1. Data Structures
- **Python**: `@dataclass(frozen=True)` -> **Scala**: `case class Token(value: String, tokenType: TokenType, metadata: Map[String, Any] = Map.empty)`
- **Python**: `Union[str, int]` -> **Scala**: `sealed trait ValueType; case class StringVal(v: String) extends ValueType; ...` (ADT)
- **Python**: `list[T]` -> **Scala**: `List[T]` or `Seq[T]` (immutable)

### 2. Control Flow
- **Python**: `if x is None: ...` -> **Scala**: `x match { case None => ... }` or `x.fold(...)`
- **Python**: `for v in values: yield v` -> **Scala**: `values.iterator`

### 3. Error Handling
- **Python**: `try...except` / `raise` -> **Scala**: `Try { ... }` or `Either[Error, Result]`

### 4. Functional Programming
- **Python**: `Callable[[T], R]` -> **Scala**: `T => R`
- **Python**: `list comprehension` -> **Scala**: `list.map(f)` or `for { x <- list } yield f(x)`
