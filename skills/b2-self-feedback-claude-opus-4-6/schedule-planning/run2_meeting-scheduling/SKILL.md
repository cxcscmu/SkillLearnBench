---
name: run2_meeting-scheduling
description: Schedule meetings into calendar free slots considering time constraints, timezone conversion, and blue-block overrides.
---

# Meeting Scheduling Algorithm

## Steps
1. Build free-slot list: merge gaps between non-blue events. Blue blocks become free.
2. For each email, extract: duration, date, requester's available time window, timezone.
3. Convert all times to calendar timezone.
4. For each request, compute intersection of requester window with free slots.
5. Use greedy earliest-fit: assign each meeting the earliest possible slot.
6. When multiple requests compete for the same window, try all orderings to find one where all fit with earliest possible times.

## Conflict Resolution
- If two meetings share a free window, schedule the one whose time window starts earlier first.
- If they start at the same time, schedule the longer meeting first.
- Verify no meeting is left unschedulable after assignment.

## Output Format
- Date: `{day_name}, {month} {DD}, {YYYY}` — zero-pad DD (e.g., `March 09`)
- Time: `{HH:MM AM/PM} - {HH:MM AM/PM}` — zero-pad hours (e.g., `09:00 AM`)
- Duration: express in hours (e.g., 45 min = `0.75 hour(s)`)
