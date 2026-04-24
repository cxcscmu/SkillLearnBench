---
name: python-scala-circe-json
description: Using the circe library for JSON encoding, decoding, and manipulation in Scala as a replacement for Python's json module, covering the Json ADT, parsing, and path traversal.
---

# Circe JSON in Scala

## Setup (build.sbt)
```sbt
libraryDependencies ++= Seq(
  "io.circe" %% "circe-core"    % "0.14.x",
  "io.circe" %% "circe-parser"  % "0.14.x",
  "io.circe" %% "circe-generic" % "0.14.x"
)
```

## Imports
```scala
import io.circe.{Json, JsonObject}
import io.circe.parser._
import io.circe.syntax._
```

## Python json Module → Circe

### Parsing
```python
import json
data = json.loads('{"key": "value"}')
```
```scala
import io.circe.parser._
val result: Either[io.circe.ParsingFailure, Json] = parse("""{"key": "value"}""")
val json: Json = parse("""{"key": "value"}""").getOrElse(Json.Null)
```

### Serializing
```python
json.dumps(value)           # compact
json.dumps(value, indent=2) # pretty
```
```scala
json.noSpaces   // compact
json.spaces2    // pretty-printed (2-space indent)
json.spaces4    // pretty-printed (4-space indent)
```

## Circe Json ADT
```scala
Json.Null             // null
Json.True / Json.False // booleans
Json.fromString("hi") // string
Json.fromInt(42)      // number
Json.fromDouble(3.14) // number
Json.arr(j1, j2)      // array
Json.obj("k" -> v)    // object
```

## Accessing Values (Safe Traversal)
```scala
val json: Json = ...

// Object field
json.asObject.flatMap(_.apply("key"))  // Option[Json]

// Array element
json.asArray.flatMap(_.lift(0))        // Option[Json]

// Type extraction
json.asString   // Option[String]
json.asNumber   // Option[JsonNumber]
json.asBoolean  // Option[Boolean]
json.asArray    // Option[Vector[Json]]
json.asObject   // Option[JsonObject]
```

## Path Traversal (Recursive)
```scala
def traversePath(json: Json, path: String): Option[Json] = {
  path.split("\\.").foldLeft(Option(json)) { (current, part) =>
    current.flatMap { j =>
      j.asObject.flatMap(_.apply(part))
        .orElse(
          j.asArray.flatMap { arr =>
            scala.util.Try(part.toInt).toOption
              .flatMap(idx => if (idx >= 0 && idx < arr.length) Some(arr(idx)) else None)
          }
        )
    }
  }
}
```

## Replacing Python json.dumps with Circe
```python
json.dumps(value)           # → value.noSpaces
json.dumps(value, indent=2) # → value.spaces2
```

## Metadata with Boolean Values
Since `Map[String, Any]` is used for metadata, `Boolean` fits naturally:
```scala
Map("json" -> true)  // Map[String, Any] — Boolean is subtype of Any
```
