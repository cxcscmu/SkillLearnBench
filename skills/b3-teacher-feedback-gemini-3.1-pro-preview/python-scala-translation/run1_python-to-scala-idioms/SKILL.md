---
name: python-to-scala-idioms
description: Idiomatic translation of Python constructs to Scala 2.13, including classes, interfaces, enums, and naming conventions.
---

When translating Python code to Scala, particularly for distributed environments (like Apache Spark), you must favor immutability and functional abstractions. 

### 1. Enums and Constants
Python `Enum` should be translated to a `sealed trait` with `case object` instances in Scala 2.13.

**Python:**
```python
from enum import Enum
class TokenType(Enum):
    STRING = 1
    NUMERIC = 2
```

**Scala 2.13:**
```scala
sealed trait TokenType
object TokenType {
  case object String extends TokenType
  case object Numeric extends TokenType
}
```

### 2. Data Classes
Python `@dataclass` translates perfectly to Scala `case class`. Case classes provide immutability, value-based equality, and pattern matching out of the box.

**Python:**
```python
@dataclass
class Token:
    value: str
    token_type: TokenType
```

**Scala:**
```scala
case class Token(value: String, tokenType: TokenType)
```

### 3. Abstract Base Classes (Interfaces)
Python `ABC` should be converted to Scala `trait`. 

**Python:**
```python
class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> list[Token]: pass
```

**Scala:**
```scala
trait BaseTokenizer {
  def tokenize(text: String): Seq[Token]
}
```

### 4. Naming Conventions
- **Classes/Traits/Objects:** PascalCase (e.g., `StringTokenizer`).
- **Methods/Variables:** camelCase (e.g., `tokenizeBatch`, `tokenType`). 
- **Packages:** lowercase (e.g., `com.example.tokenizer`).
- Scala avoids snake_case completely.

### 5. Companion Objects for Static Methods
Python standalone functions or `@staticmethod` should be placed in a `companion object` (an `object` with the same name as a `class` or `trait` in the same file).