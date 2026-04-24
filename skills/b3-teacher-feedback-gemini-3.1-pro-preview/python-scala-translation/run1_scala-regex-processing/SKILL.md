---
name: scala-regex-processing
description: Using regular expressions for text tokenization and parsing in Scala using the scala.util.matching.Regex API.
---

String manipulation and tokenization rely heavily on Regular Expressions. Scala integrates regular expressions natively through `scala.util.matching.Regex`.

### 1. Creating Regular Expressions
Scala allows defining regex securely using raw strings (`"""..."""`) and the `.r` method, avoiding the need to escape backslashes.

**Python:**
```python
import re
pattern = re.compile(r'\s+')
```

**Scala:**
```scala
val whitespacePattern = """\s+""".r
```

### 2. Matching and Splitting
**Python:**
```python
tokens = re.split(r'\s+', text)
matches = re.findall(r'\d+', text)
```

**Scala:**
```scala
// Splitting
val tokens: Array[String] = whitespacePattern.split(text)

// Finding all matches
val numberPattern = """\d+""".r
val matches: Iterator[String] = numberPattern.findAllIn(text)
val matchesList: List[String] = matches.toList
```

### 3. Pattern Matching with Regex
Scala allows using Regex as extractors in pattern matching:

```scala
val dateRegex = """(\d{4})-(\d{2})-(\d{2})""".r

text match {
  case dateRegex(year, month, day) => 
    println(s"Found date: Year $year, Month $month")
  case _ => 
    println("No date found")
}
```