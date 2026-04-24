---
name: python-scala-data-structures-mapping
description: Guidelines for translating Python dataclasses, enums, and collections to Scala.
---

# Python to Scala Data Structures

## Dataclasses to Case Classes
- Python `@dataclass(frozen=True)` -> Scala `case class`.
- Python `field(default_factory=dict)` -> Scala default argument `metadata: Map[String, Any] = Map.empty`.

## Enums
- Python `Enum` -> Scala `sealed trait` with `case object`s or `Enumeration`.
- For string values, a `sealed trait` with a `value` property is idiomatic.

## Collections
- Python `list` -> Scala `List` or `Vector`.
- Python `dict` -> Scala `Map`.
- Python `tuple` -> Scala `Tuple` or `Vector` (if variable length).
- Python `Sequence` -> Scala `Seq`.
- Python `Iterable` -> Scala `Iterable`.
- Python `Iterator` -> Scala `Iterator`.
