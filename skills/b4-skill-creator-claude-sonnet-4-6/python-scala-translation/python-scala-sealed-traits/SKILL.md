---
name: python-scala-sealed-traits
description: Guide for translating Python Enum, Protocol, and abstract class hierarchies to Scala sealed trait hierarchies. Use this skill whenever converting Python Enum classes, runtime-checkable Protocol types, abstract base classes (ABC), or Union type aliases to idiomatic Scala sealed traits, case objects, and type classes.
---

# Python Enum → Scala Sealed Trait + Case Objects

Python `Enum` with string values maps to a `sealed trait` with `case object`s in Scala. This provides exhaustive pattern matching and compile-time safety.

## Pattern

```python
# Python
class TokenType(Enum):
    STRING = "string"
    NUMERIC = "numeric"
    NULL = "null"
```

```scala
// Scala
sealed trait TokenType { val value: String }
object TokenType {
  case object STRING    extends TokenType { val value = "string"  }
  case object NUMERIC   extends TokenType { val value = "numeric" }
  case object NULL      extends TokenType { val value = "null"    }
}
```

Why sealed: the compiler enforces exhaustive `match` expressions, catching missed cases at compile time.

## Python Protocol → Scala Trait

Python's `@runtime_checkable` Protocol (structural typing) translates to a Scala `trait`. Scala uses nominal (not structural) typing by default, so explicit `extends` is required.

```python
@runtime_checkable
class Tokenizable(Protocol):
    def to_token(self) -> str: ...
```

```scala
trait Tokenizable {
  def toToken: String   // camelCase per Scala convention
}
```

Note the naming: Python uses `to_token` (snake_case); Scala uses `toToken` (camelCase).

## Python ABC → Scala Abstract Class or Trait

```python
class BaseTokenizer(ABC, Generic[T]):
    @abstractmethod
    def tokenize(self, value: T) -> Token: ...

    def tokenize_batch(self, values: Iterable[T]) -> Iterator[Token]:
        for v in values:
            yield self.tokenize(v)
```

```scala
abstract class BaseTokenizer[T] {
  def tokenize(value: T): Token   // abstract — no body

  def tokenizeBatch(values: Iterable[T]): Iterator[Token] =
    values.iterator.map(tokenize)
}
```

Use an `abstract class` (not a `trait`) when the class has constructor parameters. Use a `trait` for pure interface definitions.

## Python Union Type → Scala Overloading or Sealed Trait

Python's `Union[datetime, date]` can map to method overloading:

```scala
class TemporalTokenizer(formatStr: Option[String] = None) {
  def tokenize(value: LocalDateTime): Token = ...
  def tokenize(value: LocalDate): Token = ...
}
```

Or to a sealed trait if the union is domain-meaningful.

## Python `Optional[T]` / `T | None` → Scala `Option[T]`

```python
def tokenize_path(...) -> Token | None: ...
```

```scala
def tokenizePath(...): Option[Token] = ...
```

Always return `Option[T]` instead of nullable values. Use `Some(x)` and `None`, never `null`.

## Python TypeVar Constraints → Scala Type Bounds

```python
NumericT = TypeVar("NumericT", int, float, Decimal)
```

In Scala, union-constrained TypeVars are approximated with a common supertype or explicit overloads:

```scala
// Overloads for each numeric type:
def tokenize(value: Int): Token    = ...
def tokenize(value: Double): Token = ...
def tokenize(value: BigDecimal): Token = ...
```

## Immutable Data: `@dataclass(frozen=True)` → `case class`

```python
@dataclass(frozen=True)
class Token:
    value: str
    token_type: TokenType
    metadata: dict[str, Any] = field(default_factory=dict)
```

```scala
case class Token(
  value:     String,
  tokenType: TokenType,
  metadata:  Map[String, Any] = Map.empty
)
```

Case classes are immutable by default. `copy()` creates modified instances.

## Python `dict[str, Any]` → Scala `Map[String, Any]`

Note: `Any` in Scala is the top type (similar to Python's `Any`). Prefer narrower types where possible, but `Map[String, Any]` is acceptable for flexible metadata.
