---
name: run2_scala-numeric-precision
description: Enhanced numeric tokenization with BigDecimal and precision in Scala.
---

# Numeric Precision in Scala

Scala `BigDecimal` is robust for financial and precision calculations.

## Formatting with Precision
```scala
def formatValue(value: Any, precision: Int): String = value match {
  case d: BigDecimal => s"%.${precision}f".format(d)
  case d: Double => s"%.${precision}f".format(d)
  case d: Float => s"%.${precision}f".format(d)
  case bi: BigInt => bi.toString
  case _ => value.toString
}
```

## Scala Math Features
- `BigDecimal(str)` or `BigDecimal(double)`
- Precision can be set using `math.BigDecimal.RoundingMode` if necessary.
- In the tokenizer context, string formatting is usually sufficient.
