---
name: python-scala-functional
description: Mapping Python's functional tools to idiomatic Scala equivalents, including lambdas and collection methods.
---

# Python to Scala Functional Programming

This skill focuses on functional patterns and collection transformations.

## Lambdas and Functions

- **Python**: `lambda x: x * 2`
- **Scala**: `(x: Int) => x * 2` or `_ * 2` (placeholder syntax).

## Collection Operations

| Operation | Python | Scala |
|-----------|--------|-------|
| Map | `map(f, items)` | `items.map(f)` |
| Filter | `filter(p, items)` | `items.filter(p)` |
| Reduce | `functools.reduce(f, items)` | `items.reduce(f)` |
| For-each | `for x in items: do(x)` | `items.foreach(do)` |
| Zip | `zip(a, b)` | `a.zip(b)` |
| Sort | `sorted(items, key=...)` | `items.sortBy(...)` |

## Lazy Sequences
- **Python**: Generators (`yield`) and `Iterator`.
- **Scala**: `LazyList`, `Iterator`, or `View`.

## Higher-Order Functions
Scala supports HOFs natively.
```scala
def applyFunc(f: Int => String, x: Int): String = f(x)
```

## Pattern Matching (Instance Checks)
Instead of `isinstance`, use `match` for clean type dispatch.
```scala
value match {
  case s: String => "string"
  case i: Int    => "int"
  case _         => "unknown"
}
```
