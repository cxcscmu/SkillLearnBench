---
name: scala-functional-abstractions
description: Implementing tokenization logic using functional patterns and standard library collections.
---

### Functional Implementation Guidelines
- **Traits for Strategy**: Define a `Tokenizer` base trait. Instead of complex inheritance hierarchies, prefer composition where possible, or use the `Self-Type` annotation if tight coupling to a configuration is required.
- **Collection API**: Leverage Scala's `Iterable` and `Iterator` for lazy processing. Avoid mutable loops (`for` with `var`) in favor of `map`, `flatMap`, `filter`, and `foldLeft`.
- **Batch Processing**: Implement `tokenizeBatch` using parallel collections (`.par`) or `Future` if the data volume requires concurrency, ensuring the code remains compliant with Scala 2.13.
- **Error Handling**: Use `Try[T]` or `Either[Throwable, T]` to wrap potentially failing operations (like numeric parsing) instead of throwing raw exceptions.