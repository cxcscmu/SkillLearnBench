---
name: scala-api-compatibility
description: Aligning the implementation with provided Test Specifications.
---

### Compatibility Requirements
- **API Signature**: Strictly match the signatures defined in `TokenizerSpec.scala`. If the spec expects a specific return type (e.g., `Seq[Token]` vs `List[Token]`), ensure the implementation returns the most appropriate general collection type.
- **Factory Pattern**: Implement `TokenizerBuilder` as a companion object or a builder class that provides a fluent API, consistent with Scala's preference for functional builders.
- **Testing Alignment**: Ensure all methods listed in the task (`tokenize`, `toToken`, `withMetadata`, etc.) are public and accessible to the test suite provided in the root directory.