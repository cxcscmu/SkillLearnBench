---
name: run2_scala-json-navigation
description: Improved JSON path navigation using Circe cursors in Scala.
---

# Circe JSON Navigation

`io.circe.ACursor` provides a robust way to navigate JSON structures.

## Path Extraction
```scala
import io.circe.Json
import io.circe.syntax._

def navigatePath(json: Json, path: String): Option[Json] = {
  val parts = path.split('.')
  parts.foldLeft(Option(json.hcursor)) { (cursor, part) =>
    cursor.flatMap { c =>
      // Try treating part as object key
      val downField = c.downField(part)
      if (downField.succeeded) Some(downField)
      else {
        // Try treating part as array index
        Try(part.toInt).toOption.flatMap { idx =>
          val downN = c.downN(idx)
          if (downN.succeeded) Some(downN) else None
        }
      }
    }
  }.flatMap(_.focus)
}
```

## JSON Tokenization
- Use `noSpaces` for compact token.
- Use `spaces2` for pretty token.
- Circe natively handles recursive `Json` objects.
