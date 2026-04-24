---
name: email-json-parsing-and-meeting-extraction
description: Use this skill when you need to parse meeting schedule request emails from a JSON file, extract meeting duration, date/time constraints, sender information, and message IDs. Handles various natural language patterns for expressing meeting preferences.
---

## Parsing Meeting Request Emails from JSON

### Expected JSON Structure

The input file `/root/test_input.json` typically contains an array of email objects:

```json
[
  {
    "messageID": "msg001",
    "from": "alice@example.com",
    "to": "user@example.com",
    "subject": "Meeting Request",
    "body": "Hi, I'd like to schedule a 1-hour meeting next Thursday..."
  }
]
```

### Loading and Parsing

```python
import json

with open("/root/test_input.json", "r") as f:
    emails = json.load(f)

# Handle both list and dict with key like "emails"
if isinstance(emails, dict):
    # Try common keys
    for key in ["emails", "messages", "data"]:
        if key in emails:
            emails = emails[key]
            break
```

### Extracting Meeting Duration

Common patterns in natural language:
- "1-hour meeting" / "1 hour meeting"
- "30-minute meeting" / "30 min meeting"
- "a meeting for 2 hours"
- "1.5 hours" / "1.5-hour meeting"
- "90 minutes"

```python
import re

def extract_duration(text):
    """Extract meeting duration in minutes from text."""
    text = text.lower()
    
    # Pattern: X-hour or X hour(s)
    match = re.search(r'(\d+\.?\d*)\s*[-–]?\s*hours?', text)
    if match:
        return float(match.group(1)) * 60
    
    # Pattern: X-minute or X minute(s) or X min
    match = re.search(r'(\d+)\s*[-–]?\s*(?:minutes?|mins?)', text)
    if match:
        return int(match.group(1))
    
    # Pattern: "half hour" or "half an hour"
    if "half hour" in text or "half an hour" in text:
        return 30
    
    # Default assumption
    return 60  # 1 hour default
```

### Extracting Date Constraints

```python
from datetime import datetime, timedelta
import re

def extract_date_constraints(text):
    """Extract date preferences from email text."""
    text_lower = text.lower()
    
    # Explicit dates: "January 8, 2026", "01/08/2026", "2026-01-08"
    # Pattern for Month DD, YYYY
    match = re.search(
        r'(january|february|march|april|may|june|july|august|september|october|november|december)'
        r'\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})',
        text_lower
    )
    if match:
        month_str, day, year = match.group(1), match.group(2), match.group(3)
        date_str = f"{month_str} {day} {year}"
        return datetime.strptime(date_str, "%B %d %Y").date()
    
    # ISO format
    match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d").date()
    
    # Relative dates: "next Monday", "this Friday"
    day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for i, day_name in enumerate(day_names):
        if day_name in text_lower:
            return day_name  # Return as string for further processing
    
    return None
```

### Extracting Time Preferences

```python
def extract_time_preference(text):
    """Extract preferred time from email text."""
    text_lower = text.lower()
    
    # "morning", "afternoon", "after 2 PM", "before noon"
    if "morning" in text_lower:
        return ("morning", "09:00", "12:00")
    if "afternoon" in text_lower:
        return ("afternoon", "12:00", "17:00")
    
    # Specific time: "at 2 PM", "around 10:00 AM", "after 3:00 PM"
    match = re.search(r'(?:at|around|after|before|by)\s+(\d{1,2}):?(\d{2})?\s*(am|pm)', text_lower)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        ampm = match.group(3)
        return ("specific", f"{hour:02d}:{minute:02d} {ampm.upper()}")
    
    return None
```

### Extracting Sender/Recipient Info

```python
def extract_email_details(email_obj):
    """Extract all relevant fields from an email object."""
    return {
        "message_id": email_obj.get("messageID") or email_obj.get("message_id") or email_obj.get("id"),
        "sender": email_obj.get("from") or email_obj.get("sender"),
        "recipient": email_obj.get("to") or email_obj.get("recipient"),
        "subject": email_obj.get("subject", ""),
        "body": email_obj.get("body") or email_obj.get("message") or email_obj.get("content", ""),
    }
```

### Full Extraction Pipeline

```python
def parse_meeting_request(email_obj):
    details = extract_email_details(email_obj)
    body = details["subject"] + " " + details["body"]
    
    duration_minutes = extract_duration(body)
    date_constraint = extract_date_constraints(body)
    time_preference = extract_time_preference(body)
    
    return {
        **details,
        "duration_minutes": duration_minutes,
        "duration_hours": duration_minutes / 60,
        "date_constraint": date_constraint,
        "time_preference": time_preference,
    }
```