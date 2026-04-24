---
name: run2_request-parsing-advanced
description: Parse meeting requests with timezone handling and constraint detection
---

# Advanced Meeting Request Parsing

## Purpose
Extract all meeting constraints and preferences with explicit timezone handling and consistency validation.

## Timezone Conversion Map

```python
TIMEZONE_OFFSETS = {
    "PST": -8,  # Pacific Standard Time
    "MST": -7,  # Mountain Standard Time
    "CST": -6,  # Central Standard Time
    "EST": -5,  # Eastern Standard Time
    "UTC": 0,
    "GMT": 0,
}

def convert_time_to_calendar_tz(time_str, from_tz, to_tz="EST"):
    """
    Convert time from one timezone to another.

    Example:
        4:00 PM PST -> 7:00 PM EST (PST is 3 hours behind EST)
        1:00 PM PST -> 4:00 PM EST
    """
    offset_diff = TIMEZONE_OFFSETS[to_tz] - TIMEZONE_OFFSETS[from_tz]
    # Add offset_diff hours to the time
    return add_hours(time_str, offset_diff)
```

## Request Parsing with Validation

```python
def parse_request_with_validation(email_obj):
    """
    Extract and validate all meeting request components.

    Returns:
        {
            'from_email': str,
            'duration_hours': float,
            'target_date': date,
            'available_start': time (in calendar's timezone),
            'available_end': time (in calendar's timezone),
            'request_timezone': str,  # timezone specified in request
            'is_flexible': bool,  # is this a preference or hard constraint?
            'warnings': [list of inconsistencies/notes]
        }
    """
    warnings = []

    # 1. Extract duration
    duration = extract_duration(email_text)
    if not duration:
        warnings.append("Duration not explicitly stated")
        return None

    # 2. Extract date
    target_date = extract_date(email_text)
    if not target_date:
        warnings.append("Target date not found")
        return None

    # 3. Extract availability window with timezone
    avail_window, request_tz = extract_time_window_with_tz(email_text)
    if not avail_window:
        warnings.append("Availability window not found")
        return None

    # 4. Validate consistency
    if "morning" in email_text.lower() and (avail_window[0] >= 12 or avail_window[1] >= 17):
        warnings.append("Time window (afternoon) contradicts 'morning slots' preference")
        # Note: Don't reject, just flag for review

    # 5. Convert to calendar timezone (EST)
    if request_tz and request_tz != "EST":
        avail_start_est = convert_to_est(avail_window[0], request_tz)
        avail_end_est = convert_to_est(avail_window[1], request_tz)
    else:
        avail_start_est = avail_window[0]
        avail_end_est = avail_window[1]

    # 6. Determine if preference or constraint
    is_flexible = "prefer" in email_text.lower() or "would like" in email_text.lower()

    return {
        'from_email': email_obj['from_email'],
        'duration_hours': duration,
        'target_date': target_date,
        'available_start': avail_start_est,
        'available_end': avail_end_est,
        'request_timezone': request_tz,
        'is_flexible': is_flexible,
        'warnings': warnings
    }
```

## Edge Case Handling

### Timezone Specification Detection

```python
def extract_timezone_from_window(text):
    """
    Detect timezone mentions:
    - "1:00 PM to 5:00 PM PST" -> PST
    - "between 10am and 2pm" -> None (assume EST if not specified)
    - "3:30pm and 5:30pm" -> Ambiguous format, assume same tz as calendar

    Returns:
        timezone_str or None
    """
    tz_patterns = {
        'PST': r'\bPST\b',
        'MST': r'\bMST\b',
        'CST': r'\bCST\b',
        'EST': r'\bEST\b',
        'UTC': r'\bUTC\b',
    }

    for tz, pattern in tz_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return tz

    return None  # Default: assume EST/calendar timezone
```

### Ambiguous Time Handling

When request says "morning slots between 3:30pm and 5:30pm":
```python
# This is ambiguous:
# Option 1: Times are in wrong timezone (3:30am intended, written as 3:30pm)
# Option 2: Description is wrong (afternoon slots intended, written as morning)
# Option 3: Times are in requester's timezone (if in PST, could mean morning in their location)

# Best approach: Flag for review but proceed with stated times
warnings.append("Inconsistency: 'morning' description vs afternoon times (3:30pm-5:30pm)")
# Use the explicit times as written, not the description
```

## Implementation

```python
import re
from datetime import datetime

def extract_time_window_with_tz(email_text):
    """
    Extract time range with explicit timezone detection.

    Handles patterns like:
    - "10:00am to 2:00pm" -> (10:00, 14:00), None (no tz specified)
    - "1:00 PM and 5:00 PM PST" -> (13:00, 17:00), "PST"
    - "between 3:30pm and 5:30pm" -> (15:30, 17:30), None
    """
    # Pattern for time range with optional timezone
    pattern = r'(\d{1,2}):?(\d{2})?\s*(am|pm)?.*?(?:to|and|-)\s*(\d{1,2}):?(\d{2})?\s*(am|pm)?\s*(?:(PST|EST|CST|MST|UTC))?'

    match = re.search(pattern, email_text, re.IGNORECASE)
    if match:
        start_hour = int(match.group(1))
        start_period = match.group(3)  # am or pm
        end_hour = int(match.group(4))
        end_period = match.group(6)  # am or pm
        timezone = match.group(7) if match.group(7) else None

        # Convert to 24-hour format
        if start_period and start_period.lower() == 'pm' and start_hour != 12:
            start_hour += 12
        elif start_period and start_period.lower() == 'am' and start_hour == 12:
            start_hour = 0

        if end_period and end_period.lower() == 'pm' and end_hour != 12:
            end_hour += 12
        elif end_period and end_period.lower() == 'am' and end_hour == 12:
            end_hour = 0

        return ((start_hour, end_hour), timezone)

    return (None, None)
```
