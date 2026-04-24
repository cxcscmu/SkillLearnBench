---
name: scala-functional-parsing-and-error-handling
description: Implement idiomatic Scala logic for parsing temporal/numeric data and handling batch processing using functional transformations and error types.
---

### Functional Error Handling
Avoid returning `null` or throwing exceptions for expected failures (e.g., failed parsing). Use:
- `Option[Token]`: When a result might be absent.
- `Either[String, Token]`: When you need to provide an error message upon failure.

### Numeric and Temporal Parsing
- **Numeric:** Use `String.toDoubleOption` or `String.toIntOption` to safely convert strings to numbers. If using a version where these aren't available, wrap the logic in `scala.util.Try(s.toDouble).toOption`.
- **Temporal:** Use the `java.time` package (e.g., `LocalDateTime`, `ZonedDateTime`) and `DateTimeFormatter`. Wrap parsing logic in a functional container to handle malformed date strings gracefully.

### Batch Processing
Instead of manual loops, use Scala's collection API for `tokenizeBatch`:
- Use `.map(tokenize)` to transform a sequence of inputs into a sequence of tokens.
- Use `.flatMap` if the tokenization process returns an `Option` and you wish to filter out unsuccessful attempts.

### Standard Library Usage
Prefer Scala's standard library over reinventing logic. For example, use `s.split("\\s+")` or Regex for `WhitespaceTokenizer` logic.