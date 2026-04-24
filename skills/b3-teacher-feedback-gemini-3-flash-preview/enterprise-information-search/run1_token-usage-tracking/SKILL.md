---
name: token-usage-tracking
description: Methods for calculating or retrieving the number of tokens consumed during an LLM inference task.
---

To meet the requirement of logging consumed tokens:

1. **API Metadata**: If using an external API (like OpenAI or Anthropic), retrieve `usage.total_tokens` from the response object.
2. **Local Calculation**: If using a local model or needing a manual count, use a library like `tiktoken` or the model's native tokenizer.
   ```python
   # Example for tiktoken
   import tiktoken
   encoding = tiktoken.get_encoding("cl100k_base")
   num_tokens = len(encoding.encode(text_input)) + len(encoding.encode(text_output))
   ```
3. **Validation**: Always ensure the `tokens` value in the final JSON is a numeric type (e.g., `123`) and not a string (`"123"`).