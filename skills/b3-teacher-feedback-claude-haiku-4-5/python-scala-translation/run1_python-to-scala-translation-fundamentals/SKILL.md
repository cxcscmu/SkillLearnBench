---
name: python-to-scala-translation-fundamentals
description: Core principles for translating Python code to idiomatic Scala, including paradigm shifts from procedural/OOP to functional programming, type system differences, and structural refactoring strategies.
---

## Key Translation Principles

### 1. Paradigm Shift
- **Python**: Primarily imperative/OOP with optional functional features
- **Scala**: Multi-paradigm, favors immutability and functional composition
- **Translation approach**: Prefer immutable data structures, use case classes over mutable classes, leverage pattern matching and higher-order functions

### 2. Type System Differences
- Python has runtime typing; Scala has compile-time type safety
- Translate Python type hints to explicit Scala types
- Use Scala's `Option[T]` instead of Python's `None` for optional values
- Use sealed traits with case classes for sum types instead of Python's inheritance patterns

### 3. Collections and Data Structures
- Python lists → Scala `List`, `Seq`, or `Vector` (immutable by default)
- Python dicts → Scala `Map`
- Python sets → Scala `Set`
- Use appropriate collection methods from Scala stdlib rather than manual iteration

### 4. Error Handling
- Python's try/except → Scala's `try/catch` or better: `Option`, `Either`, `Try`
- Prefer composing error handling with functional constructs over imperative try/catch blocks
- Never use bare `Exception`; be specific about exception types

### 5. Class and Function Design
- Python classes with state → Scala case classes (immutable) or regular classes (when mutability necessary)
- Python `__init__` → Scala primary constructor or `apply` in companion object
- Python instance methods → Scala methods; consider if they should be pure functions
- Python module-level functions → Place in object (singleton) or as extension methods