---
name: scala-functional-programming-for-data-processing
description: Functional programming patterns in Scala for data transformation, collection processing, and batch operations suitable for distributed systems.
---

## Functional Data Transformation

### Map, Filter, FlatMap
```scala
tokens.map(token => token.copy(value = token.value.toUpperCase))
tokens.filter(token => token.tokenType == StringToken)
tokens.flatMap(token => // transform to multiple elements
```

### For-Comprehensions
- Alternative to nested map/flatMap: more readable syntax
```scala
for {
  token <- tokens
  if token.value.nonEmpty
} yield token.copy(metadata = token.metadata + ("processed" -> "true"))
```

## Batch Processing Patterns

### Processing Lists of Inputs
```scala
def tokenizeBatch(inputs: List[String]): List[List[Token]] = {
  inputs.map(tokenize)
}
```

### Handling Options
```scala
Option(value).map(_.toInt).getOrElse(0)
Try { riskyOperation }.toOption
value match {
  case Some(x) => // handle
  case None => // handle
}
```

## Immutability and Copy Patterns

### Using Case Class `copy`
```scala
token.copy(metadata = token.metadata + ("key" -> "value"))
```

### Avoiding Mutable Collections
- Use immutable `List`, `Map`, `Set` from Scala stdlib
- Chain operations rather than accumulating state

## Higher-Order Functions

### Functions as Parameters
```scala
def process(tokens: List[Token], transform: Token => Token): List[Token] = {
  tokens.map(transform)
}
```

### Composition
```scala
val pipeline = tokenize _ andThen filterEmpty andThen enrichMetadata
```