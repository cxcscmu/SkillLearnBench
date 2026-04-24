---
name: email-parser
description: Extract meeting request details from JSON input. Use whenever you process meeting requests.
---
# Email Parser Skill

This skill provides instructions for parsing meeting request emails from `/root/test_input.json`.

## Input Format
The file `/root/test_input.json` contains a list of requests.

## Extraction details
For each email, extract:
- Message ID
- Sender Email
- Meeting Duration (hours)
- Any specific constraints (e.g., "after 2pm", "on Monday")
