---
name: scala-immutable-builder-pattern
description: Implementing the Builder pattern idiomatically in Scala using case classes and the copy method for immutability.
---

In distributed systems, objects should be immutable to prevent concurrency issues. The traditional mutable Builder pattern in Java/Python should be adapted to an immutable Builder in Scala using case classes.

**Python (Mutable):**
```python
class TokenizerBuilder:
    def __init__(self):
        self._tokenizers = []
        
    def add_tokenizer(self, tokenizer):
        self._tokenizers.append(tokenizer)
        return self
```

**Scala (Immutable):**
```scala
case class TokenizerBuilder(tokenizers: Seq[BaseTokenizer] = Seq.empty) {
  
  // Returns a new builder instance rather than mutating the current one
  def addTokenizer(tokenizer: BaseTokenizer): TokenizerBuilder = {
    this.copy(tokenizers = this.tokenizers :+ tokenizer)
  }

  def build(): UniversalTokenizer = {
    new UniversalTokenizer(tokenizers)
  }
}

// Companion object provides a clean entry point
object TokenizerBuilder {
  def apply(): TokenizerBuilder = new TokenizerBuilder()
}
```
This guarantees that the builder is thread-safe and can be safely passed across closures in a distributed data pipeline.