name: answer-formatting
description: Formatting the final answer in the requested JSON structure and calculating/estimating token usage. Use this skill when you're ready to produce the final output.

# Answer Formatting

This skill provides guidelines for producing a well-structured JSON answer with accurate token estimation.

## JSON Structure

The output must follow this format:
```json
{
    "q1": {"answer": ["xxx"], "tokens": 123}, 
    "q2": {"answer": ["xxx"], "tokens": 123}, 
    "q3": {"answer": ["xxx"], "tokens": 123}
}
```

## Answer Requirements

- **Lists**: Every answer must be a list of strings (e.g., `["E123", "E456"]`).
- **Single Values**: If there's only one value, it should still be in a list with length 1 (e.g., `["E123"]`).
- **Completeness**: Include all relevant names, items, or IDs as requested in the question.

## Token Estimation

- Estimate tokens based on the complexity of the query and the number of tool calls and tokens used in each call.
- Provide a positive numeric value for `tokens`.
- Make sure to sum up the tokens from all research and retrieval steps for each question.
