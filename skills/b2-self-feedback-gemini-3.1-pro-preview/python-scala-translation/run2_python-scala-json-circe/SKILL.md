---
name: run2_python-scala-json-circe
description: Parsing and handling JSON safely in Scala using io.circe
---

# JSON Processing with Circe in Scala

In Python, JSON values are often recursive union types (e.g. `str | int | list | dict`) parsed dynamically by `json.loads`.
In Scala, recursive sum types for JSON are safely modeled using `io.circe.Json` (an Algebraic Data Type). 

## Python
```python
JsonValue = Union[str, int, float, bool, None, list["JsonValue"], dict[str, "JsonValue"]]

def tokenize(self, value: JsonValue) -> Token:
    return Token(json.dumps(value))
```

## Scala (Circe)
```scala
import io.circe.Json
import io.circe.syntax._

class JsonTokenizer(val pretty: Boolean = false) {
  def tokenize(value: Json): Token = {
    // Circe handles AST formatting out-of-the-box
    val jsonStr = if (pretty) value.spaces2 else value.noSpaces
    Token(jsonStr, TokenType.STRUCTURED, Map("json" -> true))
  }
}
```

## Safe Tree Traversal
Python often accesses elements via `value["key"]` or `value[idx]` which can raise errors.
Scala's Circe allows traversing cleanly:
```scala
def tokenizePath(value: Json, path: String): Option[Token] = {
  val parts = path.split('.')
  var current: Option[Json] = Some(value)

  for (part <- parts if current.isDefined) {
    val jsonOpt = current.get
    // Safe object access: .asObject and then .flatMap(_(part))
    current = if (jsonOpt.isObject && jsonOpt.asObject.exists(_.contains(part))) {
      jsonOpt.asObject.flatMap(_(part))
    } 
    // Safe array access: .asArray and index bounds checking
    else if (jsonOpt.isArray && part.forall(_.isDigit)) {
      val idx = part.toInt
      val arr = jsonOpt.asArray.get
      if (idx >= 0 && idx < arr.size) Some(arr(idx)) else None
    } else {
      None
    }
  }

  current.map(tokenize)
}
```

*Note: Alternatively, circe's `Cursor` or optics can be used for deep traversals, but iterating AST options is functionally equivalent to the Python behavior.*
