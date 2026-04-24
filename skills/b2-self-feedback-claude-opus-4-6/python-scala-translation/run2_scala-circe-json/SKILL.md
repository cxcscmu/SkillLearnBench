---
name: run2_scala-circe-json
description: Using circe for JSON tokenization in Scala, including printing, cursor navigation, and path-based access.
---

# Circe JSON for Tokenization

## Printing
```scala
import io.circe.{Json, Printer}

val compact = Printer.noSpaces.print(json)
val pretty = Printer.spaces2.print(json)
```

## Path-Based Navigation with ACursor
```scala
import io.circe.ACursor

def navigate(json: Json, path: String): Option[Json] = {
  val cursor = path.split("\\.").foldLeft(json.hcursor: ACursor) { (c, part) =>
    if (part.forall(_.isDigit)) c.downN(part.toInt)
    else c.downField(part)
  }
  cursor.focus
}
```

## Key Differences from Python json module
- circe uses `Json` ADT instead of Python's dynamic types
- No need for recursive `JsonValue` type alias - `Json` is already recursive
- Printing via `Printer` instances rather than `json.dumps` kwargs
