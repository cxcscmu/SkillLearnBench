---
name: python-scala-libraries
description: Mapping standard and common libraries from Python to Scala, including datetime, decimal, and JSON.
---

# Python to Scala Libraries and Specialized Types

This skill covers the translation of library-specific functionality.

## Datetime
- **Python**: `datetime.datetime`, `datetime.date`.
- **Scala**: `java.time.LocalDateTime`, `java.time.LocalDate`.
- **Formatting**: `java.time.format.DateTimeFormatter`.

| Python | Scala |
|--------|-------|
| `dt.strftime("%Y-%m-%d")` | `dt.format(DateTimeFormatter.ofPattern("yyyy-MM-dd"))` |
| `datetime.now()` | `LocalDateTime.now()` |

## Decimal
- **Python**: `decimal.Decimal`.
- **Scala**: `BigDecimal`.
- **Formatting**: `f"$decimal%.2f"`.

## JSON (Circe)
- **Python**: `json.dumps(obj)`, `json.loads(str)`.
- **Scala (Circe)**: `obj.asJson.noSpaces`, `parse(str)`.
- **Recursive JSON**: Use `io.circe.Json` for a safe representation.

## Error Handling
- **Python**: `try...except`, `raise RuntimeError`.
- **Scala**: `Try[T]` (Success/Failure), `Either[L, R]`.
- **Runtime Error**: `throw new RuntimeException("...")`.
```scala
import scala.util.Try
val result = Try(operation()) // Success(v) or Failure(e)
```
