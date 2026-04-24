---
name: read-python-tokenizer-source
description: Use this skill to understand the exact Python source code in /root/Tokenizer.py before translating to Scala. This covers every class, method, regex pattern, enum value, default value, and metadata key that must be faithfully reproduced.
---

# Reading and Understanding /root/Tokenizer.py

## Step-by-step workflow

1. **Read the file completely first**:
   ```
   cat /root/Tokenizer.py
   ```

2. **Key elements to extract and note**:
   - `TokenType` enum: all member names and their string values
   - `Token` dataclass/namedtuple: all fields, types, defaults
   - `BaseTokenizer` abstract class: interface methods
   - `StringTokenizer`: regex patterns, tokenize logic, what metadata it produces
   - `NumericTokenizer`: regex patterns (integers, floats, scientific notation), metadata keys
   - `TemporalTokenizer`: date/time regex patterns, metadata
   - `UniversalTokenizer`: how it combines other tokenizers, fallback logic
   - `WhitespaceTokenizer`: simple split logic
   - `TokenizerBuilder`: builder pattern methods, what it configures
   - Free functions: `tokenize`, `tokenizeBatch`, `toToken`, `withMetadata` — their exact signatures, parameters, defaults, return types

3. **Pay special attention to**:
   - Every regex pattern string (copy exactly)
   - Default parameter values
   - Error handling (what happens with empty strings, None, invalid input)
   - How metadata dictionaries are constructed
   - How tokenizers are chained/composed in UniversalTokenizer
   - Return types (lists, Optional values, etc.)

4. **Document the exact API surface** before writing any Scala code.