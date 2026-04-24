---
name: scala-generics
description: Translating Python generic types, variance, and type bounds to Scala 2.13
---

# Scala Generics and Type System for Python Developers

## Core Concepts

### Variance (Key Difference from Python)

Python has no explicit variance system. Scala requires explicit declarations:

**Covariance (+T)** - "out" position, can return subtypes:
```scala
class Container[+T](items: Seq[T]) {
  def get: T = items.head  // OK - returning subtype
  // def set(t: T): Unit   // ERROR - would be contravariant
}
```

**Contravariance (-T)** - "in" position, can accept supertypes:
```scala
class Consumer[-T] {
  def consume(t: T): Unit  // OK - accepting supertype
  // def produce: T         // ERROR - would be covariant
}
```

**Invariance (T)** - exact type, no variance:
```scala
class Handler[T] {
  def get: T
  def set(t: T): Unit  // Both OK - invariant
}
```

### Translation Pattern

| Python | Scala | Notes |
|--------|-------|-------|
| `TypeVar("T")` | `[T]` | Invariant by default |
| `TypeVar("T_co", covariant=True)` | `[+T]` | Covariant, out-position only |
| `TypeVar("T_contra", contravariant=True)` | `[-T]` | Contravariant, in-position only |
| `TypeVar("T", int, float)` | `[T <: Int \| Float]` | Upper bound (Scala 3) or sealed trait |
| `Generic[T]` | `[T]` | Class definition |
| `Union[A, B]` | `A \| B` (Scala 3) or sealed trait | Use sealed traits for compatibility |

### Type Bounds

```scala
// Upper bound - T must be subtype of Ordered
class Comparable[T <: Ordered[T]]

// Lower bound - T must be supertype of String
class Container[T >: String]

// Context bound (implicit evidence)
class Serializable[T: Format]
```

### Higher-Kinded Types (Scala's advantage)

Python's `TypeVar("F")` for type constructors cannot express true HKTs.
Scala can use type lambdas:

```scala
// Scala 2.13 with kind-projector
type Functor[F[_]] = {
  def map[A, B](fa: F[A], f: A => B): F[B]
}

// Or in Scala 3
def map[F[_], A, B](fa: F[A], f: A => B): F[B]
```

## Translation Examples

### Generic Container (Python)
```python
class TokenContainer(Generic[T_co]):
    def __init__(self, items: Sequence[T_co]) -> None:
        self._items: tuple[T_co, ...] = tuple(items)

    def get_all(self) -> tuple[T_co, ...]:
        return self._items
```

### Generic Container (Scala 2.13)
```scala
class TokenContainer[+T](items: Seq[T]) {
  private val _items: Vector[T] = items.toVector

  def getAll: Vector[T] = _items
  def size: Int = _items.size
}
```

## Collections Generics

Python uses `Sequence[T]`, `Iterable[T]`, etc. Scala equivalents:

| Python | Scala |
|--------|-------|
| `Sequence[T]` | `Seq[T]` (immutable) |
| `Iterable[T]` | `Iterable[T]` |
| `Iterator[T]` | `Iterator[T]` |
| `list[T]` | `scala.collection.mutable.ListBuffer[T]` or `List[T]` (immutable) |
| `tuple[T, ...]` | `Vector[T]` or `(T, T, ...)` for fixed size |
| `dict[K, V]` | `Map[K, V]` |

## Best Practices for Scala 2.13

1. **Prefer immutable by default** - use `Vector`, `List`, `Map`
2. **Generics in method position** - use `[T]` not just at class level
3. **Variance where appropriate** - adds flexibility but keep simple
4. **Use sealed traits for union types** - more powerful than Python's Union
5. **Type classes for ad-hoc polymorphism** - replaces duck typing

## Working with Circe JSON Types

Circe provides `Json` type which is immutable and generic:

```scala
import io.circe._

// Json is essentially: Json = JNull | JBoolean | JNumber | JString | JArray | JObject
val json: Json = Json.fromString("hello")
val jsonObj: Json = Json.obj("key" -> Json.fromString("value"))
```
