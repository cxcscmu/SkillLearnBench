---
name: datetime-formatting
description: Format dates and times according to specific requirements for meeting confirmations
---

# Date/Time Formatting Skill

## Overview
This skill covers formatting dates and times in the specific formats required for meeting confirmation replies, including proper day names, 12-hour AM/PM format, and date formatting.

## Key Concepts

### Required Format Specifications

**Date Format**: `{day_name}, {month} {DD}, {YYYY}`
- Example: `Thursday, January 08, 2026`
- **NOT**: `January 8th, 2026` or `January 8, 2026`
- Two-digit day with leading zero
- Full month name (not abbreviated)
- Full day name (not abbreviated)

**Time Format**: `{HH:MM AM/PM} - {HH:MM AM/PM}`
- Example: `09:00 AM - 10:30 AM`
- Two-digit hour with leading zero
- Two-digit minute with leading zero (never just `9:00 AM`)
- Uppercase AM/PM with space before it

## Code Examples

### Format Date
```python
from datetime import datetime

def format_date(date_obj):
    """Format datetime to 'Thursday, January 08, 2026' format"""
    return date_obj.strftime('%A, %B %d, %Y')

# Example
d = datetime(2026, 1, 8)
print(format_date(d))  # Thursday, January 08, 2026
```

### Format Time Range
```python
def format_time(hour, minute, use_am_pm=True):
    """Format single time as 'HH:MM AM/PM'"""
    time_obj = datetime(2026, 1, 1, hour, minute)
    if use_am_pm:
        return time_obj.strftime('%I:%M %p')
    else:
        return time_obj.strftime('%H:%M')

def format_time_range(start_hour, start_minute, end_hour, end_minute):
    """Format time range as 'HH:MM AM/PM - HH:MM AM/PM'"""
    start_time = format_time(start_hour, start_minute)
    end_time = format_time(end_hour, end_minute)
    return f'{start_time} - {end_time}'

# Example
print(format_time_range(9, 0, 10, 30))  # 09:00 AM - 10:30 AM
print(format_time_range(13, 30, 15, 0))  # 01:30 PM - 03:00 PM
```

### Format Duration in Hours
```python
def format_duration(duration_hours):
    """Format duration as 'X hour(s)' - match request format"""
    if duration_hours == int(duration_hours):
        hours = int(duration_hours)
        return f'{hours} hour' if hours == 1 else f'{hours} hours'
    else:
        # Handle fractional hours
        total_minutes = int(duration_hours * 60)
        if total_minutes % 60 == 0:
            hours = total_minutes // 60
            return f'{hours} hours'
        else:
            return f'{duration_hours} hours'

# Examples
print(format_duration(1.0))    # 1 hour
print(format_duration(1.5))    # 1.5 hours
print(format_duration(0.75))   # 0.75 hours
```

### Complete Reply Generation
```python
def generate_reply(recipient_name, meeting_date, start_hour, start_minute, end_hour, end_minute, duration_hours):
    """Generate complete meeting confirmation reply"""
    date_str = format_date(meeting_date)
    time_range = format_time_range(start_hour, start_minute, end_hour, end_minute)
    duration_str = format_duration(duration_hours)

    reply = f"""Hi,

Thank you for your meeting request.

I can be available:

Date: {date_str}
Time: {time_range}
Duration: {duration_str}

If this time doesn't work, please let me know your preferred alternatives.

Best regards,
ConSkillBench"""

    return reply
```

### Timezone-Aware Formatting
```python
import pytz
from datetime import datetime

def format_datetime_with_timezone(date_obj, hour, minute, timezone_name='US/Eastern'):
    """Format datetime with timezone context"""
    tz = pytz.timezone(timezone_name)
    # Create a timezone-aware datetime
    dt = tz.localize(datetime(date_obj.year, date_obj.month, date_obj.day, hour, minute))

    date_str = dt.strftime('%A, %B %d, %Y')
    time_str = dt.strftime('%I:%M %p')

    return date_str, time_str
```

### Validate Format Compliance
```python
import re

def validate_date_format(formatted_date):
    """Check if date follows correct format"""
    pattern = r'^[A-Z][a-z]+, [A-Z][a-z]+ \d{2}, \d{4}$'
    return bool(re.match(pattern, formatted_date))

def validate_time_format(formatted_time):
    """Check if time follows correct format"""
    pattern = r'^\d{2}:\d{2} [AP]M - \d{2}:\d{2} [AP]M$'
    return bool(re.match(pattern, formatted_time))

# Examples
print(validate_date_format('Thursday, January 08, 2026'))  # True
print(validate_date_format('January 8, 2026'))             # False
print(validate_time_format('09:00 AM - 10:30 AM'))         # True
print(validate_time_format('9:00 AM - 10:30 AM'))          # False
```

## Common Formatting Errors to Avoid
1. ❌ Single-digit day: `January 8` → ✅ `January 08`
2. ❌ Abbreviated day: `Thu` → ✅ `Thursday`
3. ❌ Abbreviated month: `Jan` → ✅ `January`
4. ❌ No leading zero on hour: `9:00 AM` → ✅ `09:00 AM`
5. ❌ Lowercase AM/PM: `09:00 am` → ✅ `09:00 AM`
6. ❌ Written ordinal: `January 8th` → ✅ `January 08`
7. ❌ Year only 2 digits: `January 08, 26` → ✅ `January 08, 2026`

## Python datetime Directives Reference
| Directive | Meaning | Example |
|-----------|---------|---------|
| `%A` | Full weekday name | `Thursday` |
| `%B` | Full month name | `January` |
| `%d` | Day of month (02-31) | `08` |
| `%Y` | Year with century | `2026` |
| `%I` | Hour 12-hour (01-12) | `09` |
| `%M` | Minute (00-59) | `30` |
| `%p` | AM/PM | `AM` |

## Best Practices
1. Always use `%I:%M %p` for 12-hour format with AM/PM
2. Always use `%d` for zero-padded days
3. Always use `%A, %B %d, %Y` for complete date format
4. Validate formatted output against required patterns
5. Test edge cases: midnight, noon, early morning, late night
6. When working with different timezones, convert before formatting
