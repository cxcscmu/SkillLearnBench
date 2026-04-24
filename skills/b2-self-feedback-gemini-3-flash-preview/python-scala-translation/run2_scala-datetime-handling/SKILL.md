---
name: run2_scala-datetime-handling
description: Robust temporal tokenization with Java 8 Time API and DateTimeFormatter.
---

# Temporal Tokenization in Scala

Use `java.time` for all date/time operations.

## Robust Formatting
Handle `LocalDateTime`, `LocalDate`, `ZonedDateTime`, and `Instant`.

```scala
import java.time.{LocalDate, LocalDateTime, ZonedDateTime, Instant}
import java.time.format.DateTimeFormatter

def formatTemporal(value: Any, fmtStr: Option[String]): String = {
  val isoFormat = DateTimeFormatter.ISO_LOCAL_DATE_TIME
  val dateFormat = DateTimeFormatter.ISO_LOCAL_DATE
  
  value match {
    case dt: LocalDateTime => 
      val fmt = fmtStr.map(DateTimeFormatter.ofPattern).getOrElse(isoFormat)
      dt.format(fmt)
    case d: LocalDate =>
      val fmt = fmtStr.map(DateTimeFormatter.ofPattern).getOrElse(dateFormat)
      d.format(fmt)
    case other => other.toString
  }
}
```

## Pattern Matching on Any
Useful for implementing `UniversalTokenizer`'s dispatch logic.
