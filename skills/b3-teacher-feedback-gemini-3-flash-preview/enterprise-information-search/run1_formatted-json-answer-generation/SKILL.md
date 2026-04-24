---
name: formatted-json-answer-generation
description: Generating a JSON output file with specific requirements for list-based answers and numeric token counts.
---

The output must be a JSON dictionary stored at `/root/answer.json`. Every answer must be a list, even if it contains only one item.

1. **Structure Construction**:
   - Ensure the key matches the question ID (e.g., "q1").
   - Wrap the result in a list: `{"answer": ["Result"]}`.
   - If multiple results are found, extend the list: `{"answer": ["Result1", "Result2"]}`.
2. **Token Logging**:
   - Capture the token count from the LLM response metadata.
   - Ensure the value is a positive integer/float (not a string).
3. **Serialization**:
   ```python
   import json
   output_data = {
       "q1": {"answer": ["Apple", "Banana"], "tokens": 45},
       "q2": {"answer": ["OnlyOneItem"], "tokens": 30}
   }
   with open('/root/answer.json', 'w') as f:
       json.dump(output_data, f, indent=4)
   ```