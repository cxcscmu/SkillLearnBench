---
name: schedule-constraint-parsing
description: Uses regular expressions to parse dates, time ranges, and durations from natural language text like meeting requests.
---

# Schedule Constraint Parsing

This skill outlines how to use standard Python `re` and `datetime` libraries to extract specific meeting requirements (duration, dates, start/end time windows) from email bodies.

## Common Regex Patterns

### 1. Extracting Duration
People describe duration in hours or minutes (e.g., "1.5 hour", "one-hour", "45-minute").

```python
import re

def parse_duration(text):
    duration_min = None
    
    # Hour pattern
    hr_match = re.search(r'([\d\.]+|(?:one|two|three|half))\s*(?:hour|hr)', text, re.IGNORECASE)
    if hr_match:
        val = hr_match.group(1).lower()
        if val == 'one': hours = 1.0
        elif val == 'two': hours = 2.0
        elif val == 'half': hours = 0.5
        else: hours = float(val)
        duration_min = int(hours * 60)
        
    # Minute pattern
    min_match = re.search(r'(\d+)\s*(?:minute|min)', text, re.IGNORECASE)
    if min_match:
        duration_min = int(min_match.group(1))
        
    return duration_min
```

### 2. Extracting Time Range
Extracting available start and end boundaries (e.g., "between 10:00am to 2:00pm", "between 1:00 PM and 5:00 PM PST").

```python
def parse_time_window(text):
    # Extracts HH:MM AM/PM pairs
    pattern = r'(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)).*?(?:to|and|-)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM))'
    match = re.search(pattern, text)
    if match:
        start_time_str = match.group(1)
        end_time_str = match.group(2)
        return start_time_str, end_time_str
    return None, None
```

These simple extraction functions are excellent bases for parsing natural language scheduling intents.
