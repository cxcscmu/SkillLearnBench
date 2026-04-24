---
name: scala-circe-json
description: Guide for using Circe in Scala 2.13 for parsing and generating JSON, specifically when translating Python JSON handling.
---

# Using Circe for JSON in Scala 2.13

When converting Python's `json` module usage (e.g., `json.loads`, `json.dumps`, `JsonValue = Union[...]`), Scala relies on the Circe library. Since Scala 2.13 does not support native union types, JSON trees are best represented using the `io.circe.Json` Algebraic Data Type (ADT).

## Setup
Ensure Circe dependencies are available.
```scala
import io.circe._
import io.circe.parser._
import io.circe.syntax._
```

## Basic Operations

### Parsing JSON (like `json.loads`)
In Python:
```python
import json
data = json.loads('{"key":"value"}')
```
In Scala:
```scala
val jsonString = """{"key":"value"}"""
val jsonAst = parse(jsonString).getOrElse(Json.Null)
```

### Serializing JSON (like `json.dumps`)
In Python:
```python
json.dumps(data)
json.dumps(data, indent=2)
```
In Scala:
```scala
val compactStr = jsonAst.noSpaces
val prettyStr = jsonAst.spaces2
```

### Navigating JSON Trees
Python uses dict/list indexing:
```python
value = data.get("key")[0]
```
In Scala, use Cursors or pattern matching on `Json` methods:
```scala
val valueOption = jsonAst.hcursor.downField("key").downArray.focus
// or traversing Json values directly:
val objOption: Option[JsonObject] = jsonAst.asObject
val arrOption: Option[Vector[Json]] = jsonAst.asArray
```
