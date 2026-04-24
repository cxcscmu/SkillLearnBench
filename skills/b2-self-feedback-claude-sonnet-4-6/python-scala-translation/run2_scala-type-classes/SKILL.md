---
name: run2_scala-type-classes
description: Translating Python Protocol, ABC, and isinstance dispatch to Scala traits, overloaded methods, and functor/monad abstractions.
---

# Scala Traits, Overloading, and Functors (vs Python Protocol/ABC/isinstance)

## Python Protocol → Scala Trait

Python structural typing (duck typing):
```python
@runtime_checkable
class Tokenizable(Protocol):
    def to_token(self) -> str: ...
```

Scala uses **nominal typing** — classes must explicitly declare `extends Tokenizable`:
```scala
trait Tokenizable {
  def toToken: String
}
```

- No `@runtime_checkable` — Scala trait membership is checked at compile time
- Method name convention: `toToken` (camelCase) not `to_token`

## Python ABC → Scala Abstract Class

```python
class BaseTokenizer(ABC, Generic[T]):
    @abstractmethod
    def tokenize(self, value: T) -> Token: ...
    def tokenize_batch(self, values: Iterable[T]) -> Iterator[Token]:
        for v in values: yield self.tokenize(v)
```

```scala
abstract class BaseTokenizer[T] {
  def tokenize(value: T): Token                          // abstract (no body)
  def tokenizeBatch(values: Iterable[T]): Iterator[Token] =
    values.iterator.map(tokenize)                        // concrete default
}
```

- Methods without body are abstract — no `@abstractmethod` annotation needed
- `values.iterator.map(tokenize)` is lazy — same semantics as Python generator

## Python isinstance Dispatch → Scala Method Overloading

Python runtime dispatch with type checks:
```python
def tokenize(self, value: Any) -> Token:
    if value is None: return Token("NULL", TokenType.NULL)
    if isinstance(value, (str, bytes)): return self._string_tokenizer.tokenize(value)
    if isinstance(value, (int, float, Decimal)): return self._numeric_tokenizer.tokenize(value)
    if isinstance(value, (datetime, date)): return self._temporal_tokenizer.tokenize(value)
```

Scala compile-time overloading:
```scala
final class UniversalTokenizer {
  private val stringTokenizer   = new StringTokenizer()
  private val numericTokenizer  = new NumericTokenizer()
  private val temporalTokenizer = new TemporalTokenizer()

  def tokenize(value: String):        Token = stringTokenizer.tokenize(value)
  def tokenize(value: Array[Byte]):   Token = stringTokenizer.tokenizeBytes(value)
  def tokenize(value: Int):           Token = numericTokenizer.tokenizeInt(value)
  def tokenize(value: Double):        Token = numericTokenizer.tokenizeDouble(value)
  def tokenize(value: BigDecimal):    Token = numericTokenizer.tokenize(value)
  def tokenize(value: LocalDateTime): Token = temporalTokenizer.tokenize(value)
  def tokenize(value: LocalDate):     Token = temporalTokenizer.tokenizeDate(value)
  def tokenize(value: Tokenizable):   Token = Token(value.toToken, TokenType.STRUCTURED)
  def tokenizeNull: Token = Token("NULL", TokenType.NULL)   // null has no value in Scala
}
```

- Each overload is resolved at compile time — no runtime overhead
- `None` → `tokenizeNull` (separate method, since Scala `null` is not a type)

## TokenFunctor and TokenMonad

```scala
class TokenFunctor[T](private val _value: T) {
  def get: T = _value
  def map[B](f: T => B): TokenFunctor[B]           = new TokenFunctor(f(_value))
  def flatMap[B](f: T => TokenFunctor[B]): TokenFunctor[B] = f(_value)
  def getOrElse[B >: T](default: => B): B = Option(_value).getOrElse(default)
}
```

Key improvements over Python:
- `map` and `flatMap` are properly typed with `B` — not `Any`
- `get` is the primary value accessor
- `getOrElse` uses call-by-name `default` — only evaluated if needed
- `[B >: T]` lower bound in `getOrElse` preserves type safety

```scala
class TokenMonad[T](value: T) extends TokenFunctor[T](value) {
  def ap[B](funcWrapped: TokenMonad[T => B]): TokenMonad[B] =
    new TokenMonad(funcWrapped.get(get))
}

object TokenMonad {
  def pure[T](value: T): TokenMonad[T] = new TokenMonad(value)
}
```

- `pure` lives in companion object — replaces Python `@classmethod`
- `ap` properly typed: accepts `TokenMonad[T => B]`, returns `TokenMonad[B]`

## TokenRegistry: Handler Pipeline

Python `for/else` semantics (first successful handler wins):
```python
for handler in self._handlers:
    result = handler(item)
    if result is not None:
        results.append(result); break
else:
    results.append(None)
```

Scala with lazy iterator short-circuit:
```scala
handlers.iterator.flatMap(h => h(item)).nextOption()
```

- `h(item)` returns `Option[Token]`
- `flatMap` on `Iterator[Option[Token]]` flattens to `Iterator[Token]`, skipping `None`
- `.nextOption()` takes only the first result — lazy, so remaining handlers NOT evaluated
- Returns `Option[Token]` — `None` if all handlers returned `None`
