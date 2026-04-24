---
name: scheduling-engine
description: Algorithm to find earliest available meeting slots given constraints and existing appointments.
---

# Scheduling Engine

This skill manages the logic for finding the earliest possible time slot for a meeting, accounting for both hard and soft (low-priority) conflicts.

## Key Logic
- Represent the day's schedule as a list of occupied and flexible (low-priority) blocks.
- Filter the schedule based on meeting constraints (start time, end time, duration).
- Consider 'blue' blocks as open slots that can be overwritten.

## Example Python logic for overlapping checks

```python
from datetime import datetime, timedelta

def find_earliest_slot(requests, schedule, blue_blocks):
    """
    requests: List of (duration_hrs, constraint_start, constraint_end)
    schedule: List of occupied (start, end)
    blue_blocks: List of low-priority (start, end)
    """
    # 1. Open up blue blocks
    # Effective occupied schedule: schedule minus any block in blue_blocks.
    
    # 2. Iterate through candidate start times (e.g., every 15 mins)
    # Check if a candidate start_time + duration fits within constraints.
    # Check if candidate window (start, end) overlaps with any occupied block.
```

## Important Considerations
- Handle multiple requests (though the task is to propose a meeting for all requests, typically it means finding a slot for each one independently while trying to fit all if possible - although the workflow says "propose a meeting time for all requests").
- Ensure that the earliest compatible time is selected.
- Date/Time formatting for output is critical.
