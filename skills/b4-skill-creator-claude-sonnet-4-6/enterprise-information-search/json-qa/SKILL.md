---
name: json-qa
description: Answer questions from JSON enterprise data and write results to answer.json. Use this skill when the user asks multiple questions about enterprise data and needs answers stored in a JSON file with token counts. Handles the output format requirements for answer.json.
---

# JSON Q&A Answer Writer

## Output Format

Write answers to `/root/answer.json` with this exact structure:
```json
{
    "q1": {"answer": ["item1", "item2"], "tokens": 123},
    "q2": {"answer": ["item1"], "tokens": 456},
    "q3": {"answer": ["url1", "url2"], "tokens": 789}
}
```

## Rules
- `answer` is always a list, even if only one item
- `tokens` is a positive integer (not a string) representing tokens consumed for that question
- All question keys match the keys from the question file exactly

## Token Estimation
- Estimate tokens as: ~(input characters / 4) + ~(output characters / 4)
- For grep searches on large files, count the characters in the grep results
- Keep a running total per question

## Writing the Answer File
Use the Write tool to create `/root/answer.json` with all answers after completing all questions.
