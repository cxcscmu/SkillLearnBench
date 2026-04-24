---
name: meeting-request-parser
description: Parse duration and time constraints from email text.
---

# Meeting Request Parser

This skill facilitates the extraction of meeting duration and time constraints from unstructured email text.

## Techniques

- Use regex to identify durations (e.g., "1.5 hour", "45-minute").
- Identify date mentions (e.g., "March 9th, 2026").
- Identify time windows (e.g., "10:00am to 2:00pm").

## Example Logic

```python
import re

def parse_meeting_request(email_text):
    # Regex for duration
    duration_match = re.search(r'(\d+(\.\d+)?)\s*hour', email_text)
    duration_min_match = re.search(r'(\d+)\s*minute', email_text)
    
    if duration_match:
        duration_hrs = float(duration_match.group(1))
    elif duration_min_match:
        duration_hrs = float(duration_min_match.group(1)) / 60
    else:
        duration_hrs = 1.0 # Default

    # Regex for time window (this is a simplified example)
    time_window = re.findall(r'(\d{1,2}:\d{2}\s*(?:am|pm|AM|PM))', email_text)
    # Parse window: start and end times
    
    return duration_hrs, time_window

# Tips: handle '1:00 PM' and '5:00 PM PST' correctly.
```
