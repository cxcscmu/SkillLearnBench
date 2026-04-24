---
name: run2_scala-variance
description: Translating Python TypeVar covariant/contravariant generics to Scala variance annotations, with concrete patterns for containers, sinks, and handlers.
---

# Scala Variance Annotations (vs Python TypeVars)

## Python TypeVar → Scala Variance

```python
T_co    = TypeVar("T_co",    covariant=True)     # +T in Scala
T_contra = TypeVar("T_contra", contravariant=True) # -T in Scala
T       = TypeVar("T")                            # T  in Scala (invariant)
```

## Variance Rules

| Annotation | Meaning              | T can appear in       | Subtyping              |
|------------|----------------------|-----------------------|------------------------|
| `+T`       | Covariant            | Output (return types) | `F[Dog] <: F[Animal]`  |
| `-T`       | Contravariant        | Input (parameters)    | `F[Animal] <: F[Dog]`  |
| `T`        | Invariant (default)  | Both                  | No subtype relation    |

## Common Variance Problem: Covariant T in Function Parameter Position

Python doesn't enforce variance rules, but Scala does at compile time:

```python
# Python allows this — T_co (covariant) used in contravariant (input) position
class TokenContainer(Generic[T_co]):
    def map_tokens(self, func: Callable[[T_co], str]) -> list[str]: ...
```

Scala compiler REJECTS:
```scala
class TokenContainer[+T] {
  def mapTokens(f: T => String): List[String]  // ERROR: covariant T in contravariant position
}
```

Scala fix — use a **lower bound**:
```scala
class TokenContainer[+T](items: Seq[T]) {
  def mapTokens[B >: T](f: B => String): List[String] = items.map(f).toList
  // B >: T: B is a supertype of T. f accepts B, and T values can be passed as B.
}
```

## Covariant Container (read-only)

```scala
final class TokenContainer[+T](items: Seq[T]) {
  private val _items: Vector[T] = items.toVector
  def getAll: Vector[T]         = _items
  def size: Int                 = _items.size
  def mapTokens[B >: T](f: B => String): List[String] = _items.map(f).toList
}
```

- `Vector[T]` is itself covariant, so returning it from `+T` class is fine.
- `getAll` returns `Vector[T]` — covariant position ✓

## Contravariant Sink (write-only)

```scala
final class TokenSink[-T] {
  private var _received: List[Any] = Nil   // List[Any] avoids variance issue in var
  def receive(item: T): Unit = _received = _received :+ (item: Any)
  def drain(): List[Any] = {
    val result = _received
    _received = Nil
    result
  }
}
```

- `List[Any]` instead of `List[T]` — a `var List[T]` with `-T` would be invalid
- `receive(item: T)` — contravariant position ✓

## Invariant Handler (read + write)

```scala
final class BivariantHandler[T](private var value: T) {
  def get: T               = value
  def set(v: T): Unit      = value = v
  def transform(f: T => T): T = { value = f(value); value }
}
```

- Both `get` (output) and `set` (input) use T → must be invariant

## Abstract Generic Tokenizer

```scala
abstract class BaseTokenizer[T] {
  def tokenize(value: T): Token                              // abstract
  def tokenizeBatch(values: Iterable[T]): Iterator[Token] = // concrete default
    values.iterator.map(tokenize)
}
```

- `Iterable[T]` is covariant, so `tokenizeBatch` works correctly.
- Concrete subclasses implement `tokenize`.

## Concrete Subclass Pattern

```scala
final class StringTokenizer(
  encoding: String = "UTF-8",
  normalizer: String => String = identity
) extends BaseTokenizer[String] {
  def tokenize(value: String): Token = Token(normalizer(value), TokenType.STRING)
  def tokenizeBytes(bytes: Array[Byte]): Token = tokenize(new String(bytes, encoding))
}
```
