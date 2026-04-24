---
name: run2_scala-data-abstractions
description: Idiomatic data modeling with case classes, sealed traits, and exhaustive matching.
---

### Best Practices

1. **Sealed Hierarchy**: Ensure all subtypes are known at compile time for exhaustive pattern matching.
   ```scala
   sealed trait TokenValue
   case class StringValue(s: String) extends TokenValue
   ```

2. **Case Classes**: Use for data containers. They provide `equals`, `hashCode`, `copy`, and constructor-based pattern matching out of the box.

3. **Collections**: Prefer `immutable.Seq`, `Vector`, or `List` for functional transformations. Use `view` for lazy operations.
