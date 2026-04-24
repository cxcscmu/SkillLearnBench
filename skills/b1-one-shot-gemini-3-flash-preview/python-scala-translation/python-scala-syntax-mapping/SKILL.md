---
name: python-scala-syntax-mapping
description: Basic syntax and type mapping from Python to Scala, including primitive types and common control structures.
---

# Python to Scala Syntax Mapping

This skill provides a quick reference for translating basic Python syntax to Scala 2.13.

## Type Mapping

| Python | Scala | Notes |
|--------|-------|-------|
| `int` | `Int` or `Long` | Use `Long` for large integers. |
| `float` | `Double` | Scala's `Double` is equivalent to Python's `float`. |
| `str` | `String` | |
| `bytes` | `Array[Byte]` | |
| `bool` | `Boolean` | |
| `None` | `null` or `None` | Use `Option[T]` (Some/None) for idiomatic Scala. |
| `list[T]` | `List[T]` or `Seq[T]` | `List` is immutable, `ArrayBuffer` is mutable. |
| `dict[K, V]` | `Map[K, V]` | `Map` is immutable, `mutable.Map` is mutable. |
| `tuple[T, ...]` | `(T, ...)` | Scala uses parentheses for tuples. |
| `Any` | `Any` | |
| `Union[A, B]` | `Either[A, B]` or Trait | Use traits for better structure. |

## Variables and Constants

- **Python**: `x = 1` (mutable/immutable by convention)
- **Scala**: `val x = 1` (immutable), `var x = 1` (mutable)

## String Formatting

- **Python**: `f"Value: {val:.2f}"`
- **Scala**: `s"Value: $val"`, `f"Value: $val%.2f"`

## Control Flow

### If-Else
- **Python**:
  ```python
  if x > 0:
      return "pos"
  else:
      return "neg"
  ```
- **Scala**:
  ```scala
  if (x > 0) "pos" else "neg" // Expressions are preferred
  ```

### For Loops
- **Python**: `for i in range(10):`
- **Scala**: `for (i <- 0 until 10) { ... }`

### List Comprehension
- **Python**: `[x * 2 for x in items if x > 0]`
- **Scala**: `items.filter(_ > 0).map(_ * 2)` or `for (x <- items if x > 0) yield x * 2`
