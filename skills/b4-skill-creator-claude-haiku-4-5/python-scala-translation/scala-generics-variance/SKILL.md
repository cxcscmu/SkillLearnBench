---
name: scala-generics-variance
description: |
  How to handle type variance in Scala generics when translating from Python's flexible type system.
  Use this whenever translating Python generic types (TypeVar with covariant/contravariant bounds) to Scala.
  Covers covariance (+T), contravariance (-T), and invariance for proper type safety.
---

# Scala Generics and Variance

## Core Concepts

Scala's type system is **stricter than Python**. Python allows flexible runtime type dispatch, while Scala enforces compile-time variance constraints. When translating Python generics to Scala:

### Variance Modes in Scala

1. **Invariant (T)** - Default, exact type matching required
   - Can appear in both input (contravariant position) and output (covariant position)
   - Use for mutable containers or bidirectional types

2. **Covariant (+T)** - Subtypes allowed in output
   - Can return subtypes
   - Cannot accept as input (read-only, immutable)
   - Use for producers: `class Container[+T]`, function returns

3. **Contravariant (-T)** - Supertypes allowed in input
   - Can accept supertypes
   - Cannot return (write-only)
   - Use for consumers: `class Handler[-T]`, function parameters

## Translation Patterns

### Python TypeVar → Scala Type Parameter

**Python (flexible):**
```python
T = TypeVar("T")                    # Invariant
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
```

**Scala (strict):**
```scala
class Invariant[T]           // No annotation
class Container[+T]          // Covariant (producer)
class Handler[-T]            // Contravariant (consumer)
```

### Python Generic Class → Scala Implementation

**Python (duck typing):**
```python
class BaseTokenizer(ABC, Generic[T]):
    @abstractmethod
    def tokenize(self, value: T) -> Token:
        pass
```

**Scala (type-safe):**
```scala
abstract class BaseTokenizer[T] {
  def tokenize(value: T): Token
}
```

### Covariant Container (Read-only)

**Python:**
```python
class TokenContainer(Generic[T_co]):
    def __init__(self, items: Sequence[T_co]) -> None:
        self._items: tuple[T_co, ...] = tuple(items)

    def get_all(self) -> tuple[T_co, ...]:
        return self._items
```

**Scala (producer, covariant):**
```scala
class TokenContainer[+T](items: Seq[T]) {
  private val _items = items.toVector

  def getAll: Vector[T] = _items

  def mapTokens[S](func: T => String): List[String] =
    _items.map(func).toList
}
```

**Why `+T`**: The class only *returns* T values (covariant position), never accepts them as input.

### Contravariant Handler (Write-only)

**Python:**
```python
class TokenSink(Generic[T_contra]):
    def __init__(self) -> None:
        self._received: list[Any] = []

    def receive(self, item: T_contra) -> None:
        self._received.append(item)
```

**Scala (consumer, contravariant):**
```scala
class TokenSink[-T] {
  private var _received: List[Any] = List()

  def receive(item: T): Unit =
    _received = _received :+ item

  def drain(): List[Any] = {
    val result = _received
    _received = List()
    result
  }
}
```

**Why `-T`**: The class only *accepts* T values as input (contravariant position), never returns them typed as T.

### Invariant Bidirectional (Get and Set)

**Python:**
```python
class BivariantHandler(Generic[T]):
    def __init__(self, default: T) -> None:
        self._value: T = default

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value
```

**Scala (both input and output):**
```scala
class BivariantHandler[T](default: T) {
  private var _value: T = default

  def get: T = _value

  def set(value: T): Unit =
    _value = value

  def transform(func: T => T): T = {
    _value = func(_value)
    _value
  }
}
```

**Why invariant (no +/-)**: Method both *accepts* T (set) and *returns* T (get), so requires exact type match.

## Method Type Parameters vs Class Type Parameters

Type parameters can also appear at method level:

```scala
// Covariant class can use covariant type parameter in methods
class Container[+T](items: Seq[T]) {
  // This works: method output can depend on T
  def map[U](f: T => U): Container[U] = ???

  // This also works due to covariance bound
  def filtered[U >: T](pred: U => Boolean): Container[T] = ???
}

// Invariant class can use any method-level variance
class BivariantHandler[T](default: T) {
  def transform[U](func: T => U): U = func(_value)
}
```

## Variance Bounds (Upper/Lower Bounds)

**Python (implicit via unions and optional):**
```python
T_contra = TypeVar("T_contra", contravariant=True)
def process(item: T_contra) -> None: ...
```

**Scala (explicit):**
```scala
class Handler[-T] {
  def process(item: T): Unit = ???
}

// Method with lower bound: can accept T or any supertype
def acceptSuper[T >: MyBase](item: T): Unit = ???

// Method with upper bound: can accept T or any subtype
def acceptSub[T <: MyBase](item: T): Unit = ???
```

## Key Rules to Remember

1. **Covariant (+T)** = read-only, immutable producers
   - Return T, never accept T as input
   - Example: immutable containers, function returns

2. **Contravariant (-T)** = write-only consumers
   - Accept T, never return typed as T
   - Example: callback handlers, event listeners

3. **Invariant (no +/-)** = bidirectional, mutable
   - Both accept and return T
   - Example: mutable containers, references

4. **Default to invariant** when unsure; Scala will tell you if variance is wrong (compile-time checking!)

## Common Mistakes

❌ Don't use `+T` in mutable containers:
```scala
// WRONG: can't mutate
class MutableBag[+T] { def add(item: T) = ??? }

// RIGHT: use invariant
class MutableBag[T] { def add(item: T) = ??? }
```

❌ Don't mix variance in a single method:
```scala
// WRONG: T used in both positions
class Container[+T] { def swap(item: T) = ??? }

// RIGHT: use invariant or clarify purpose
class Container[T] { def swap(item: T): Unit = ??? }
```

✓ Use method-level type parameters for flexibility:
```scala
// OK: preserves covariance on class level
class Container[+T](items: Seq[T]) {
  def collect[U >: T](f: T => Option[U]): Seq[U] = ???
}
```
