---
name: scala-tokenizer-implementation-guide
description: Use this skill when writing /root/Tokenizer.scala. It provides the concrete implementation strategy, Scala idioms, and compilation workflow for translating the Python Tokenizer to Scala 2.13.
---

# Implementing /root/Tokenizer.scala

## Prerequisites
- You MUST have already read `/root/Tokenizer.py` (use read-python-tokenizer-source skill)
- You MUST have already read `/root/TokenizerSpec.scala` (use read-scala-test-spec skill)

## Implementation Strategy

### 1. File Structure
```scala
package tokenizer  // or whatever package the test spec imports from

// All code in a single file /root/Tokenizer.scala
```

### 2. TokenType — Use Scala 2.13 Enumeration or sealed trait

**If the test uses `TokenType.STRING` style access, use Enumeration:**
```scala
object TokenType extends Enumeration {
  type TokenType = Value
  val STRING, NUMERIC, TEMPORAL, WHITESPACE, UNKNOWN = Value
  // Add all values from the Python enum
}
```

**If the test uses pattern matching or case objects:**
```scala
sealed trait TokenType
object TokenType {
  case object STRING extends TokenType
  case object NUMERIC extends TokenType
  // etc.
}
```

### 3. Token — Use case class
```scala
case class Token(
  value: String,
  tokenType: TokenType.TokenType,  // or TokenType depending on approach
  position: Int = 0,
  metadata: Map[String, String] = Map.empty
)
```
- Match field names exactly to what the test spec expects
- Use default values matching the Python defaults

### 4. BaseTokenizer — Use trait
```scala
trait BaseTokenizer {
  def tokenize(text: String): List[Token]  // or Seq — match test expectations
}
```

### 5. Concrete Tokenizers

**StringTokenizer:**
- Copy regex patterns exactly from Python
- Use `scala.util.matching.Regex`
- Use `regex.findAllMatchIn(text)` to iterate matches
- Build Token instances with position and metadata

```scala
class StringTokenizer extends BaseTokenizer {
  // Python: pattern = r'[a-zA-Z_][a-zA-Z0-9_]*'  (example — use actual pattern from source)
  private val pattern = """[a-zA-Z_][a-zA-Z0-9_]*""".r
  
  override def tokenize(text: String): List[Token] = {
    pattern.findAllMatchIn(text).map { m =>
      Token(
        value = m.matched,
        tokenType = TokenType.STRING,
        position = m.start,
        metadata = Map("length" -> m.matched.length.toString)  // match Python metadata keys exactly
      )
    }.toList
  }
}
```

**NumericTokenizer:**
- Translate all numeric regex patterns (integers, floats, scientific notation)
- Preserve the exact regex from Python
- Handle metadata (e.g., "isInteger", "isFloat", "value")

**TemporalTokenizer:**
- Translate date/time regex patterns exactly
- Handle metadata for format detection

**UniversalTokenizer:**
- Combines multiple tokenizers
- Implement fallback/priority logic from Python
- Sort by position if Python does that

**WhitespaceTokenizer:**
- Simple `text.split("\\s+")` approach
- Track positions

### 6. TokenizerBuilder — Builder Pattern
```scala
class TokenizerBuilder {
  private var tokenizers: List[BaseTokenizer] = List.empty
  // Add builder methods matching Python: addStringTokenizer, addNumericTokenizer, etc.
  // Return `this` for chaining
  def build(): BaseTokenizer = { /* return composed tokenizer */ }
}
```

### 7. Free Functions — Package object or companion object
Check where the test imports them from. Likely a package object:
```scala
package object tokenizer {
  def tokenize(text: String): List[Token] = { /* use UniversalTokenizer or default */ }
  def tokenizeBatch(texts: Seq[String]): Seq[List[Token]] = texts.map(tokenize)
  def toToken(value: String): Token = { /* create single token with type inference */ }
  def withMetadata(token: Token, metadata: Map[String, String]): Token = token.copy(metadata = token.metadata ++ metadata)
}
```

**OR** if they're in an object:
```scala
object Tokenizer {
  def tokenize(text: String): List[Token] = ...
  // etc.
}
```

### 8. Scala Idioms to Apply
- **Pattern matching** instead of if-elif chains for type detection
- **Option** instead of null/None for optional values
- **Immutable collections** (List, Map) by default
- **Case class copy** for creating modified tokens
- **String interpolation** `s"..."` instead of f-strings
- **`scala.util.matching.Regex`** for all regex operations
- **No mutable state** where possible
- **`map`, `flatMap`, `filter`, `collect`** instead of imperative loops
- **Method chaining** with builder pattern returning `this`

### 9. Error Handling
- Empty string input → return empty List
- Invalid input → return UNKNOWN token type or empty result (match Python behavior exactly)
- Use `Option` where Python uses `Optional` or `None`
- Use `Try`/`Either` only if Python explicitly raises exceptions that need catching

## Compilation and Testing Workflow

### Step 1: Write the implementation
```bash
cat > /root/Tokenizer.scala << 'SCALA'
// ... your implementation ...
SCALA
```

### Step 2: Compile just the implementation
```bash
scalac /root/Tokenizer.scala
```
Fix any compilation errors before proceeding.

### Step 3: Compile with test spec
Check what test framework the spec uses (ScalaTest, MUnit, specs2) and compile both:
```bash
# Find available jars
find / -name "*.jar" 2>/dev/null | grep -i scalatest
# Compile together
scalac -cp ".:path/to/scalatest.jar" /root/Tokenizer.scala /root/TokenizerSpec.scala
```

### Step 4: Run tests
```bash
# ScalaTest example
scala -cp ".:path/to/scalatest.jar" org.scalatest.run TokenizerSpec
```

### Step 5: Iterate on failures
- Read error messages carefully
- Common issues: wrong collection type (List vs Seq), wrong TokenType representation, missing methods, wrong package
- Fix and recompile

## Common Pitfalls
1. **Regex escaping**: In Scala triple-quoted strings `"""..."""`, backslashes are literal. In regular strings, double them: `"\\d+"`.
2. **Package mismatch**: If test says `import tokenizer._`, your code must be in `package tokenizer` (possibly in a package object for free functions).
3. **Enumeration import**: If using `Enumeration`, you may need `import TokenType._` for the type alias.
4. **Position tracking**: Python's `re.finditer` gives `.start()` — Scala's `findAllMatchIn` gives `.start`.
5. **Metadata values as String**: Python may store int metadata; Scala Map[String, String] needs `.toString`.
6. **If the spec expects `package object`**: You CANNOT have a `package object tokenizer` inside `package tokenizer` in the same file easily. Put the package object in its own declaration block.