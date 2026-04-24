---
name: scala-functional-error-handling
description: Handling absence of values and errors in Scala using Option, Try, and Either instead of nulls and exceptions.
---

Scala discourages the use of `null` and exception throwing for control flow, preferring functional error handling types from the standard library.

### 1. Handling Missing Values (`Option`)
Instead of returning `None` as in Python, Scala methods should return `Option[T]`.

**Python:**
```python
def get_metadata(self) -> dict | None:
    return self.metadata if self.metadata else None
```

**Scala:**
```scala
def getMetadata: Option[Map[String, String]] = {
  if (metadata.nonEmpty) Some(metadata) else None
}
```

### 2. Handling Exceptions (`Try`)
When parsing data (like numbers or dates), Python uses `try...except`. Scala uses `scala.util.Try`, which can be easily mapped to an `Option` if you only care about success/failure.

**Python:**
```python
def parse_number(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None
```

**Scala:**
```scala
import scala.util.Try

def parseNumber(text: String): Option[Double] = {
  Try(text.toDouble).toOption
}
```

### 3. Collection Safety
When operating on collections, avoid operations that can throw exceptions (like `.head`). Use safe alternatives (like `.headOption`).