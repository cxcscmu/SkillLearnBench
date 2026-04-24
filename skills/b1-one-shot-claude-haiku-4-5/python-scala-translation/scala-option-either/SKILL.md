---
name: scala-option-either
description: Translating Python's None/Optional to Scala's Option, Either, and Try types
---

# Scala Option, Either, and Try for Python Developers

## Core Concept: Functional Error Handling

Python uses `None` and `Optional[T]` to represent absence. Scala uses types that can be pattern-matched:

| Python | Scala | Purpose |
|--------|-------|---------|
| `None` | `None` (in Option) | Represents absence |
| `Optional[T]` / `T \| None` | `Option[T]` | Represents presence or absence |
| Exception handling | `Either[Err, Success]` | Represents error or success |
| Exception handling | `Try[T]` | Like Either but for exceptions |

## Option[T] - Replace None/Optional

### Python Pattern
```python
def safe_divide(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b

result = safe_divide(10, 2)
if result is not None:
    print(f"Result: {result}")
else:
    print("Division by zero")
```

### Scala Pattern
```scala
def safeDivide(a: Double, b: Double): Option[Double] =
  if (b == 0) None else Some(a / b)

// Pattern matching
safeDivide(10, 2) match {
  case Some(result) => println(s"Result: $result")
  case None => println("Division by zero")
}

// Or functional style
safeDivide(10, 2).foreach(result => println(s"Result: $result"))
```

### Key Option Methods

```scala
val opt: Option[Int] = Some(42)

// Extraction
opt.get        // 42 (throws if None - avoid!)
opt.getOrElse(0)  // 42
opt.orElse(Some(0))  // Some(42)

// Transformation
opt.map(_ * 2)    // Some(84)
opt.flatMap(x => Some(x * 2))  // Some(84)
opt.filter(_ > 40)  // Some(42)

// Iteration
for (v <- opt) println(v)  // prints 42

// Checking
opt.isDefined   // true
opt.isEmpty     // false
```

## Either[L, R] - Represent Success or Failure

Either is more powerful than Option - it carries error information.

### Python Pattern
```python
def validate_age(age: int) -> tuple[bool, str | None]:
    if age < 0:
        return False, "Age cannot be negative"
    if age > 150:
        return False, "Age seems unrealistic"
    return True, None

success, error = validate_age(-5)
if not success:
    print(f"Error: {error}")
```

### Scala Pattern
```scala
def validateAge(age: Int): Either[String, Int] =
  if (age < 0) Left("Age cannot be negative")
  else if (age > 150) Left("Age seems unrealistic")
  else Right(age)

// Pattern matching
validateAge(-5) match {
  case Left(error) => println(s"Error: $error")
  case Right(age) => println(s"Valid age: $age")
}

// Functional style
validateAge(25).map(age => age + 1).foreach(println)
```

### Either is Right-biased (map operates on Right)

```scala
val result: Either[String, Int] = Right(5)

result.map(_ * 2)  // Right(10)
result.flatMap(x => Right(x * 2))  // Right(10)
result.leftMap(s => s.toUpperCase)  // Left side transformation
result.fold(
  error => println(s"Error: $error"),  // Left side
  value => println(s"Success: $value")  // Right side
)
```

## Try[T] - For Exception Handling

Try captures exceptions instead of throwing them.

### Python Pattern
```python
import json

def parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}
```

### Scala Pattern
```scala
import scala.util.Try
import io.circe.parser._

def parseJson(text: String): Try[Json] =
  parse(text).toTry  // Convert Either to Try

// Or with try-catch
def parseJson(text: String): Try[Map[String, String]] = Try {
  Json.fromString(text).as[Map[String, String]].getOrElse(Map())
}

// Usage
parseJson("{}") match {
  case scala.util.Success(json) => println(s"Parsed: $json")
  case scala.util.Failure(ex) => println(s"Error: ${ex.getMessage}")
}
```

## Chaining Operations

### Python Chaining
```python
def process(text: str) -> str | None:
    trimmed = text.strip()
    if not trimmed:
        return None

    parts = trimmed.split()
    if not parts:
        return None

    return parts[0].upper()

result = process("  hello world  ")
```

### Scala Chaining with for-comprehension
```scala
def process(text: String): Option[String] = for {
  trimmed <- Option(text.trim).filter(_.nonEmpty)
  parts <- Option(trimmed.split("\\s+")).filter(_.nonEmpty)
  first <- Option(parts(0))
} yield first.toUpperCase

// Or with flatMap chain
def process(text: String): Option[String] =
  Option(text.trim)
    .filter(_.nonEmpty)
    .map(_.split("\\s+"))
    .filter(_.nonEmpty)
    .map(_(0).toUpperCase)
```

## Converting Between Types

```scala
// Option to Either
val opt: Option[Int] = Some(5)
opt.toRight("Value not found")  // Either[String, Int]

// Either to Option
val either: Either[String, Int] = Right(5)
either.toOption  // Option[Int]

// Try to Either
val attempt: scala.util.Try[Int] = scala.util.Success(5)
attempt.toEither  // Either[Throwable, Int]

// List of Options to Option of List (if all Some)
List(Some(1), Some(2), Some(3)).sequence  // Option[List[Int]]
```

## Pattern in Tokenizer Context

### Python (Returns Token | None)
```python
def tokenize_path(self, value: JsonValue, path: str) -> Token | None:
    parts = path.split(".")
    current = value

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None

    return self.tokenize(current)
```

### Scala (Returns Option[Token])
```scala
def tokenizePath(value: Json, path: String): Option[Token] = {
  val parts = path.split("\\.")
  val finalValue = parts.foldLeft(value) { (current, part) =>
    if (current.isObject) {
      current.hcursor.downField(part).focus.getOrElse(Json.Null)
    } else if (current.isArray) {
      val idx = part.toIntOption.getOrElse(-1)
      if (idx >= 0) current.asArray.flatMap(_.lift(idx)).getOrElse(Json.Null)
      else Json.Null
    } else {
      Json.Null
    }
  }

  if (finalValue == Json.Null) None else Some(tokenize(finalValue))
}
```

## Best Practices

1. **Never use `.get` on Option** - use pattern matching or `.getOrElse`
2. **Use `for` comprehensions** for multiple Option/Either chains
3. **Leverage `.map` and `.flatMap`** for transformations
4. **Use `Either` when you need error information** (not just `Option`)
5. **Use `Try` when wrapping exception-throwing code**
6. **Prefer functional style** - map, flatMap, fold instead of pattern matching on every line
