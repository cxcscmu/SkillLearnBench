---
name: scala-traits-protocols
description: |
  How to convert Python Protocol classes (structural typing) to Scala traits and type classes.
  Use when translating Python's @runtime_checkable Protocol patterns to Scala's nominal typing with traits.
  Covers trait-based abstraction, implicit type classes, and structural type emulation.
---

# Scala Traits as Protocols

## Python Protocols vs Scala Traits

Python's `Protocol` allows **structural typing** (duck typing):
```python
@runtime_checkable
class Tokenizable(Protocol):
    def to_token(self) -> str: ...

# Any class with to_token() method matches, no inheritance needed
class MyClass:
    def to_token(self) -> str: return "token"

obj = MyClass()
assert isinstance(obj, Tokenizable)  # True! Runtime check
```

Scala uses **nominal typing** (explicit inheritance), but traits provide the same abstraction:

## Pattern 1: Trait-Based Abstraction (Direct Replacement)

### Python Protocol

```python
@runtime_checkable
class HasLength(Protocol):
    def __len__(self) -> int: ...

class MyContainer:
    def __len__(self) -> int: return 5

obj = MyContainer()
if isinstance(obj, HasLength):
    print(len(obj))
```

### Scala Trait

```scala
trait HasLength {
  def length: Int
}

class MyContainer extends HasLength {
  def length: Int = 5
}

val obj: HasLength = new MyContainer()
println(obj.length)
```

**Key difference**: In Scala, you explicitly declare `extends HasLength`. The trade-off is that Scala catches errors at compile-time instead of runtime.

### Generic Protocol → Generic Trait

**Python:**
```python
class TokenProcessor(Protocol[T_contra]):
    """Contravariant processor that consumes tokens."""
    def process(self, item: T_contra) -> None: ...
```

**Scala:**
```scala
trait TokenProcessor[-T] {
  def process(item: T): Unit
}

// Implementation
class StringProcessor extends TokenProcessor[String] {
  def process(item: String): Unit = println(item)
}
```

## Pattern 2: Type Classes (Advanced Protocol-like Behavior)

For true **duck typing without inheritance**, use Scala's type class pattern:

### Python (Runtime Dispatch)

```python
@runtime_checkable
class Tokenizable(Protocol):
    def to_token(self) -> str: ...

def format_tokenizable(obj: Tokenizable) -> str:
    return obj.to_token()

# Works with any object that has to_token()
class CustomObj:
    def to_token(self) -> str: return "custom"

format_tokenizable(CustomObj())  # Works!
```

### Scala Type Class (Compile-time Dispatch)

```scala
// Define the type class
trait Tokenizable[T] {
  def toToken(value: T): String
}

// Define implementations
object Tokenizable {
  implicit val stringTokenizable: Tokenizable[String] =
    new Tokenizable[String] {
      def toToken(value: String): String = value
    }

  implicit val intTokenizable: Tokenizable[Int] =
    new Tokenizable[Int] {
      def toToken(value: Int): String = value.toString
    }
}

// Use with context bounds
def formatTokenizable[T: Tokenizable](obj: T): String =
  implicitly[Tokenizable[T]].toToken(obj)

// Or using extension methods (Scala 3 style, but works in 2.13 with magnet pattern)
def formatTokenizable[T](obj: T)(implicit tokenizable: Tokenizable[T]): String =
  tokenizable.toToken(obj)

// Call it
formatTokenizable("hello")  // String instance
formatTokenizable(42)       // Int instance
```

**Advantage**: Type-safe, no reflection, extensible without modifying classes.

## Pattern 3: Simplified Trait Without Generics

### Python Protocol (Simple)

```python
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable):
    obj.draw()
```

### Scala Trait (Simple)

```scala
trait Drawable {
  def draw(): Unit
}

def render(obj: Drawable): Unit = obj.draw()

// Any class extending Drawable works
class Circle extends Drawable {
  def draw(): Unit = println("Drawing circle")
}

render(new Circle())
```

## Converting Contravariant Consumer Protocols

### Python Consumer Protocol

```python
class TokenProcessor(Protocol[T_contra]):
    """Consumes tokens of type T."""
    def process(self, item: T_contra) -> None: ...

# Can accept any supertype
def create_processor() -> TokenProcessor[Any]:
    def processor(item: Any) -> None:
        print(item)
    return processor
```

### Scala Trait with Contravariance

```scala
trait TokenProcessor[-T] {
  def process(item: T): Unit
}

def createProcessor(): TokenProcessor[Any] = new TokenProcessor[Any] {
  def process(item: Any): Unit = println(item)
}

// Can be used with subtypes due to contravariance
val stringProcessor: TokenProcessor[String] = createProcessor()
stringProcessor.process("hello")
```

## Multiple Trait Inheritance

Scala supports multiple trait inheritance naturally:

**Python (composition or ABC):**
```python
class ABC:
    pass

class Serializable(ABC):
    @abstractmethod
    def to_bytes(self) -> bytes: ...

class Drawable(ABC):
    @abstractmethod
    def draw(self) -> None: ...

class MyWidget(Serializable, Drawable):
    def to_bytes(self) -> bytes: ...
    def draw(self) -> None: ...
```

**Scala (clean mixin composition):**
```scala
trait Serializable {
  def toBytes: Array[Byte]
}

trait Drawable {
  def draw(): Unit
}

class MyWidget extends Serializable with Drawable {
  def toBytes: Array[Byte] = Array()
  def draw(): Unit = println("Drawing")
}
```

## Abstract Methods in Traits

Both Python and Scala support abstract methods:

**Python (ABC):**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

# Cannot instantiate directly
# shape = Shape()  # TypeError
```

**Scala (implicit—no decorator needed):**
```scala
trait Shape {
  def area: Double  // No implementation = abstract
}

// Cannot instantiate directly
// val shape = new Shape()  // Error: Shape is abstract

// Must extend and implement
class Circle(radius: Double) extends Shape {
  def area: Double = math.Pi * radius * radius
}
```

## Converting Optional/Default Behavior

### Python Protocol with Optional Method

```python
@runtime_checkable
class Validator(Protocol):
    def validate(self, value: Any) -> bool: ...
    def on_error(self, error: str) -> None:  # Optional in practice
        pass
```

### Scala Trait with Default Implementation

```scala
trait Validator {
  def validate(value: Any): Boolean

  def onError(error: String): Unit = {
    // Default implementation
    println(s"Validation error: $error")
  }
}

class CustomValidator extends Validator {
  def validate(value: Any): Boolean = value != null

  // Optionally override onError
  override def onError(error: String): Unit = {
    super.onError(error)
    // Custom behavior
  }
}
```

## Combining Traits with Generics

**Python Protocol with Generic:**
```python
T = TypeVar("T")

class Container(Protocol[T]):
    def get(self) -> T: ...
    def put(self, value: T) -> None: ...
```

**Scala Trait with Generic:**
```scala
trait Container[T] {
  def get: T
  def put(value: T): Unit
}

class Box[T](initialValue: T) extends Container[T] {
  private var value: T = initialValue

  def get: T = value
  def put(value: T): Unit = {
    this.value = value
  }
}
```

## Key Differences Summary

| Feature | Python Protocol | Scala Trait |
|---------|-----------------|-------------|
| Structural typing | Yes (runtime) | No (compile-time nominal) |
| Requires inheritance | No | Yes, explicit |
| Pattern matching | Limited | Excellent |
| Performance | Runtime dispatch | Compile-time dispatch |
| Variance | Limited | Full support (+T, -T) |
| Type safety | Runtime | Compile-time |

## Migration Strategy

1. **Simple protocols** → Convert to `trait` with explicit inheritance
2. **Runtime duck typing** → Use type classes with `implicit` parameters
3. **Contravariant protocols** → Use trait with `-T` variance annotation
4. **Covariant producers** → Use trait with `+T` variance annotation
5. **Complex polymorphism** → Combine traits with sealed trait hierarchies

## Practical Example: Protocol to Trait Conversion

### Python Code
```python
@runtime_checkable
class JsonSerializable(Protocol):
    def to_json(self) -> str: ...

@runtime_checkable
class JsonDeserializable(Protocol):
    @classmethod
    def from_json(cls, json_str: str) -> "JsonDeserializable": ...

def api_call(obj: JsonSerializable) -> str:
    return obj.to_json()
```

### Scala Equivalent
```scala
trait JsonSerializable {
  def toJson: String
}

trait JsonDeserializable {
  // Companion object handles factory methods
}

object JsonDeserializable {
  def fromJson[T](jsonStr: String)(implicit deserializer: JsonDeserializer[T]): T =
    deserializer.deserialize(jsonStr)
}

def apiCall(obj: JsonSerializable): String = obj.toJson
```

**Note**: Scala uses companion objects and implicit parameters instead of class methods—this is more idiomatic.
