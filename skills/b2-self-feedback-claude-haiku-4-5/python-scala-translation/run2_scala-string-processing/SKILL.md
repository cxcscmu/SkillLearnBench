---
name: scala-string-processing
description: String manipulation, formatting, and regex patterns in Scala
---

# String Processing in Scala

## String Formatting

```scala
// f-string style (Scala 2.13+)
val value = 42
val formatted = f"Value: $value%d"

// String format (compatible)
String.format("%.2f", 3.14159)

// String interpolation
val name = "world"
s"Hello $name"  // simple interpolation
f"Pi: ${3.14159}%.2f"  // formatted interpolation
```

## Numeric Precision

```scala
// For Double/Float
val d = 3.14159
String.format("%.2f", d)  // "3.14"

// For BigDecimal
val bd: BigDecimal = BigDecimal("3.14159")
String.format("%.2f", bd.doubleValue)

// Using precision variable
val precision = 4
String.format(s"%.${precision}f", value)
```

## Working with Character Sets and Punctuation

```scala
// String to set of characters
val punctuation = ".,!?;:'\"()[]{}" .toSet

// Check if character is in set
if (punctuation.contains(c)) { ... }

// Strip leading/trailing punctuation
val stripped = word
  .dropWhile(punctuation.contains)
  .reverse
  .dropWhile(punctuation.contains)
  .reverse

// Or using regex
word.replaceAll("^[.,!?;:'\"]|[.,!?;:'\"']$", "")
```

## Whitespace Splitting

```scala
// Split by whitespace
val words = "hello world test".split("\\s+").toVector

// Split with filter
text.split("\\s+").filter(_.nonEmpty)

// Preserve structure
val (first, rest) = words.splitAt(1)
```

## String Validation

```scala
// Check if all digits
if (part.forall(_.isDigit)) { ... }

// Check emptiness
if (str.nonEmpty) { ... }
if (str.isEmpty) { ... }

// Check length
if (str.length < minLength) { ... }
```

## Case Conversion

```scala
str.toLowerCase  // → "hello"
str.toUpperCase  // → "HELLO"
```
