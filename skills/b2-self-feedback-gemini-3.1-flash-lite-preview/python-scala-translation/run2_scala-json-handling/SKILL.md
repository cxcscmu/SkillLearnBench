---
name: run2_scala-json-handling
description: Idiomatic JSON handling using Circe.
---

### Standard Approach

1. **Imports**: `import io.circe._, io.circe.parser._, io.circe.syntax._`
2. **Decoding**: Use `decode[T](jsonString)` (returns `Either[DecodingFailure, T]`).
3. **Encoding**: Use `obj.asJson` (returns `Json`).
