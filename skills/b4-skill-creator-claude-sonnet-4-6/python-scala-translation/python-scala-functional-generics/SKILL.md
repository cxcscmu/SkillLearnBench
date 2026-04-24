---
name: python-scala-functional-generics
description: Guide for translating Python generic containers (covariant/contravariant), functor/monad simulations, and JSON handling to idiomatic Scala. Use this skill when converting Python Generic[T_co], Generic[T_contra], TokenFunctor, TokenMonad, or json.dumps/json.loads patterns to Scala variance annotations, proper functional types, and Circe JSON.
---

# Python Generic Variance → Scala Variance Annotations

Python simulates covariance/contravariance with `TypeVar(..., covariant=True)`. Scala declares variance directly on the class.

## Covariant Container (`+T`)

```python
class TokenContainer(Generic[T_co]):  # T_co is covariant
    def __init__(self, items: Sequence[T_co]) -> None:
        self._items = tuple(items)
    def get_all(self) -> tuple[T_co, ...]: ...
    def map_tokens(self, func) -> list[str]: ...
```

```scala
class TokenContainer[+T](items: Seq[T]) {
  private val _items: Vector[T] = items.toVector

  def getAll: Vector[T]                       = _items
  def size: Int                               = _items.size
  def mapTokens(f: T => String): List[String] = _items.map(f).toList
}
```

`+T` means `TokenContainer[Dog]` is a subtype of `TokenContainer[Animal]`.

## Contravariant Sink (`-T`)

```python
class TokenSink(Generic[T_contra]):  # contravariant
    def receive(self, item: T_contra) -> None: ...
    def drain(self) -> list[Any]: ...
```

```scala
class TokenSink[-T] {
  private val _received = scala.collection.mutable.ListBuffer.empty[Any]

  def receive(item: T): Unit = _received += item

  def drain(): List[Any] = {
    val result = _received.toList
    _received.clear()
    result
  }
}
```

`-T` means `TokenSink[Animal]` is a subtype of `TokenSink[Dog]`.

## Invariant Handler

```python
class BivariantHandler(Generic[T]):  # invariant
    def get(self) -> T: ...
    def set(self, value: T) -> None: ...
    def transform(self, func) -> T: ...
```

```scala
class BivariantHandler[T](default: T) {
  private var _value: T = default

  def get: T                      = _value
  def set(value: T): Unit         = { _value = value }
  def transform(f: T => T): T     = { _value = f(_value); _value }
}
```

No variance annotation = invariant (exact type match required).

# Functor / Monad Simulation

Python's `TokenFunctor` and `TokenMonad` simulate functional type classes. In Scala, represent these as classes with `map` / `flatMap` so they integrate with `for`-comprehensions.

```python
class TokenFunctor(Generic[T]):
    def map(self, func) -> "TokenFunctor[Any]": ...
    def flat_map(self, func) -> "TokenFunctor[Any]": ...
    def get_or_else(self, default) -> T: ...
```

```scala
class TokenFunctor[T](protected val value: T) {
  def map[U](f: T => U): TokenFunctor[U]              = new TokenFunctor(f(value))
  def flatMap[U](f: T => TokenFunctor[U]): TokenFunctor[U] = f(value)
  def get: T                                           = value
  def getOrElse(default: T): T                         = if (value != null) value else default
}

class TokenMonad[T](value: T) extends TokenFunctor[T](value) {
  override def map[U](f: T => U): TokenMonad[U]       = new TokenMonad(f(value))
  def ap[U](wrapped: TokenMonad[T => U]): TokenMonad[U] = new TokenMonad(wrapped.get(value))
}

object TokenMonad {
  def pure[T](v: T): TokenMonad[T] = new TokenMonad(v)
}
```

Note: `get` (not `get_or_else` by default) is the primary accessor in Scala-style.

# JSON Handling: json module → Circe

Python uses `json.dumps` / `json.loads`. In Scala, use **Circe** (`io.circe`).

```python
import json
class JsonTokenizer:
    def tokenize(self, value: JsonValue) -> Token:
        json_str = json.dumps(value, indent=2) if self.pretty else json.dumps(value)
        return Token(json_str, TokenType.STRUCTURED, {"json": True})
```

```scala
import io.circe.Json
import io.circe.parser._

class JsonTokenizer(pretty: Boolean = false) {
  def tokenize(value: Json): Token = {
    val jsonStr = if (pretty) value.spaces2 else value.noSpaces
    Token(jsonStr, TokenType.STRUCTURED, Map("json" -> true))
  }

  def tokenizePath(value: Json, path: String): Option[Token] = {
    val parts = path.split("\\.")
    val resolved = parts.foldLeft(Option(value)) { (cur, part) =>
      cur.flatMap { json =>
        json.asObject.flatMap(_.apply(part))
          .orElse(json.asArray.flatMap { arr =>
            scala.util.Try(part.toInt).toOption
              .filter(i => i >= 0 && i < arr.size)
              .map(arr(_))
          })
      }
    }
    resolved.map(tokenize)
  }
}
```

## Circe Key Methods

| Operation             | Python                        | Circe (Scala)                     |
|-----------------------|-------------------------------|-----------------------------------|
| Serialize compact     | `json.dumps(v)`               | `v.noSpaces`                      |
| Serialize pretty      | `json.dumps(v, indent=2)`     | `v.spaces2`                       |
| Parse string          | `json.loads(s)`               | `parse(s): Either[ParsingFailure, Json]` |
| Object field access   | `d["key"]`                    | `json.asObject.flatMap(_.apply("key"))` |
| Array index access    | `lst[i]`                      | `json.asArray.map(_(i))`          |

# Registry with Handlers

```python
class TokenRegistry(Generic[T]):
    def process(self, key: str) -> list[Token | None]:
        container = self._registry.get(key)
        if container is None: return []
        results = []
        for item in container.get_all():
            for handler in self._handlers:
                result = handler(item)
                if result is not None:
                    results.append(result); break
            else:
                results.append(None)
        return results
```

```scala
class TokenRegistry[T] {
  private val registry = scala.collection.mutable.Map.empty[String, TokenContainer[T]]
  private val handlers = scala.collection.mutable.ListBuffer.empty[T => Option[Token]]

  def register(key: String, container: TokenContainer[T]): Unit =
    registry(key) = container

  def addHandler(handler: T => Option[Token]): Unit =
    handlers += handler

  def process(key: String): List[Option[Token]] =
    registry.get(key).fold(List.empty[Option[Token]]) { container =>
      container.getAll.toList.map { item =>
        handlers.view.flatMap(h => h(item)).headOption
      }
    }
}
```

`handlers.view.flatMap(h => h(item)).headOption` lazily tries each handler and returns the first `Some`.
