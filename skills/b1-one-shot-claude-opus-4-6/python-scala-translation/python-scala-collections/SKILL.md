---
name: python-scala-collections
description: Guide for mapping Python collection types and operations to Scala equivalents.
---

# Python to Scala Collections

## Type Mappings
| Python | Scala |
|--------|-------|
| `list[T]` | `List[T]` or `mutable.ListBuffer[T]` |
| `dict[K, V]` | `Map[K, V]` or `mutable.Map[K, V]` |
| `tuple[T, ...]` | `(T, ...)` or `Vector[T]` |
| `set[T]` | `Set[T]` |
| `Sequence[T]` | `Seq[T]` |
| `Iterable[T]` | `Iterable[T]` |
| `Iterator[T]` | `Iterator[T]` |

## Mutable Collections
```scala
import scala.collection.mutable

// Python: list with append -> mutable.ListBuffer
val buf = mutable.ListBuffer.empty[Token]
buf += token

// Python: dict -> mutable.Map
val reg = mutable.Map.empty[String, TokenContainer[T]]
reg(key) = container
```

## Collection Operations
```scala
// Python: [f(x) for x in xs] -> xs.map(f)
// Python: [x for x in xs if p(x)] -> xs.filter(p)
// Python: enumerate(xs) -> xs.zipWithIndex
```
