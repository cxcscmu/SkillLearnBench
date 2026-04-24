---
name: email-scheduling
description: Parse meeting request emails to extract duration and time constraints, then find the earliest available time slot on a calendar.
---

# Email Meeting Scheduling

## Parsing Meeting Requests

### Extract duration from email text
```python
import re

def parse_duration_hours(text):
    """Extract meeting duration in hours from email text."""
    # Match patterns like "1 hour", "1.5 hour", "45 minutes", "45-minute"
    patterns = [
        r'(\d+(?:\.\d+)?)\s*-?\s*hour',
        r'(\d+)\s*-?\s*minute',
        r'(\d+(?:\.\d+)?)\s*hr',
    ]
    for i, pat in enumerate(patterns):
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            if 'minute' in pat:
                return val / 60
            return val
    return 1.0  # default 1 hour
```

### Extract time constraints
```python
from datetime import datetime, time
import re

def parse_time_range(text):
    """Extract available time range from email, returns (start_hour, end_hour) as floats."""
    # Match patterns like "10:00am", "2:00 PM", "1pm", "13:00"
    time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm|AM|PM)?'
    matches = re.findall(time_pattern, text)

    times = []
    for h, m, period in matches:
        h = int(h)
        m = int(m) if m else 0
        if period:
            period = period.lower()
            if period == 'pm' and h != 12:
                h += 12
            elif period == 'am' and h == 12:
                h = 0
        times.append(h + m / 60)

    if len(times) >= 2:
        return times[-2], times[-1]  # last two times found
    return None, None
```

### Time zone conversion
```python
def to_eastern(hour, from_tz):
    """Convert hour from given timezone to Eastern Time."""
    offsets = {
        'PST': 3,   # PST is UTC-8, EST is UTC-5, difference = +3
        'PDT': 2,   # PDT is UTC-7, EDT is UTC-4, difference = +3
        'CST': 1,   # CST is UTC-6, difference = +1
        'MST': 2,   # MST is UTC-7, difference = +2
        'EST': 0,
        'EDT': 0,
    }
    return hour + offsets.get(from_tz.upper(), 0)
```

### Find earliest available slot
```python
def find_earliest_slot(duration_hours, window_start, window_end, busy_slots):
    """
    Find earliest available slot of given duration.
    busy_slots: list of (start, end) tuples in hours
    Returns (start, end) or None
    """
    # Sort and merge busy slots
    busy = sorted(busy_slots)

    current = window_start
    while current + duration_hours <= window_end:
        # Check if current slot conflicts with any busy period
        slot_end = current + duration_hours
        conflict = False
        for bs, be in busy:
            if current < be and slot_end > bs:
                conflict = True
                current = be  # jump past the busy block
                break
        if not conflict:
            return current, current + duration_hours

    return None, None  # No slot found
```

### Format time for reply
```python
def format_time(hour):
    """Convert float hour to HH:MM AM/PM format."""
    h = int(hour)
    m = int(round((hour - h) * 60))
    if m == 60:
        h += 1
        m = 0
    period = "AM" if h < 12 else "PM"
    if h == 0: display_h = 12
    elif h > 12: display_h = h - 12
    else: display_h = h
    return f"{display_h:02d}:{m:02d} {period}"

def format_duration(hours):
    """Format duration for reply template."""
    if hours == int(hours):
        return str(int(hours))
    # e.g. 1.5 -> "1.5"
    return str(hours)
```

## Reply Template
```python
REPLY_TEMPLATE = """Hi,

    Thank you for your meeting request.

    I can be available:

    Date: {day_name}, {date_formatted}
    Time: {time_range}
    Duration: {meetingDuration} hour(s)

    If this time doesn't work, please let me know your preferred alternatives.

    Best regards,
    ConSkillBench"""

def generate_reply(date, start_hour, end_hour, duration_hours):
    day_name = date.strftime("%A")
    date_str = date.strftime("%B %d, %Y")  # January 08, 2026
    time_range = f"{format_time(start_hour)} - {format_time(end_hour)}"
    duration = format_duration(duration_hours)
    return REPLY_TEMPLATE.format(
        day_name=day_name,
        date_formatted=date_str,
        time_range=time_range,
        meetingDuration=duration
    )
```

## Notes
- All times should be scheduled in the calendar's timezone (Eastern Time per the PDF header)
- If a requester specifies PST, convert: PST + 3h = EST
- "Earliest compatible time" means find the first available slot, while ensuring all meetings can be accommodated without conflicts
- Blue calendar blocks can be overwritten; treat them as available slots
