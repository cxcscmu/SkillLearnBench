---
name: run2_scala-text-processing
description: Robust text tokenization with regex and position tracking in Scala.
---

# Text Tokenization in Scala

Scala `String` methods like `split` and `replaceAll` are available.

## Regex Splitting
```scala
val words = text.split("\\s+").filter(_.nonEmpty)
```

## Position Tracking
Find positions using `indexOf`.

```scala
def tokenizeWithPos(text: String): List[(String, Int, Int)] = {
  val words = text.split("\\s+").filter(_.nonEmpty)
  var curr = 0
  words.map { w =>
    val start = text.indexOf(w, curr)
    val end = start + w.length
    curr = end
    (w, start, end)
  }.toList
}
```

## Character Sets
Scala's `Set[Char]` and `exists` for char-level operations.
Using `dropWhile` and `reverse.dropWhile` for trimming custom character sets.
