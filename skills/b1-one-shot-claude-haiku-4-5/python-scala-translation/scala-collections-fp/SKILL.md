---
name: scala-collections-fp
description: Scala collections, iterators, and functional programming patterns for Python developers
---

# Scala Collections and Functional Programming

## Collections Overview

### Immutable Collections (Preferred in Scala)

| Python | Scala | Characteristics |
|--------|-------|-----------------|
| `list[T]` | `List[T]` | Linked list, prepend fast |
| `list[T]` | `Vector[T]` | Indexed access fast, append ok |
| `tuple[T, ...]` | `Seq[T]` (umbrella type) | Immutable sequence |
| `set[T]` | `Set[T]` | Unordered, unique elements |
| `dict[K, V]` | `Map[K, V]` | Key-value pairs |
| `range(n)` | `(0 until n)` or `Range` | Lazy range |

### Mutable Collections

```scala
import scala.collection.mutable

val list = scala.collection.mutable.ListBuffer[Int]()
val set = scala.collection.mutable.Set[String]()
val map = scala.collection.mutable.Map[String, Int]()
```

## Iteration Patterns

### Python iteration
```python
# List comprehension
squares = [x * x for x in range(10)]

# Generator
def gen():
    for x in range(10):
        yield x * x

# Higher-order functions
list(map(lambda x: x * x, range(10)))
list(filter(lambda x: x > 10, range(20)))
```

### Scala equivalents
```scala
// Collection methods (eager)
val squares = (0 until 10).map(x => x * x).toList

// Iterator (lazy)
def gen: Iterator[Int] = (0 until 10).iterator.map(x => x * x)

// For-comprehension (syntactic sugar)
val squares = for (x <- 0 until 10) yield x * x

// Higher-order functions
List(1, 2, 3).map(_ * 2)    // List(2, 4, 6)
List(1, 2, 3, 4).filter(_ > 2)  // List(3, 4)
```

## Iterator Pattern

Iterators are lazy and consume memory efficiently:

### Python Generator
```python
def tokenize_batch(self, values: Iterable[T]) -> Iterator[Token]:
    for v in values:
        yield self.tokenize(v)

# Usage
for token in tokenizer.tokenize_batch(large_list):
    process(token)  # Lazy - doesn't compute all at once
```

### Scala Iterator
```scala
def tokenizeBatch(values: Iterable[T]): Iterator[Token] =
  values.toIterator.map(tokenize)

// Usage
tokenizer.tokenizeBatch(largeList).foreach(token => process(token))

// Or with Iterator directly
def tokenizeBatch(values: Iterator[T]): Iterator[Token] =
  values.map(tokenize)
```

## Map and FlatMap

FlatMap is essential in Scala - combines map + flatten.

### Python equivalent
```python
# Map
nums = [1, 2, 3]
squared = [x * x for x in nums]  # [1, 4, 9]

# FlatMap-like behavior
lists = [[1, 2], [3, 4], [5, 6]]
flattened = [x for sublist in lists for x in sublist]  # [1,2,3,4,5,6]

# Function that returns list
def duplicate(x):
    return [x, x]

result = [y for x in nums for y in duplicate(x)]  # [1,1,2,2,3,3]
```

### Scala equivalent
```scala
// Map
val nums = List(1, 2, 3)
val squared = nums.map(x => x * x)  // List(1, 4, 9)

// FlatMap
val lists = List(List(1, 2), List(3, 4), List(5, 6))
val flattened = lists.flatMap(identity)  // List(1,2,3,4,5,6)

// Function that returns List
def duplicate(x: Int): List[Int] = List(x, x)
val result = nums.flatMap(duplicate)  // List(1,1,2,2,3,3)
```

## Fold/Reduce

Used for aggregations (Python: reduce, sum, etc.)

### Python patterns
```python
# Sum/reduce
total = sum([1, 2, 3, 4])  # 10

# Reduce
from functools import reduce
product = reduce(lambda a, b: a * b, [1, 2, 3, 4])  # 24

# Manual loop
result = 0
for x in [1, 2, 3, 4]:
    result += x * 2
```

### Scala patterns
```scala
// Sum (built-in)
val total = List(1, 2, 3, 4).sum  // 10

// Fold (left fold - left to right)
val product = List(1, 2, 3, 4).fold(1)((a, b) => a * b)  // 24
val product = List(1, 2, 3, 4).foldLeft(1)(_ * _)  // 24

// Or reduce (like Python's reduce, needs non-empty)
val product = List(1, 2, 3, 4).reduce(_ * _)  // 24

// Complex aggregation
val result = List(1, 2, 3, 4).foldLeft(0)((acc, x) => acc + x * 2)  // 20
```

## Grouping and Sorting

### Python grouping
```python
from itertools import groupby

data = [("a", 1), ("a", 2), ("b", 3), ("b", 4)]
grouped = {k: list(g) for k, g in groupby(data, key=lambda x: x[0])}

# Sorting
sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
```

### Scala grouping
```scala
val data = List(("a", 1), ("a", 2), ("b", 3), ("b", 4))
val grouped = data.groupBy(_._1)  // Map("a" -> List(...), "b" -> List(...))

// Sorting
val sortedData = data.sortBy(_._2)(Ordering.Int.reverse)
// Or
val sortedData = data.sortWith((a, b) => a._2 > b._2)
```

## Collecting/Pattern Matching on Collections

Scala's `collect` is like Python's list comprehension with filtering:

```scala
val nums = List(1, 2, 3, 4, 5)

// collect with partial function
val evens = nums.collect { case x if x % 2 == 0 => x }  // List(2, 4)

// Instead of: nums.filter(_ % 2 == 0)

// With transformation
val doubled = nums.collect { case x if x > 2 => x * 2 }  // List(6, 8, 10)
```

## Lazy Evaluation

Unlike Python, Scala collections are eager by default, but you can use Views:

```scala
// Eager - creates all intermediate collections
val result = (1 to 1000000)
  .map(_ * 2)
  .filter(_ > 100)
  .take(5)  // Still computes all 1M values!

// Lazy - View delays computation until forced
val result = (1 to 1000000)
  .view
  .map(_ * 2)
  .filter(_ > 100)
  .take(5)
  .toList  // Only computes what's needed!
```

## Key Differences from Python

1. **Scala collections are immutable by default** - use `scala.collection.mutable.*` for mutable
2. **Methods return new collections** - doesn't modify in place
3. **`.toList`, `.toVector`, `.toSet`** - explicitly convert between types
4. **No negative indexing** - use `lastOption` or `reverse.head`
5. **Range is lazy** - `(1 to 1000000)` doesn't create a million-element list
6. **`for` comprehension** - more powerful than Python's list comprehension

## Common Patterns in Tokenizer Context

### Building lists
```scala
// Python
tokens = []
for word in words:
    tokens.append(Token(word, ...))

// Scala - functional
val tokens = words.map(word => Token(word, ...))

// Scala - mutable accumulation (if really needed)
val tokens = scala.collection.mutable.ListBuffer[Token]()
for (word <- words) {
  tokens += Token(word, ...)
}
val result = tokens.toList
```

### Processing with metadata tracking
```scala
// Python
result = []
for i, word in enumerate(words):
    token = Token(word, ..., metadata={"position": i})
    result.append(token)

// Scala
val result = words.zipWithIndex.map { case (word, i) =>
  Token(word, TokenType.STRING, Map("position" -> i))
}
```

### Filtering and transforming
```scala
// Python
result = []
for word in words:
    processed = process(word)
    if processed is not None:
        result.append(processed)

// Scala
val result = words.flatMap { word =>
  process(word)  // Returns Option[Token]
}.toList
```
