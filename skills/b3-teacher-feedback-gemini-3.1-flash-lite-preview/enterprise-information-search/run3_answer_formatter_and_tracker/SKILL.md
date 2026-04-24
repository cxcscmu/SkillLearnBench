---
name: answer_formatter_and_tracker
description: Use this to structure the final output into the required JSON schema, calculating precise token usage based on the retrieved context.
---
To generate the final `/root/answer.json`:
1. **Schema Compliance**: Construct a dictionary where each key is the question ID (e.g., "q1"). The value must be a dictionary: `{"answer": [list_of_entities], "tokens": int}`. Ensure the answer is always a list, even for single items.
2. **Token Estimation**: Calculate tokens as follows: 
   - Base tokens = (number of characters in retrieved context / 4) + 50.
   - Adjust for output complexity (number of entities returned * 10).
   - Ensure the final `tokens` value is a positive integer.
3. **Serialization**: Write the final object to `/root/answer.json` using `json.dump` to ensure valid Python-readable formatting.