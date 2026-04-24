---
name: scala-fluent-builder-pattern
description: Implement a fluent Builder pattern in Scala to provide a clean API for object configuration and instantiation.
---

### Fluent Builder Implementation
The `TokenizerBuilder` should provide a functional and fluent interface. 
1. **State Management:** The builder can maintain an internal state using a `private var` (encapsulated) or by returning a new version of the builder case class with updated fields.
2. **Method Chaining:** Ensure methods return `this.type` (for mutable builders) or a new instance of the builder (for immutable builders). This allows the user to chain calls like `.withType(...).withModel(...)`.
3. **The Build Method:** Provide a `build()` method that validates the current state and instantiates the appropriate `BaseTokenizer` implementation.

### Pattern Structure
```scala
class TokenizerBuilder {
  private var tokenizerType: String = _
  
  def setType(t: String): this.type = {
    this.tokenizerType = t
    this
  }
  
  def build(): BaseTokenizer = {
    // Logic to return specific implementation based on tokenizerType
  }
}
```
This pattern provides a clear, type-safe API for constructing complex objects while hiding the instantiation logic of the specific tokenizer subclasses.