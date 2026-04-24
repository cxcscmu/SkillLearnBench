---
name: run2_python-scala-generics-variance
description: Translating Python generics (TypeVar covariant/contravariant) to Scala generics (+T, -T) with examples
---

# Translating Python Generics to Scala

In Python, generics with variance are defined using `TypeVar` with `covariant=True` or `contravariant=True` and passed to `Generic[T]`. 
In Scala, variance is defined at the class level using `+T` (covariant) and `-T` (contravariant).

## Python Example
```python
T_co = TypeVar('T_co', covariant=True)
class TokenContainer(Generic[T_co]):
    def __init__(self, items: Sequence[T_co]) -> None:
        self._items = tuple(items)

T_contra = TypeVar('T_contra', contravariant=True)
class TokenSink(Generic[T_contra]):
    def receive(self, item: T_contra) -> None: ...
```

## Scala Translation
```scala
class TokenContainer[+T](items: Seq[T]) {
  // We cannot use T in a contravariant position (like var, or method param) 
  // directly without lower bounds, so we typically use Vector internally.
  private val _items: Vector[T] = items.toVector
  def getAll: Vector[T] = _items
}

class TokenSink[-T] {
  private val _received = scala.collection.mutable.ListBuffer.empty[Any]
  
  // T is safely consumed (contravariant position)
  def receive(item: T): Unit = {
    _received += item
  }
}
```

## Best Practices
- **Covariant `+T`**: Best for producers, immutable collections (like `List[+A]`). You cannot have `def add(item: T)` unless you use `def add[U >: T](item: U)`.
- **Contravariant `-T`**: Best for consumers, sinks, observers. You cannot have `def get(): T` because `T` is in a covariant position.
- **Invariant `T`**: Default, use for mutable collections (like `Array[T]`) or classes that both produce and consume.
