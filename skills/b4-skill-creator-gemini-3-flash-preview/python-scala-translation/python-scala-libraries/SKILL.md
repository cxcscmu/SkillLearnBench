---
name: python-scala-external-libraries
description: Guidelines for mapping Python standard libraries (json, datetime) to Scala equivalents (Circe, java.time).
---

# Python to Scala External Libraries

## JSON
- Python `json` -> Scala `io.circe`.
- `JsonValue` recursive type -> `io.circe.Json`.

## Date and Time
- Python `datetime.datetime` -> `java.time.LocalDateTime`.
- Python `datetime.date` -> `java.time.LocalDate`.
- Python `strftime` -> `java.time.format.DateTimeFormatter`.

## Numeric
- Python `decimal.Decimal` -> `BigDecimal`.
- Python `float` -> `Double`.
- Python `int` -> `Int` or `Long`.
