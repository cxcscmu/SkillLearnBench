---
name: python-scala-functional
description: Guide for translating Python functional patterns (map, flatMap, Option, monads) to idiomatic Scala.
---

# Python to Scala Functional Patterns

## Functor / Monad Simulation -> Proper Scala Types
```scala
// Python simulates functors; Scala has them natively via map/flatMap
class TokenFunctor[A](val get: A) {
  def map[B](f: A => B): TokenFunctor[B] = new TokenFunctor(f(get))
  def flatMap[B](f: A => TokenFunctor[B]): TokenFunctor[B] = f(get)
  def getOrElse(default: => A): A = if (get != null) get else default
}
```

## Option Handling
```scala
// Python: return None -> Scala: Option[T]
// Python: if x is None -> Scala: x match { case None => ... case Some(v) => ... }
// Python: x or default -> Scala: x.getOrElse(default)
```

## Higher-Order Functions
```scala
// Python: Callable[[T], Token] -> Scala: T => Token
// Python: Callable[[T], Token | None] -> Scala: T => Option[Token]
```

## Lazy Evaluation
```scala
// Python: yield (generator) -> Scala: Iterator via .iterator.map
def tokenizeBatch(values: Iterable[T]): Iterator[Token] =
  values.iterator.map(tokenize)
```
