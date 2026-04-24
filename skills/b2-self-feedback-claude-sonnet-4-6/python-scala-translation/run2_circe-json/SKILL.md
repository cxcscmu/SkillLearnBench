---
name: run2_circe-json
description: Using Circe for JSON tokenization and dot-path navigation in Scala, with the exact APIs needed to replace Python's json module and dict traversal.
---

# Circe JSON Library (replacing Python's json module)

## Setup (build.sbt)

```scala
libraryDependencies ++= Seq(
  "io.circe" %% "circe-core"    % "0.14.6",
  "io.circe" %% "circe-generic" % "0.14.6",
  "io.circe" %% "circe-parser"  % "0.14.6"
)
```

## Imports

```scala
import io.circe.Json
import io.circe.parser._   // for parse()
import io.circe.syntax._   // for .asJson (not needed for tokenizer)
```

## Serialization

Python:
```python
json.dumps(value)            # compact
json.dumps(value, indent=2)  # pretty
```

Circe:
```scala
value.noSpaces   // compact — equivalent to json.dumps(value)
value.spaces2    // 2-space indent — equivalent to json.dumps(value, indent=2)
value.spaces4    // 4-space indent
```

## Parsing

```scala
val json: Either[io.circe.Error, Json] = parse("""{"key": "value"}""")
val json: Json = parse("""{"key": "value"}""").getOrElse(Json.Null)
```

## Key Json Navigation APIs

```scala
json.asObject             // Option[JsonObject] — access if json is an object
jsonObj.apply("key")      // Option[Json] — get field by name
json.asArray              // Option[Vector[Json]] — access if json is an array
arr.lift(idx)             // Option[Json] — safe array index (None if out of bounds)
json.asString             // Option[String]
json.asNumber             // Option[JsonNumber]
json.asBoolean            // Option[Boolean]
Json.Null                 // null Json value
```

## Dot-Path Navigation (replacing Python dict/list traversal)

Python:
```python
def tokenize_path(self, value: JsonValue, path: str) -> Token | None:
    parts = path.split(".")
    current = value
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit():
            idx = int(part)
            current = current[idx] if 0 <= idx < len(current) else return None
        else:
            return None
    return self.tokenize(current)
```

Scala with Circe (functional foldLeft):
```scala
def tokenizePath(value: Json, path: String): Option[Token] = {
  val parts = path.split("\\.").toList
  val leaf  = parts.foldLeft(Option(value)) { (current, part) =>
    current.flatMap { json =>
      json.asObject.flatMap(_.apply(part))
        .orElse(
          part.toIntOption.flatMap(idx =>
            json.asArray.flatMap(arr => arr.lift(idx))
          )
        )
    }
  }
  leaf.map(tokenize)
}
```

Key idiomatic choices:
- `Option[Json]` as the accumulator — `None` propagates failures automatically
- `flatMap` chains: each step returns `None` if navigation fails, `foldLeft` propagates it
- `part.toIntOption` (Scala 2.13+) — safe string-to-int, replaces `part.isdigit()` + `int(part)`
- `arr.lift(idx)` — safe array access (None if out of bounds), replaces bounds check

## Complete JsonTokenizer

```scala
final class JsonTokenizer(pretty: Boolean = false) {

  def tokenize(value: Json): Token = {
    val jsonStr = if (pretty) value.spaces2 else value.noSpaces
    Token(jsonStr, TokenType.STRUCTURED, Map("json" -> true))
  }

  def tokenizePath(value: Json, path: String): Option[Token] = {
    val parts = path.split("\\.").toList
    parts.foldLeft(Option(value)) { (current, part) =>
      current.flatMap { json =>
        json.asObject.flatMap(_.apply(part))
          .orElse(part.toIntOption.flatMap(idx =>
            json.asArray.flatMap(_.lift(idx))
          ))
      }
    }.map(tokenize)
  }
}
```
