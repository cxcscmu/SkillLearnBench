---
name: scala-circe-json
description: How to use circe for JSON processing in Scala. Use this skill whenever translating Python json operations to Scala or working with circe libraries.
---
# Scala Circe JSON

When translating Python's `json` module to Scala, use `io.circe` when requested or working with Json data structures.

## Parsing JSON
- Parse JSON string: `io.circe.parser.parse(string)` returns `Either[ParsingFailure, Json]`.
- Extract value safely: `parse(string).getOrElse(Json.Null)`.

## Generating JSON Strings
- Compact string output: `json.noSpaces`.
- Pretty printed output (indented): `json.spaces2`.

## Navigating JSON
- Objects: `json.asObject` returns `Option[JsonObject]`.
- Arrays: `json.asArray` returns `Option[Vector[Json]]`.
- Access object properties: `jsonObject(key)` or `jsonObject.toMap.get(key)`.
- Access array elements: `jsonArray.lift(index)`.
