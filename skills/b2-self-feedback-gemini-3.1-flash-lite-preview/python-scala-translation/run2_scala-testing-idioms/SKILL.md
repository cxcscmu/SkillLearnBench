---
name: run2_scala-testing-idioms
description: Idiomatic Scala testing patterns with ScalaTest.
---

### Standard Approach

1. **Matchers**: Use `result shouldBe expected`.
2. **Setup**: Use `BeforeAndAfterEach` for shared setup/teardown.
3. **Structure**: Keep tests close to implementations, use `package` correctly.
