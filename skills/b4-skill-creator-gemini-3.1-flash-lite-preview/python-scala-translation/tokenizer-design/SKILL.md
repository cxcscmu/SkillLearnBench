name: tokenizer-design
description: Design principles for Scala-based tokenization systems. Use this skill when designing or implementing tokenization logic in Scala, particularly when porting from Python-based designs. Covers immutable structures, type-safe hierarchies, and monad/functor patterns for data transformation.
---

## Scala Tokenization Principles

- **Immutability First**: Represent all data structures (Tokens, Batches) as immutable case classes.
- **Type Safety**: Use Scala's type system (sealed traits, ADTs) instead of Python's dynamic `Union` and duck typing.
- **Functional Composition**: Use `map`, `flatMap`, and `for` comprehensions for transformations instead of procedural loops.
- **Error Handling**: Use `Option`, `Either`, or `Try` for fallible operations instead of raising exceptions or returning `None`.
- **Type Classes**: Replace Python's `Protocol` and `Generic` constraints with Scala type classes (traits with context bounds).
- **Builder Pattern**: Utilize Scala's constructor overloading or implicit parameter lists for flexible configuration instead of mutable builders.
