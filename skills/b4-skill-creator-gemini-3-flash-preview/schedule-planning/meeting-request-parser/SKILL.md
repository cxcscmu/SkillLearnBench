---
name: meeting-request-parser
description: Extracts meeting durations and constraints from a meeting request JSON file (e.g., test_input.json). Use this whenever you need to process incoming meeting invitations to understand their specific requirements.
---

# Meeting Request Parser

This skill facilitates extracting key information from structured meeting request JSON data.

## Input format
The input should be a JSON array of objects representing email requests. Each object should contain:
- `id` (or `messageID`): A unique identifier for the request.
- `from`: The sender's email address.
- `subject`: The email subject line.
- `body`: The content of the email, where constraints and duration are typically found.

## Key fields to extract
- **Duration**: Identify the requested duration (e.g., "1 hour", "30 minutes"). Convert all to hours or minutes consistently.
- **Date constraints**: Look for specific days or dates mentioned (e.g., "on Thursday", "next week", "January 08").
- **Time constraints**: Look for specific time ranges (e.g., "after 2 PM", "between 9:00 AM and 11:00 AM", "before noon").

## Example processing
Input body: "Hi, can we meet for 1.5 hours next Thursday morning?"
Output:
- Duration: 1.5 hours
- Constraint: Thursday morning (typically 9:00 AM - 12:00 PM unless specified)
