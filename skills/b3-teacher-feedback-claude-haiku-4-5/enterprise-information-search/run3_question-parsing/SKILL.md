---
name: question-parsing
description: Load and parse questions from /root/question.txt, extract question IDs and their artifact/product context. Validate that all questions are correctly mapped before proceeding to data retrieval.
---

# Question Parsing Skill

## Step 1: Load Question File
- Read `/root/question.txt` completely
- Handle any encoding issues (UTF-8)
- Preserve all question entries

## Step 2: Parse Each Question
For each line/entry in the file:
- Extract the question ID (e.g., "q1", "q2", "q3")
- Extract the question text
- Identify the **artifact/product context** mentioned in the question
- Identify the **entity type** being asked for (e.g., reviewers, contributors, participants)
- Store parsed metadata in a structured dictionary

## Step 3: Validate and Debug
- Print all parsed questions with their IDs, artifact contexts, and entity types
- Verify the total count matches expectations
- Check for any malformed entries
- Confirm key names and values are correctly extracted

## Step 4: Return Parsed Questions
Return a dictionary mapping question IDs to:
```python
{
  "question_id": "q1",
  "text": "full question text",
  "artifact_context": "artifact or product name",
  "entity_type": "reviewers|contributors|participants|etc",
  "parsed_at": timestamp
}
```