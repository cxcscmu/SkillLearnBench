---
name: meeting-slot-scheduling
description: Find the earliest available meeting time slots that satisfy constraints. This skill implements the scheduling algorithm to match meeting requests with available calendar slots, handling blue (flexible) block overwriting, time constraints, and date preferences. Use this whenever you need to schedule a meeting or find available time slots.
---

# Meeting Slot Scheduling

## Overview

This skill finds the earliest available time slots for meeting requests by:
- Comparing meeting duration with available calendar gaps
- Handling blue-block overwriting (flexible slots can be used for meetings)
- Respecting date and time constraints
- Selecting the earliest compatible time

## Scheduling Algorithm

### Step 1: Prepare Data

Input requirements:
- **Parsed meeting requests**: duration, date constraints, time constraints
- **Extracted calendar appointments**: start time, end time, color (blue/fixed)
- **Calendar timezone**: For time calculations

### Step 2: Process Each Meeting Request

For each request:

1. **Determine applicable dates**:
   - If date constraint exists: use specified date
   - Otherwise: use current/next available date in calendar
   - If multi-day calendar: search across available dates

2. **Determine time window**:
   - If time constraint exists (e.g., "morning"): use constrained window
   - Otherwise: use full available day (e.g., 8 AM - 6 PM)

### Step 3: Find Available Slots

Scan the calendar for continuous free time:

1. **Identify gaps between appointments**:
   - Space between end of one appointment and start of next
   - Space before first appointment
   - Space after last appointment

2. **Calculate slot duration**:
   - Gap duration = gap_end - gap_start
   - Can accommodate meeting if: gap_duration ≥ meeting_duration

3. **Handle blue blocks**:
   - If gap overlaps with a blue block: treat blue time as available
   - Remove blue block from occupied time
   - Extend available slot to include blue time
   - Only if requested meeting duration fits

4. **Respect constraints**:
   - Ensure slot falls within date constraint
   - Ensure slot falls within time window constraint
   - Skip slots that violate constraints

### Step 4: Select Earliest Slot

- Scan chronologically from start of calendar
- Select the FIRST (earliest) slot that:
  - Fits meeting duration
  - Respects all constraints
  - Does not conflict with fixed appointments (non-blue)
- Return: date, start_time, end_time

### Step 5: Format Results

Return scheduled meeting data:

```json
{
  "messageID": "msg123",
  "scheduled_date": "2026-03-25",
  "scheduled_day_name": "Tuesday",
  "start_time": "10:00",
  "end_time": "11:00",
  "duration_hours": 1.0,
  "slot_type": "gap|blue_overwrite"
}
```

## Example Scenario

**Calendar state:**
- 9:00-10:00 AM: Fixed appointment (gray)
- 10:00-10:30 AM: Blue block (flexible)
- 10:30-11:30 AM: Free gap
- 11:30 AM-12:30 PM: Fixed appointment (gray)

**Request:** 1-hour meeting, no constraints

**Process:**
1. Check 8:00-9:00 AM: Only 1 hour, fits! ✓ Return 8:00-9:00 AM as earliest slot

## Edge Cases

- **Meeting longer than any gap**: Request cannot be scheduled with current constraints
- **Blue block exactly fills gap**: Can use blue block to extend available time
- **Multiple blue blocks in sequence**: Combine to create larger slot
- **Constraint makes no slots available**: Note constraint violation in response

## Integration

This algorithm is used after parsing both calendar and requests. Feed it:
1. List of extracted appointments with colors and times
2. List of parsed requests with durations and constraints

Output feeds directly into response formatting.
