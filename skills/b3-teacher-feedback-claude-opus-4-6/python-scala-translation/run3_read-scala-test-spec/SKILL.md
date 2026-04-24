---
name: read-scala-test-spec
description: Use this skill to read and understand /root/TokenizerSpec.scala to determine the exact expected API signatures, imports, class names, method names, and enum values that the Scala implementation must match.
---

# Reading and Understanding /root/TokenizerSpec.scala

## Step-by-step workflow

1. **Read the test spec completely first** (this is the authoritative source for the API):
   ```
   cat /root/TokenizerSpec.scala
   ```

2. **Extract from the test spec**:
   - **Package declaration**: What package does the spec import from? Your implementation must use the same package.
   - **Import statements**: Exactly what classes/objects/methods are imported? e.g., `import tokenizer._` or `import tokenizer.TokenType._` — this tells you the package and whether things live in companion objects.
   - **TokenType usage**: Are enum values accessed as `TokenType.STRING`, `TokenType.NUMERIC`, etc.? This tells you whether to use a sealed trait + case objects, an Enumeration, or Scala 3 enum (use Scala 2.13 compatible approach).
   - **Token construction**: How are Token instances created in tests? `Token(...)` with what fields?
   - **Tokenizer instantiation**: `new StringTokenizer()`, `StringTokenizer()` (companion object apply), or `TokenizerBuilder`?
   - **Method calls**: Exact method names like `.tokenize(text)`, `.tokenizeBatch(texts)`, return types (List, Seq, Option, etc.)
   - **Free functions**: Are `tokenize`, `tokenizeBatch`, `toToken`, `withMetadata` called as standalone functions (from a package object or imported from an object)?
   - **Assertion patterns**: What types are expected? `List[Token]`, `Seq[Token]`, `Option[Token]`?
   - **Metadata access**: How is metadata accessed on tokens? `.metadata("key")`, `.metadata.get("key")`?

3. **Critical decisions determined by the spec**:
   - Whether to use `sealed trait` + `case object` vs `Enumeration` for TokenType
   - Whether Token is a `case class`
   - Where free functions live (package object vs companion object)
   - What collection types to use (List vs Seq vs Vector)
   - Whether methods return Option or can throw

4. **Write down every test case name** — these are the behaviors you must implement correctly.