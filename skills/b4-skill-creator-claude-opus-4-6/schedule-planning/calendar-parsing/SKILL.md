---
name: calendar-parsing
description: Parse visual calendar PDFs to extract existing appointments with their time ranges, colors, and availability status. Use this skill whenever processing calendar images/PDFs to determine busy/free slots, even if the user just says "check my calendar" or "find available time".
---

# Calendar Parsing Skill

## Purpose
Extract structured event data from visual calendar PDFs where events are rendered as colored blocks on a timeline.

## Parsing Process

1. **Identify the timeline axis**: Read hour labels (12am-11pm) along the left edge. Each space between adjacent dashed horizontal lines represents 15 minutes.

2. **Extract metadata**: Date and timezone from the calendar header (e.g., "Mon Mar 9, 2026 (Eastern Time - New York)").

3. **Map colored blocks to events**:
   - Determine each block's start/end by its vertical position relative to hour labels
   - Read the event title text within or beside each block
   - Note the block color — this determines priority

4. **Color semantics**:
   - **Pink/Red/Salmon blocks**: Fixed appointments — cannot be moved or overwritten
   - **Blue/Purple blocks**: Low-priority/flexible tasks — treat as available; can be overwritten by meeting requests
   - **Yellow/Olive blocks**: Fixed appointments — cannot be moved
   - **Dark gray blocks**: Out of office / unavailable — hard block
   - **Green labels**: Event title labels (not a block type)

5. **Build availability map**: Combine free gaps + blue/overwritable blocks into a unified list of available time slots.

## Output Format

```
Available slots on {date} ({timezone}):
- HH:MM AM/PM - HH:MM AM/PM (duration)
```

## Edge Cases
- Blocks that appear adjacent with no visible gap: treat as back-to-back (no free time between them)
- 15-minute precision: all times should snap to 15-minute boundaries
- When timezone differs between requester and calendar, convert to calendar timezone for scheduling
