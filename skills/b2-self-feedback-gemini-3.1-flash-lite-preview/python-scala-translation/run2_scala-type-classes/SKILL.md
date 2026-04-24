---
name: run2_scala-type-classes
description: Implementing type classes for extensible, ad-hoc polymorphism.
---

### Pattern

1. **Definition**: Define a trait `Tc[T]` that describes the behavior.
2. **Implicit Instances**: Create implicit objects/vals for each type.
3. **Implicit Parameters**: Use `(implicit tc: Tc[T])` in methods/constructors.
4. **Syntax (Extension Methods)**: Create `implicit class ...` to provide dot-syntax convenience.
