---
name: scala-java-time-handling
description: Working with Java's LocalDate and LocalDateTime in Scala for temporal tokenization
---

# Java Time API in Scala

## Import Statements

```scala
import java.time.{LocalDate, LocalDateTime}
import java.time.format.DateTimeFormatter
```

## Creating Formatters

```scala
// Predefined patterns
private val isoFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss")
private val dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")

// Using formatter
val formatted = isoFormatter.format(localDateTime)
```

## Handling Optional Format Strings

```scala
// Option for custom format
formatStr match {
  case Some(pattern) => DateTimeFormatter.ofPattern(pattern).format(value)
  case None => defaultFormatter.format(value)
}

// Or with getOrElse
val formatter = formatStr
  .map(DateTimeFormatter.ofPattern)
  .getOrElse(isoFormatter)
formatter.format(value)
```

## Type Matching for Date/Time

```scala
value match {
  case dt: LocalDateTime => isoFormatter.format(dt)
  case d: LocalDate => dateFormatter.format(d)
  case _ => value.toString
}
```

## ISO 8601 Standards

- DateTime: `yyyy-MM-dd'T'HH:mm:ss`
- Date: `yyyy-MM-dd`
- Time: `HH:mm:ss`

## Common Patterns

```scala
// Store formatter as val for reuse (thread-safe)
private val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")

// Format with fallback
def formatDate(date: LocalDate): String = {
  try {
    formatter.format(date)
  } catch {
    case _: Exception => date.toString
  }
}
```
