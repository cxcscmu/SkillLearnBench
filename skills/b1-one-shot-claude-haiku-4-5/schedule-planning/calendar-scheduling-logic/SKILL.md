---
name: calendar-scheduling-logic
description: Find available time slots in a calendar and schedule meetings while respecting constraints
---

# Calendar Scheduling Logic Skill

## Overview
This skill covers scheduling algorithms to find available time slots in a calendar, handle time conflicts, prioritize blue-colored flexible blocks, and match meeting requests with available time windows.

## Key Concepts

### Calendar Representation
```python
# Event representation
event = {
    'name': 'Weekly Group Meeting',
    'start_hour': 10,
    'start_minute': 0,
    'end_hour': 11,
    'end_minute': 0,
    'color': 'red',           # 'red', 'blue', 'yellow', 'gray'
    'is_flexible': True/False # Only blue is True
}

# 15-minute interval representation
# 9:00am = index 0, 9:15am = index 1, etc.
```

### Constraint Types
1. **User Availability Window**: Person only available during specific hours
2. **Date Constraint**: Meeting must be on specific date
3. **Duration Requirement**: Meeting needs exact duration
4. **Block Overriding**: Blue blocks can be overridden for higher priority meetings

## Code Examples

### Time Conversion to Minutes
```python
def time_to_minutes(hour, minute):
    """Convert hour:minute to total minutes since midnight"""
    return hour * 60 + minute

def minutes_to_time(minutes):
    """Convert total minutes to (hour, minute) tuple"""
    hour = minutes // 60
    minute = minutes % 60
    return (hour, minute)
```

### Convert Time Slots to Intervals
```python
def time_range_to_intervals(start_hour, start_min, end_hour, end_min, interval_minutes=15):
    """Convert a time range to 15-minute interval indices"""
    start_total_min = time_to_minutes(start_hour, start_min)
    end_total_min = time_to_minutes(end_hour, end_min)

    intervals = []
    current = start_total_min
    while current < end_total_min:
        intervals.append(current // interval_minutes)
        current += interval_minutes

    return intervals
```

### Track Busy Intervals
```python
def mark_busy_intervals(calendar_events, day_start_hour=0, day_end_hour=24):
    """Mark all busy intervals in a day"""
    total_intervals = (day_end_hour - day_start_hour) * 60 // 15
    busy = [False] * total_intervals

    for event in calendar_events:
        intervals = time_range_to_intervals(
            event['start_hour'], event['start_minute'],
            event['end_hour'], event['end_minute']
        )
        for i in intervals:
            if 0 <= i < total_intervals:
                busy[i] = True

    return busy
```

### Find Available Slots (Basic)
```python
def find_available_slots(busy_array, duration_intervals):
    """Find all available slots of at least duration_intervals length"""
    available_slots = []
    consecutive = 0
    start_idx = None

    for i, is_busy in enumerate(busy_array):
        if not is_busy:
            if consecutive == 0:
                start_idx = i
            consecutive += 1

            if consecutive >= duration_intervals:
                available_slots.append((start_idx, i + 1))
        else:
            consecutive = 0

    return available_slots
```

### Filter by User Availability Window
```python
def filter_by_availability_window(available_slots, user_start, user_end, interval_minutes=15):
    """Filter slots to only those within user's available window"""
    user_start_intervals = time_to_minutes(user_start[0], user_start[1]) // interval_minutes
    user_end_intervals = time_to_minutes(user_end[0], user_end[1]) // interval_minutes

    filtered = []
    for start_idx, end_idx in available_slots:
        # Check if slot overlaps with user's availability
        if end_idx > user_start_intervals and start_idx < user_end_intervals:
            # Constrain to user's window
            constrained_start = max(start_idx, user_start_intervals)
            constrained_end = min(end_idx, user_end_intervals)
            filtered.append((constrained_start, constrained_end))

    return filtered
```

### Select Earliest Valid Slot
```python
def select_earliest_slot(available_slots, duration_intervals):
    """Select the earliest slot that can fit the duration"""
    for start_idx, end_idx in available_slots:
        slot_duration = end_idx - start_idx
        if slot_duration >= duration_intervals:
            return (start_idx, start_idx + duration_intervals)

    return None
```

### Handle Blue Block Override
```python
def create_busy_with_overrides(calendar_events, allow_blue_override=True):
    """Mark busy intervals, but allow blue blocks to be overridden"""
    total_intervals = 24 * 60 // 15
    busy = [False] * total_intervals
    blue_blocks = []

    for event in calendar_events:
        intervals = time_range_to_intervals(
            event['start_hour'], event['start_minute'],
            event['end_hour'], event['end_minute']
        )

        if event.get('color') == 'blue' and allow_blue_override:
            blue_blocks.append((intervals[0], intervals[-1]))
        else:
            for i in intervals:
                if 0 <= i < total_intervals:
                    busy[i] = True

    return busy, blue_blocks
```

### Complete Scheduling Algorithm
```python
def schedule_meeting(calendar_events, request):
    """
    Schedule a meeting respecting all constraints

    request = {
        'duration_hours': 1.0,
        'available_times': {'start': (10, 0), 'end': (14, 0), 'timezone': None},
        'timezone': 'US/Eastern'
    }
    """
    duration_minutes = request['duration_hours'] * 60
    duration_intervals = duration_minutes // 15

    # Get busy times and blue overridable blocks
    busy, blue_blocks = create_busy_with_overrides(calendar_events)

    # Find all available slots
    available_slots = find_available_slots(busy, duration_intervals)

    # Filter by user's availability window
    if request['available_times']:
        available_slots = filter_by_availability_window(
            available_slots,
            request['available_times']['start'],
            request['available_times']['end']
        )

    # Select earliest slot
    selected = select_earliest_slot(available_slots, duration_intervals)

    if selected:
        start_intervals, end_intervals = selected
        start_hour, start_min = minutes_to_time(start_intervals * 15)
        end_hour, end_min = minutes_to_time(end_intervals * 15)
        return {
            'start': (start_hour, start_min),
            'end': (end_hour, end_min),
            'success': True
        }

    return {'success': False, 'reason': 'No available slots'}
```

## Advanced: Priority-Based Scheduling
```python
def schedule_multiple_meetings(calendar_events, requests, priority_fn=None):
    """
    Schedule multiple meetings, resolving conflicts with priority function

    priority_fn: function that returns numeric priority (higher = more important)
    """
    # Sort by priority
    if priority_fn:
        requests = sorted(requests, key=priority_fn, reverse=True)
    else:
        # Default: earlier constraint window = higher priority
        requests = sorted(
            requests,
            key=lambda r: time_to_minutes(r['available_times']['end'][0], r['available_times']['end'][1])
        )

    scheduled = []
    working_events = calendar_events.copy()

    for request in requests:
        slot = schedule_meeting(working_events, request)
        if slot['success']:
            # Add booked meeting to calendar
            working_events.append({
                'name': f"Meeting: {request['sender']}",
                'start_hour': slot['start'][0],
                'start_minute': slot['start'][1],
                'end_hour': slot['end'][0],
                'end_minute': slot['end'][1],
                'color': 'booked'
            })
            scheduled.append({'request': request, 'slot': slot})

    return scheduled
```

## Best Practices
1. Always work with intervals to avoid floating-point time issues
2. Store both interval indices and actual times for clarity
3. Handle timezone conversions before scheduling
4. Validate that proposed times fall within business hours
5. Log which blue blocks were overridden for transparency
6. Ensure slot duration exactly matches requirement (no partial hours unless specified)
