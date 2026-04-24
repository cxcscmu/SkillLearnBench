---
name: python-scala-oop
description: Translating Python classes, inheritance, and generic variance to Scala equivalents.
---

# Python to Scala OOP and Generics

This skill covers the translation of object-oriented concepts from Python to Scala.

## Classes and Inheritance

### Data Classes
- **Python**: `@dataclass(frozen=True)`
- **Scala**: `case class` (immutable by default, comes with `copy` and structural equality).

### Abstract Base Classes
- **Python**: `ABC` and `@abstractmethod`
- **Scala**: `abstract class` or `trait`. Use `trait` when multiple inheritance is needed.

### Methods
- **Python**: `def my_method(self, arg):`
- **Scala**: `def myMethod(arg: Type): ReturnType = { ... }`

## Enums
- **Python**: `class Color(Enum):`
- **Scala**: `object Color extends Enumeration { val Red, Green, Blue = Value }` or (better) `sealed trait Color`.

## Generics and Variance

| Python | Scala | Notes |
|--------|-------|-------|
| `Generic[T]` | `[T]` | Invariant |
| `Generic[T_co]` | `[+T]` | Covariant (can return subtypes) |
| `Generic[T_contra]` | `[-T]` | Contravariant (can accept supertypes) |

### Covariance (`+T`)
Useful for read-only containers (e.g., `List[+A]`).
```scala
class Container[+T](val item: T)
```

### Contravariance (`-T`)
Useful for consumers or sinks.
```scala
trait Sink[-T] { def consume(item: T): Unit }
```

## Structural Typing (Protocols)
- **Python**: `@runtime_checkable class Protocol:`
- **Scala**: `trait` or structural types `type MyType = { def method(): Unit }`. Usually, explicit traits are preferred.
