---
name: python-to-scala-translation-patterns
description: Use when translating Python OOP/functional code to idiomatic Scala 2.13, covering class hierarchies, enumerations, error handling, and naming conventions
---

# Python to Scala Translation Patterns

## Class and Object Hierarchy

### Enumerations
Python `Enum` → Scala `sealed trait` + `case object`:
```scala
// Python
class TokenType(Enum):
    STRING = "string"
    NUMERIC = "numeric"

// Scala
sealed trait TokenType
object TokenType {
  case object String  extends TokenType
  case object Numeric extends TokenType
  // companion object provides namespace
}
```

### Abstract Base Classes
Python `ABC` / abstract methods → Scala `abstract class` or `trait`:
```scala
// Python
class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[Token]: ...

// Scala
abstract class BaseTokenizer {
  def tokenize(text: String): List[Token]
}
// OR as a trait (preferred for mixin composition)
trait BaseTokenizer {
  def tokenize(text: String): List[Token]
}
```

### Data Classes / Named Tuples
Python `@dataclass` / `NamedTuple` → Scala `case class`:
```scala
// Python
@dataclass
class Token:
    value: str
    token_type: TokenType
    metadata: dict = field(default_factory=dict)

// Scala
case class Token(
  value: String,
  tokenType: TokenType,
  metadata: Map[String, Any] = Map.empty
)
```

## Naming Conventions

| Concept | Python | Scala |
|---------|--------|-------|
| Class | `PascalCase` | `PascalCase` |
| Method/field | `snake_case` | `camelCase` |
| Constant | `UPPER_SNAKE` | `UpperCamelCase` or `camelCase val` |
| Package | `lowercase` | `lowercase` |
| Type param | `T` | `T` |

```scala
// Python: token_type, is_valid, to_token
// Scala: tokenType, isValid, toToken
```

## Optional / None Handling
Python `Optional[T]` / `None` → Scala `Option[T]`:
```scala
// Python
def find(text: str) -> Optional[Token]:
    if condition: return Token(...)
    return None

// Scala
def find(text: String): Option[Token] =
  if (condition) Some(Token(...)) else None
```

## Error Handling
Python `try/except` with custom exceptions → Scala `Try`, `Either`, or `Option`:
```scala
import scala.util.{Try, Success, Failure}

// Python
try:
    result = risky()
except ValueError as e:
    return None

// Scala — Try
def risky(): Try[Token] = Try { /* may throw */ }

// Scala — Either for typed errors
def parse(s: String): Either[String, Token] =
  if (valid(s)) Right(Token(s, ...))
  else Left(s"Invalid input: $s")
```

## Collections
| Python | Scala |
|--------|-------|
| `list` | `List[T]` or `Seq[T]` |
| `dict` | `Map[K, V]` |
| `set` | `Set[T]` |
| `tuple` | `(A, B)` or `case class` |
| `List[str]` | `List[String]` |
| `Dict[str, Any]` | `Map[String, Any]` |

```scala
// Python: [t for t in tokens if t.value != ""]
// Scala:
tokens.filter(_.value.nonEmpty)

// Python: [f(x) for x in xs]
// Scala:
xs.map(f)

// Python: sum(len(t.value) for t in tokens)
// Scala:
tokens.map(_.value.length).sum
```

## Companion Objects (replacing Python class methods / static methods)
```scala
// Python @classmethod or @staticmethod
class Token:
    @staticmethod
    def from_string(s: str) -> Token: ...

// Scala companion object
case class Token(value: String, tokenType: TokenType)
object Token {
  def fromString(s: String): Token = ...
}
```

## Pattern Matching (replaces isinstance / match)
```scala
// Python
if isinstance(x, StringTokenizer): ...
elif isinstance(x, NumericTokenizer): ...

// Scala
x match {
  case _: StringTokenizer  => ...
  case _: NumericTokenizer => ...
}

// On sealed traits
tokenType match {
  case TokenType.String  => ...
  case TokenType.Numeric => ...
}
```

## Default Parameters and Named Arguments
```scala
// Python
def tokenize(text: str, lower: bool = True) -> List[Token]: ...
tokenize("Hello", lower=False)

// Scala
def tokenize(text: String, lower: Boolean = true): List[Token] = ...
tokenize("Hello", lower = false)
```