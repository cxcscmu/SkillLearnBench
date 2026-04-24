---
name: meeting-request-parsing
description: Parse meeting request emails from test_input.json to extract meeting details. This skill helps extract recipient email, message ID, meeting duration, and any date/time constraints from JSON email records. Use this whenever you need to process meeting requests from a JSON file.
---

# Meeting Request Parsing

## Overview

This skill parses meeting request emails stored in JSON format, extracting:
- Recipient email address
- Message ID (for reply tracking)
- Meeting duration in hours
- Specific date/time constraints mentioned in the message body
- Any other scheduling preferences

## Reading and Parsing test_input.json

### Step 1: Read the JSON File

Use the Read tool to load the meeting requests:

```
Read /root/test_input.json
```

### Step 2: Parse JSON Structure

The file should contain an array of email objects. Each email typically has:

```json
{
  "messageID": "string",
  "from": "recipient_email@domain.com",
  "subject": "Meeting Request",
  "body": "Meeting body text with duration and constraints"
}
```

### Step 3: Extract Key Information

For each email, extract:

1. **Message ID**: Unique identifier for this request (used in reply filename)
2. **Recipient Email**: The sender's email (from the `from` field)
3. **Meeting Duration**: Parse the body for duration mentions:
   - Look for patterns: "30 minutes", "1 hour", "2 hours", "45 minutes"
   - Convert to decimal hours (e.g., 30 min = 0.5 hours)
4. **Date/Time Constraints**: Check body for:
   - Specific date requests: "Tuesday", "March 25", "next week"
   - Time preferences: "morning", "afternoon", "9am", "after 2pm"
   - Unavailability: "not before", "not after", "cannot on"
5. **Special Notes**: Any other preferences mentioned

### Step 4: Normalize Duration

Convert meeting duration to consistent format:

```
"30 minutes" → 0.5 hours
"1 hour" → 1.0 hours
"1.5 hours" or "1 hour 30 minutes" → 1.5 hours
"2 hours" → 2.0 hours
```

If duration is not explicitly stated, use a default (typically 1 hour).

### Step 5: Record Parsed Requests

Create a structured list:

```json
{
  "requests": [
    {
      "messageID": "msg123",
      "recipient": "user@example.com",
      "duration_hours": 1.0,
      "date_constraints": "any day",
      "time_constraints": "none",
      "parsed_from_body": "relevant excerpt from email body"
    }
  ]
}
```

## Constraint Interpretation

- **No constraints mentioned**: Assume any available time works
- **Date mentioned**: Prioritize that specific date
- **Time range mentioned**: Schedule within that time range
- **"Morning"**: Typically 8 AM - 12 PM
- **"Afternoon"**: Typically 12 PM - 5 PM
- **Specific hour**: Use exact hour mentioned

## Output Format

Return parsed requests as a structured list suitable for the meeting slot finder algorithm.
