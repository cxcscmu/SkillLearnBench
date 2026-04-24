---
name: scala-circe-json
description: Working with Circe JSON library in Scala for type-safe JSON processing
---

# Scala Circe JSON Processing

## Overview

Circe is the standard type-safe JSON library in Scala. It provides:
- Immutable `Json` type
- Type-safe codecs (Encoder/Decoder)
- Cursor-based navigation (like XPath for JSON)
- Pretty printing
- Seamless case class integration

## Installation

Add to `build.sbt`:
```scala
libraryDependencies ++= Seq(
  "io.circe" %% "circe-core" % "0.14.5",
  "io.circe" %% "circe-parser" % "0.14.5",
  "io.circe" %% "circe-generic" % "0.14.5"
)
```

## Basic Usage

### Parsing JSON
```scala
import io.circe.parser._
import io.circe._

// Parse from string
val jsonString = """{"name": "Alice", "age": 30}"""
val result: Either[io.circe.ParsingFailure, Json] = parse(jsonString)

// Safe extraction
result match {
  case Right(json) => println(s"Parsed: $json")
  case Left(error) => println(s"Parse error: $error")
}

// Or with Try
val json: scala.util.Try[Json] = parse(jsonString).toTry
```

### Creating JSON
```scala
import io.circe.syntax._

// From primitives
val str = Json.fromString("hello")
val num = Json.fromInt(42)
val bool = Json.fromBoolean(true)
val null_val = Json.Null

// Object (using syntax extension)
val obj = Json.obj(
  "name" -> Json.fromString("Alice"),
  "age" -> Json.fromInt(30)
)

// Array
val arr = Json.arr(
  Json.fromInt(1),
  Json.fromInt(2),
  Json.fromInt(3)
)

// Using tuple extension (cleaner)
val obj = Json.obj(
  "name" -> "Alice".asJson,
  "age" -> 30.asJson,
  "scores" -> List(90, 85, 88).asJson
)
```

### Working with Json Type

```scala
val json = Json.obj(
  "name" -> "Alice".asJson,
  "age" -> 30.asJson
)

// Type checks
json.isObject    // true
json.isArray     // false
json.isNull      // false

// Conversions
json.asObject    // Option[JsonObject]
json.asArray     // Option[Vector[Json]]
json.asString    // Option[String]
json.asNumber    // Option[JsonNumber]
json.asBoolean   // Option[Boolean]

// Unsafe conversion (throws)
json.asObject.get
```

## Navigation with Cursors

Cursors provide safe, composable navigation (like XPath):

```scala
import io.circe.{Json, HCursor}

val json = parse("""
{
  "person": {
    "name": "Alice",
    "addresses": [
      {"city": "NYC"},
      {"city": "Boston"}
    ]
  }
}
""").getOrElse(Json.Null)

// Creating cursor
val cursor: HCursor = json.hcursor

// Navigation
val name: Either[DecodingFailure, String] =
  cursor
    .downField("person")
    .downField("name")
    .as[String]

// Navigate arrays
val firstCity: Either[DecodingFailure, String] =
  cursor
    .downField("person")
    .downField("addresses")
    .downArray
    .downField("city")
    .as[String]

// Optional navigation (returns Json)
cursor.downField("person").downField("name").focus  // Option[Json]
```

### Cursor Methods

```scala
val cursor = json.hcursor

// Navigation
cursor.downField("fieldName")   // Navigate to field
cursor.downArray                // Navigate to first array element
cursor.up                       // Go to parent
cursor.left                     // Move to previous array element
cursor.right                    // Move to next array element

// Extraction
cursor.focus                    // Option[Json] - current value
cursor.as[String]               // Either[DecodingFailure, String]

// Checking
cursor.succeeded               // Boolean - did navigation succeed?
```

## Type-Safe Encoding/Decoding

### For Case Classes

```scala
import io.circe._, io.circe.generic.semiauto._

case class Person(name: String, age: Int)

// Automatic codec generation
implicit val encoder: Encoder[Person] = deriveEncoder[Person]
implicit val decoder: Decoder[Person] = deriveDecoder[Person]

// Usage
val person = Person("Alice", 30)
val json = person.asJson
val decoded = json.as[Person]  // Either[DecodingFailure, Person]
```

### Custom Codecs

```scala
implicit val customEncoder: Encoder[Person] = new Encoder[Person] {
  def apply(p: Person): Json = Json.obj(
    "fullName" -> Json.fromString(p.name),
    "years" -> Json.fromInt(p.age)
  )
}

implicit val customDecoder: Decoder[Person] = new Decoder[Person] {
  def apply(c: HCursor): Decoder.Result[Person] = for {
    name <- c.downField("fullName").as[String]
    age <- c.downField("years").as[Int]
  } yield Person(name, age)
}
```

## Recursive JSON Structures

For recursive types like JSON itself:

```scala
// Representing JSON recursively
sealed trait JsonValue
case class JString(value: String) extends JsonValue
case class JNumber(value: Double) extends JsonValue
case class JBoolean(value: Boolean) extends JsonValue
case object JNull extends JsonValue
case class JArray(value: Vector[JsonValue]) extends JsonValue
case class JObject(value: Map[String, JsonValue]) extends JsonValue

// Or use Circe's Json type directly (which IS recursive)
val json: Json = Json.obj(
  "data" -> Json.arr(
    Json.obj("id" -> 1.asJson),
    Json.obj("id" -> 2.asJson)
  )
)
```

## Pretty Printing

```scala
import io.circe.Printer

val json = Json.obj("name" -> "Alice".asJson, "age" -> 30.asJson)

// Compact
json.toString()
// {"name":"Alice","age":30}

// Pretty printed
val printer = Printer.spaces2  // 2-space indent
println(printer.print(json))
// {
//   "name" : "Alice",
//   "age" : 30
// }

// Custom printer
val customPrinter = Printer(
  dropNullValues = false,
  indent = "  "
)
```

## JSON Path Extraction (for tokenize_path)

```scala
def getValueAtPath(json: Json, path: String): Option[Json] = {
  val parts = path.split("\\.")
  parts.foldLeft(Option(json)) { case (current, part) =>
    current.flatMap { j =>
      if (j.isObject) {
        j.hcursor.downField(part).focus
      } else if (j.isArray) {
        part.toIntOption.flatMap { idx =>
          j.asArray.flatMap(_.lift(idx))
        }
      } else {
        None
      }
    }
  }
}

// Usage
val json = parse("""{"person": {"name": "Alice", "scores": [90, 85]}}""").getOrElse(Json.Null)
val name = getValueAtPath(json, "person.name")      // Some("Alice")
val score = getValueAtPath(json, "person.scores.0") // Some(90)
val missing = getValueAtPath(json, "person.email")  // None
```

## Common Patterns for Tokenizer

### JSON Tokenization
```scala
import io.circe.Json
import io.circe.syntax._

class JsonTokenizer(pretty: Boolean = false) {
  def tokenize(json: Json): Token = {
    val jsonStr = if (pretty) {
      Printer.spaces2.print(json)
    } else {
      json.toString()
    }
    Token(jsonStr, TokenType.STRUCTURED, Map("json" -> true.asJson))
  }

  def tokenizePath(json: Json, path: String): Option[Token] = {
    getValueAtPath(json, path).map(tokenize)
  }

  private def getValueAtPath(json: Json, path: String): Option[Json] = {
    val parts = path.split("\\.")
    parts.foldLeft(Option(json)) { case (current, part) =>
      current.flatMap { j =>
        if (j.isObject) j.hcursor.downField(part).focus
        else if (j.isArray) {
          part.toIntOption.flatMap(idx => j.asArray.flatMap(_.lift(idx)))
        } else None
      }
    }
  }
}
```

## Type Safety Benefits

Unlike Python's duck typing with JSON:

```python
# Python - runtime errors possible
data = {"name": "Alice"}
age = data["age"]  # KeyError!
```

```scala
// Scala - compile-time safety
val json = parse("""{"name": "Alice"}""").getOrElse(Json.Null)
val age: Option[Int] = json.hcursor.downField("age").as[Int].toOption
// Type mismatch caught at compile time
```

## Circe vs Manual JSON Handling

```scala
// Manual approach (error-prone)
val jsonStr = s"""{"value": "$value", "type": "$tokenType"}"""

// Circe approach (safe, composable)
val token = Token(value, tokenType)
val json = token.asJson  // With derived encoders
```
