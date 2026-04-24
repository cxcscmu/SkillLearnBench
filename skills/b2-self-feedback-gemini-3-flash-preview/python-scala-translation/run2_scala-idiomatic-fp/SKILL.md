---
name: run2_scala-idiomatic-fp
description: Refined FP patterns for Functors and Monads in Scala, including applicative.
---

# Idiomatic FP in Scala

## Functors and Monads
A proper Functor should be covariant.
A Monad should provide `pure` and `flatMap`.

```scala
class TokenFunctor[+T](val value: T) {
  def map[U](f: T => U): TokenFunctor[U] = new TokenFunctor(f(value))
}

class TokenMonad[+T](value: T) extends TokenFunctor[T](value) {
  def flatMap[U](f: T => TokenMonad[U]): TokenMonad[U] = f(value)
  
  // Applicative: apply a wrapped function to a wrapped value
  def ap[U, V](ff: TokenMonad[U => V])(implicit ev: T <:< U): TokenMonad[V] = {
    ff.flatMap(f => TokenMonad.pure(f(value)))
  }
}

object TokenMonad {
  def pure[T](v: T): TokenMonad[T] = new TokenMonad(v)
}
```

## Abstract Tokenizer with Covariance/Contravariance
```scala
trait BaseTokenizer[-T] {
  def tokenize(value: T): Token
}
```
If a tokenizer only consumes `T`, it should be contravariant in `T`.
