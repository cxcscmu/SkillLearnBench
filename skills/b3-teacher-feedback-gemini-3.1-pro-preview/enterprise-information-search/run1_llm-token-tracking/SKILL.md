---
name: llm-token-tracking
description: Extracts and tracks the consumed token usage from an LLM API response to monitor API cost and utilization.
---

When querying a Large Language Model (LLM) such as OpenAI, you often need to log the consumed tokens for the request and response. Standard LLM APIs return a `usage` object in their response payload containing this information.

```python
# Example of making a request and tracking token usage (OpenAI API structure)
def get_answer_and_tokens(client, prompt, context):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the text answer
    answer_text = response.choices[0].message.content
    
    # Extract total consumed tokens as a positive integer
    consumed_tokens = response.usage.total_tokens
    
    return answer_text, consumed_tokens
```