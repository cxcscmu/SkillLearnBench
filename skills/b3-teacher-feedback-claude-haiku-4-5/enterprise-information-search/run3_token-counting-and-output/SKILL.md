---
name: token-counting-and-output
description: Count tokens consumed during data retrieval operations, validate numeric format, and write results to /root/answer.json with proper structure.
---

# Token Counting and Output Skill

## Step 1: Initialize Token Counter
- Create a counter starting at 0 for each question
- Track tokens consumed by:
  - File I/O operations (reading question file, data files)
  - Data parsing and searching operations
  - Evidence extraction and traversal
  - Deduplication and formatting

## Step 2: Accumulate Tokens Per Question
For each question:
- Add tokens for artifact retrieval
- Add tokens for evidence tier extraction (Tier 1, 2, 3)
- Add tokens for multi-hop traversal (per hop)
- Store as numeric value (int or float), NOT as string

## Step 3: Validate Answer Lists
Before finalizing:
- Verify every answer is stored as a list, never a string
- If answer contains one item, list has length 1: `["item"]`
- If answer contains multiple items, all in one list: `["item1", "item2", "item3"]`
- If answer is empty, use empty list: `[]`

## Step 4: Validate Token Format
- Ensure `tokens` field is numeric type (int or float)
- Never store tokens as `"123"` (quoted string)
- Always store as `123` (unquoted number)

## Step 5: Build Output JSON Structure
```python
{
    "q1": {
        "answer": ["name1", "name2"],  # Always a list
        "tokens": 150                   # Always numeric, never string
    },
    "q2": {
        "answer": ["single_name"],      # Single item still in list
        "tokens": 200
    },
    "q3": {
        "answer": [],                   # Empty if no answer found
        "tokens": 100
    }
}
```

## Step 6: Write to File
- Write to `/root/answer.json`
- Use `json.dumps()` with proper formatting
- Ensure the file is valid JSON that can be parsed by `json.load()` in Python
- Verify file is readable and contains expected structure