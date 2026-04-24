---
name: run2_scala-immutable-builder
description: Implementing the builder pattern in Scala using immutable case classes or private constructors with copy.
---

# Immutable Builder Pattern in Scala

## Using Private Constructor + Companion Object
```scala
class Builder[T] private (
  normalizers: Vector[String => String],
  validators: Vector[T => Boolean],
  metadata: Map[String, Any]
) {
  def withNormalizer(f: String => String): Builder[T] =
    new Builder(normalizers :+ f, validators, metadata)

  def withMetadata(entries: (String, Any)*): Builder[T] =
    new Builder(normalizers, validators, metadata ++ entries.toMap)

  def build(): T => Result = { value =>
    validators.foreach(v => if (!v(value)) throw new IllegalArgumentException(...))
    val str = normalizers.foldLeft(value.toString)((s, f) => f(s))
    Result(str, metadata)
  }
}

object Builder {
  def apply[T](): Builder[T] = new Builder(Vector.empty, Vector.empty, Map.empty)
}
```

Key: immutable collections (`Vector`, `Map`) ensure thread safety. Each `with*` method returns a new instance.
