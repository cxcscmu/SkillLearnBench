---
name: scala-higher-kinded-types
description: Translating Python simulated Functors and Monads to Scala Higher-Kinded Types. Use this skill whenever implementing functional programming concepts like Functor, Monad, Applicative in Scala.
---
# Scala Higher-Kinded Types

In Python, HKTs are simulated because Python's type system lacks them. In Scala, you can express them directly, but sometimes a simple generic class is sufficient depending on the spec.

## Functor Example
A `TokenFunctor[T]` can be a generic class with map operations:

```scala
class TokenFunctor[T](val value: T) {
  def map[U](f: T => U): TokenFunctor[U] = new TokenFunctor(f(value))
  def flatMap[U](f: T => TokenFunctor[U]): TokenFunctor[U] = f(value)
  def getOrElse[U >: T](default: => U): U = if (value != null) value else default
  def get: T = value
}
```

## Applicative/Monad Apply
For an Applicative's `ap` method (in a `TokenMonad` subclass):
```scala
class TokenMonad[T](value: T) extends TokenFunctor[T](value) {
  def ap[U](funcWrapped: TokenMonad[T => U]): TokenMonad[U] = 
    new TokenMonad(funcWrapped.value(this.value))
}
object TokenMonad {
  def pure[T](value: T): TokenMonad[T] = new TokenMonad(value)
}
```
