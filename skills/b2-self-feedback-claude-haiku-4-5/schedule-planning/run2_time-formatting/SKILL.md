---
name: run2_time-formatting
description: Format dates and times with strict adherence to required formats
---

# Strict Time and Date Formatting

## Purpose
Generate properly formatted date and time strings that exactly match requirements.

## Date Format Specification

**Required format**: `{day_name}, {month} {DD}, {YYYY}`

### Rules:
- Day name: Full name (Monday, Tuesday, ..., Sunday)
- Month: Full name (January, February, ..., December)
- Day: Always 2 digits with leading zero (01, 02, ..., 31)
- Year: 4 digits (2026)

### Implementation:

```python
from datetime import datetime

def format_date_strict(date_obj):
    """
    Format date exactly as required.

    Args:
        date_obj: datetime.date or datetime.datetime

    Returns:
        str: "Monday, March 09, 2026"

    Examples:
        ✓ Monday, March 09, 2026
        ✓ Thursday, January 08, 2026
        ✗ Monday, March 9, 2026 (missing leading zero)
        ✗ March 9, 2026 (missing day name)
        ✗ Monday, Mar 9, 2026 (abbreviated month)
    """
    day_name = date_obj.strftime("%A")        # Monday
    month_name = date_obj.strftime("%B")      # March
    day_two_digit = date_obj.strftime("%d")   # 09 (ensures leading zero)
    year_four_digit = date_obj.strftime("%Y") # 2026

    return f"{day_name}, {month_name} {day_two_digit}, {year_four_digit}"


# Test cases
test_dates = [
    (datetime(2026, 3, 9), "Monday, March 09, 2026"),
    (datetime(2026, 1, 8), "Thursday, January 08, 2026"),
    (datetime(2026, 1, 1), "Thursday, January 01, 2026"),
    (datetime(2026, 12, 31), "Thursday, December 31, 2026"),
]

for date, expected in test_dates:
    result = format_date_strict(date)
    assert result == expected, f"Expected '{expected}', got '{result}'"
```

## Time Format Specification

**Required format**: `{HH:MM AM/PM} - {HH:MM AM/PM}`

### Rules:
- Hour: Always 2 digits with leading zero (01, 02, ..., 12)
- Minute: Always 2 digits with leading zero (00, 01, ..., 59)
- Period: Uppercase (AM or PM)
- Separator: ` - ` (space-dash-space)
- Use 12-hour format, never 24-hour

### Implementation:

```python
def format_time_12hr(hour_24, minute=0):
    """
    Convert 24-hour time to 12-hour with AM/PM.

    Args:
        hour_24: 0-23
        minute: 0-59

    Returns:
        (hour_12, minute, is_pm): (1-12, 0-59, bool)

    Examples:
        13 -> (1, is_pm=True)   # 1:00 PM
        0 -> (12, is_pm=False)  # 12:00 AM
        12 -> (12, is_pm=True)  # 12:00 PM
    """
    is_pm = hour_24 >= 12
    hour_12 = hour_24 % 12
    if hour_12 == 0:
        hour_12 = 12

    return (hour_12, minute, is_pm)


def format_time_strict(hour_24, minute=0):
    """
    Format time exactly as required.

    Args:
        hour_24: 0-23 (24-hour format)
        minute: 0-59

    Returns:
        str: "01:00 PM" format

    Examples:
        ✓ 09:00 AM
        ✓ 01:00 PM
        ✓ 12:00 PM
        ✗ 9:00 AM (missing leading zero)
        ✗ 01:00 pm (lowercase)
        ✗ 1:00 PM (missing leading zero on hour)
    """
    hour_12, minute, is_pm = format_time_12hr(hour_24, minute)
    hour_str = str(hour_12).zfill(2)  # Ensure 2 digits: 1 -> "01"
    minute_str = str(minute).zfill(2)  # Ensure 2 digits: 0 -> "00"
    period = "PM" if is_pm else "AM"

    return f"{hour_str}:{minute_str} {period}"


def format_time_range_strict(start_time, end_time):
    """
    Format time range.

    Args:
        start_time: str "HH:MM" (24-hour) or (hour, minute) tuple
        end_time: str "HH:MM" (24-hour) or (hour, minute) tuple

    Returns:
        str: "09:00 AM - 10:30 AM"
    """
    # Parse inputs
    if isinstance(start_time, str):
        h, m = map(int, start_time.split(':'))
        start_formatted = format_time_strict(h, m)
    else:
        start_formatted = format_time_strict(*start_time)

    if isinstance(end_time, str):
        h, m = map(int, end_time.split(':'))
        end_formatted = format_time_strict(h, m)
    else:
        end_formatted = format_time_strict(*end_time)

    return f"{start_formatted} - {end_formatted}"


# Test cases
assert format_time_strict(13) == "01:00 PM"
assert format_time_strict(9, 0) == "09:00 AM"
assert format_time_strict(12, 30) == "12:30 PM"
assert format_time_strict(0, 0) == "12:00 AM"
assert format_time_strict(12, 0) == "12:00 PM"
assert format_time_range_strict("13:00", "14:00") == "01:00 PM - 02:00 PM"
assert format_time_range_strict("09:00", "10:30") == "09:00 AM - 10:30 AM"
```

## Duration Display

When showing meeting duration, format as: `{duration} hour(s)`

```python
def format_duration(hours):
    """
    Format duration for display.

    Args:
        hours: float (1.0, 1.5, 0.75)

    Returns:
        str: "1 hour(s)" or "1.5 hour(s)"
    """
    # Keep decimal if present, otherwise show integer
    if hours == int(hours):
        return f"{int(hours)} hour(s)"
    else:
        return f"{hours} hour(s)"
```

## Complete Reply Template

```python
REPLY_TEMPLATE = """Hi,

Thank you for your meeting request.

I can be available:

Date: {date}
Time: {time_range}
Duration: {duration} hour(s)

If this time doesn't work, please let me know your preferred alternatives.

Best regards,
ConSkillBench"""


def generate_reply(date_obj, start_hour_24, start_minute, end_hour_24, end_minute, duration_hours):
    """Generate complete reply with all formatting correct."""
    date_str = format_date_strict(date_obj)
    time_str = format_time_range_strict((start_hour_24, start_minute), (end_hour_24, end_minute))
    duration_str = format_duration(duration_hours)

    return REPLY_TEMPLATE.format(
        date=date_str,
        time_range=time_str,
        duration=duration_str
    )
```
