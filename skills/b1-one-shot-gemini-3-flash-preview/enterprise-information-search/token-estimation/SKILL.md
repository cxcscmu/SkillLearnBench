---
name: token-estimation
description: Skill to estimate the number of consumed tokens for the task.
---

# Token Estimation Skill

This skill provides a way to estimate token usage for a task in the absence of a direct token counting tool.

## Estimation Formulas
1. **By Characters**: `num_characters / 4` is a common estimate for English text.
2. **By Words**: `num_words / 0.75` is another standard approximation.

## Application
- For each question answered, calculate the estimated tokens based on the length of the research and the response.
- If the task involves processing many files, add a baseline for the tool outputs processed.
- The user requires `tokens` as a positive numeric value in the final JSON.

## Example
If an answer contains 100 characters, the estimated tokens would be `100 / 4 = 25`.
If you read 1000 characters to find the answer, the total consumed tokens could be estimated as `(1000 + 100) / 4 = 275`.
