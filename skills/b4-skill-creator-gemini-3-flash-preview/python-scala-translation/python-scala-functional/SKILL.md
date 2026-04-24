---
name: python-scala-functional-idioms
description: Guidelines for translating Python functional patterns and simulations to idiomatic Scala.
---

# Python to Scala Functional Idioms

## Functions and Callables
- Python `Callable[[T], R]` -> Scala `T => R`.
- Python `Optional[T]` -> Scala `Option[T]`.

## Overloading and Dispatch
- Python `@overload` -> Scala method overloading.
- Python `isinstance` dispatch -> Scala pattern matching.

## Functors and Monads
- Python simulated Functor/Monad -> Scala's built-in `map`/`flatMap` patterns.
- Proper Scala implementation should follow the `def map[B](f: A => B): F[B]` signature.

## Builder Pattern
- Python fluent builder -> Scala class with methods returning `this.type` or new instances for immutability.
