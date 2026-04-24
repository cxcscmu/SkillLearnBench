---
name: json-email-extraction
description: Use this skill to read and parse structured email data from a JSON file, extracting fields like message ID, sender email, subject, body, and meeting constraints (duration, preferred times/dates).
---

## Reading Email Requests from JSON

### File Structure
The input file `/root/test_input.json` contains an array of email objects. Each object typically includes:
- `messageID` (or similar key): unique identifier for the email
- `from` / `sender` / `email`: sender's email address (used as recipient for reply)
- `subject`: email subject line
- `body` / `message`: the text content of the email

### Parsing with Python

```python
import json

with open('/root/test_input.json', 'r') as f:
    emails = json.load(f)

# emails may be a list or dict with a key like "emails" or "messages"
if isinstance(emails, dict):
    email_list = emails.get('emails') or emails.get('messages') or list(emails.values())
else:
    email_list = emails

for email in email_list:
    message_id = email.get('messageID') or email.get('id')
    recipient = email.get('from') or email.get('sender') or email.get('email')
    body = email.get('body') or email.get('message') or email.get('content')
    subject = email.get('subject', '')
    print(message_id, recipient, body)
```

### Extracting Meeting Constraints from Body Text

Use regex and keyword scanning to find:

```python
import re

def extract_meeting_details(body):
    details = {}
    
    # Duration: look for "X hour(s)", "X-hour", "30 minutes", "1.5 hours", etc.
    duration_match = re.search(
        r'(\d+(?:\.\d+)?)\s*[-]?\s*(hour|hr|minute|min)s?', body, re.IGNORECASE)
    if duration_match:
        value = float(duration_match.group(1))
        unit = duration_match.group(2).lower()
        if 'min' in unit:
            details['duration_hours'] = value / 60
        else:
            details['duration_hours'] = value
    
    # Date constraints: "next Monday", "on Friday", specific dates
    date_patterns = [
        r'\b(next\s+)?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\b',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            details['date_constraint'] = match.group(0)
            break
    
    # Time constraints: "after 2pm", "before noon", "between 10am and 12pm"
    time_match = re.search(
        r'(after|before|between|around|at)\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)',
        body, re.IGNORECASE)
    if time_match:
        details['time_constraint'] = time_match.group(0)
    
    return details
```

### Key Points
- Always handle missing keys gracefully with `.get()`
- Duration in hours is the primary scheduling parameter
- Constraints are soft hints; if no slot matches, find nearest compatible slot
- The recipient email for the reply file is the **sender** of the incoming request