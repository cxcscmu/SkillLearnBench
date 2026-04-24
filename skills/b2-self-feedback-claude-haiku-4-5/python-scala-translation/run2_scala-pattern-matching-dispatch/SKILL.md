---
name: scala-pattern-matching-dispatch
description: Type-safe dispatch using Scala pattern matching for polymorphic operations
---

# Pattern Matching for Type Dispatch

## Basic Type Dispatch

Scala's pattern matching provides superior type-safe dispatch compared to Python's isinstance checks and duck typing.

```scala
def tokenize(value: Any): Token = value match {
  case s: String => tokenizeString(s)
  case i: Int => tokenizeInt(i)
  case d: Double => tokenizeDouble(d)
  case l: LocalDateTime => tokenizeDateTime(l)
  case null => Token("NULL", NULL)
  case _ => Token(value.toString, STRING, Map("fallback" -> true))
}
```

## Benefits Over Python

- **Compile-time checking**: Patterns are checked for exhaustiveness
- **Type narrowing**: Within each case, the type is narrowed (s is known to be String)
- **Guard clauses**: Add conditions with `if`

```scala
value match {
  case s: String if s.nonEmpty => processString(s)
  case s: String => Token("EMPTY", STRING)
  case _ => fallback(value)
}
```

## Instance and Constant Matching

```scala
value match {
  case null => handleNull()
  case true => handleTrue()
  case 0 => handleZero()
  case _ => handleOther()
}
```

## Collections Matching

```scala
values match {
  case Seq() => "empty"
  case Seq(single) => s"one: $single"
  case Seq(first, rest @ _*) => s"first=$first, count=${rest.length}"
  case _ => "unknown"
}
```

## Sealed Trait Matching

```scala
tokenType match {
  case STRING => "string type"
  case NUMERIC => "numeric type"
  case TEMPORAL => "temporal type"
  case STRUCTURED => "structured type"
  case BINARY => "binary type"
  case NULL => "null type"
}
```

When matching on sealed traits, the compiler enforces exhaustiveness.
