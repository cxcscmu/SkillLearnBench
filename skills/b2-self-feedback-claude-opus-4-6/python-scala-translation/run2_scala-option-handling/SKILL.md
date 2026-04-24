---
name: run2_scala-option-handling
description: Handling absence and nullability in Scala using Option, with patterns for translating Python None handling.
---

# Option Handling in Scala

## Python None -> Scala Option
- `x: str | None` -> `x: Option[String]`
- `if x is None` -> `x match { case None => ... case Some(v) => ... }`
- Or use `.map`, `.flatMap`, `.getOrElse`, `.fold`

## Processing Pipelines with Option
Instead of mutable var + early returns:
```scala
// BAD (Python-like)
var w = word
if (condition) w = transform(w)
if (w.length < min) return None

// GOOD (functional Scala)
Some(word)
  .map(w => if (condition) transform(w) else w)
  .filter(_.length >= min)
  .map(w => maxLen.fold(w)(m => w.take(m)))
  .filter(_.nonEmpty)
```

## Option with Collections
- `list.flatMap(f)` where `f` returns `Option` naturally filters None
- `collectFirst` for finding first matching element
- `iterator.map(...).collectFirst { case Some(x) => x }` for lazy first-match
