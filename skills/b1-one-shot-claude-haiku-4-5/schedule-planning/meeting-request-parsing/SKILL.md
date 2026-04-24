---
name: meeting-request-parsing
description: Parse meeting request emails from JSON format and extract duration and time constraints
---

# Meeting Request Parsing Skill

## Overview
This skill covers parsing JSON-formatted meeting request emails to extract key scheduling information: meeting duration, date constraints, time window constraints, and sender email.

## Key Concepts

### Meeting Request Structure
Typical meeting request contains:
- **Duration**: stated explicitly (e.g., "one-hour", "1.5 hour")
- **Date**: specific date requested
- **Time Window**: earliest and latest times when person is available
- **Time Zone**: explicitly stated or inferred
- **Sender**: email address for reply

### Email Text Parsing Patterns
Common patterns in email bodies:
- Duration: "one-hour meeting", "1.5 hour", "45-minute", "30 min"
- Date: "March 9th, 2026", "March 9, 2026", "on March 9"
- Availability: "available from 10am to 2pm", "between 1:00 PM and 5:00 PM"
- Time zone: "PST", "EST", "UTC-8", etc.

## Code Examples

### JSON Loading and Basic Parsing
```python
import json
import re

# Load email requests
with open('/root/test_input.json') as f:
    requests = json.load(f)

for request in requests:
    email_text = request['email_text']
    sender = request['from_email']
    print(f"From: {sender}")
    print(f"Body: {email_text}")
```

### Extracting Duration
```python
def extract_duration(email_text):
    """Extract meeting duration in hours"""
    # Match patterns: "one-hour", "1 hour", "1.5 hours", "45 minute", "30 min"
    patterns = [
        r'(\d+\.?\d*)\s*hour',
        r'(\d+)\s*minute',
        r'(\d+)\s*min(?!ute)',
    ]

    for pattern in patterns:
        match = re.search(pattern, email_text, re.IGNORECASE)
        if match:
            duration_str = match.group(1)
            if 'minute' in pattern:
                return float(duration_str) / 60  # Convert minutes to hours
            else:
                return float(duration_str)

    # Handle written-out numbers
    if 'one hour' in email_text.lower():
        return 1.0
    if 'one and a half' in email_text.lower() or '1.5 hour' in email_text.lower():
        return 1.5

    return None
```

### Extracting Date
```python
from datetime import datetime

def extract_date(email_text):
    """Extract meeting date from email"""
    # Match patterns: "March 9th, 2026", "March 9, 2026", "on March 9"
    pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})'

    match = re.search(pattern, email_text, re.IGNORECASE)
    if match:
        month_str, day_str, year_str = match.groups()
        date_obj = datetime.strptime(f'{month_str} {day_str} {year_str}', '%B %d %Y')
        return date_obj

    return None
```

### Extracting Time Window
```python
def extract_time_window(email_text):
    """Extract available time window (earliest to latest)"""
    # Match patterns: "from 10:00am to 2:00pm", "between 1:00 PM and 5:00 PM"
    pattern = r'(?:from|between)\s+(\d{1,2}):?(\d{2})?\s*(?:AM|PM|am|pm)?\s+(?:to|and)\s+(\d{1,2}):?(\d{2})?\s*(AM|PM|am|pm|PST|EST|UTC-\d+)?'

    match = re.search(pattern, email_text, re.IGNORECASE)
    if match:
        start_hour, start_min, end_hour, end_min, tz = match.groups()
        start_hour = int(start_hour)
        end_hour = int(end_hour)
        start_min = int(start_min) if start_min else 0
        end_min = int(end_min) if end_min else 0

        return {
            'start': (start_hour, start_min),
            'end': (end_hour, end_min),
            'timezone': tz.upper() if tz else None
        }

    return None
```

### Complete Request Parsing
```python
def parse_meeting_request(request_dict):
    """Parse a complete meeting request"""
    email_text = request_dict['email_text']
    sender = request_dict['from_email']

    duration_hours = extract_duration(email_text)
    date = extract_date(email_text)
    time_window = extract_time_window(email_text)

    return {
        'sender': sender,
        'duration_hours': duration_hours,
        'requested_date': date,
        'available_times': time_window,
        'raw_text': email_text
    }
```

## Time Zone Handling
```python
def normalize_timezone(tz_string):
    """Normalize timezone to standard format"""
    tz_map = {
        'PST': 'US/Pacific',
        'EST': 'US/Eastern',
        'CST': 'US/Central',
        'MST': 'US/Mountain'
    }
    return tz_map.get(tz_string, tz_string)

def convert_time_zones(start_hour, start_min, from_tz, to_tz):
    """Convert time from one timezone to another"""
    from datetime import datetime, timezone
    import pytz

    # Create a datetime in source timezone
    src_tz = pytz.timezone(from_tz)
    dst_tz = pytz.timezone(to_tz)

    dt = src_tz.localize(datetime(2026, 3, 9, start_hour, start_min))
    converted = dt.astimezone(dst_tz)

    return converted.hour, converted.minute
```

## Common Patterns to Handle
- Duration with/without articles: "a one-hour meeting" vs "one hour meeting"
- Time with/without colons: "10:00am" vs "10am"
- Ordinal suffixes: "March 9th" vs "March 9"
- Written-out numbers: "one hour" vs "1 hour"
- Time zone abbreviations: "PST", "EST", "CST"

## Best Practices
1. Always validate extracted values (reasonable hours, future dates)
2. Handle both written and numeric forms of durations
3. Normalize time zones before comparison
4. Extract sender email for reply tracking
5. Store raw text for debugging and validation
