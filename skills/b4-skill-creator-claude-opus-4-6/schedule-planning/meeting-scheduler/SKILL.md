---
name: meeting-scheduler
description: Schedule meetings by matching email requests against calendar availability. Use this skill when processing meeting request emails, finding optimal meeting times, or generating meeting reply templates. Triggers on phrases like "schedule a meeting", "find a time", "propose meeting slots".
---

# Meeting Scheduler Skill

## Purpose
Process meeting request emails, match against calendar availability, and generate formatted reply files.

## Workflow

### 1. Extract Request Details
From each email, extract:
- **Duration**: e.g., "one-hour", "1.5 hour", "45-minute"
- **Date constraint**: specific date requested
- **Time window**: sender's available range (e.g., "10:00am to 2:00pm")
- **Timezone**: if sender specifies a timezone (e.g., PST), convert to calendar timezone

### 2. Timezone Conversion
- Calendar timezone is the reference (e.g., Eastern Time)
- PST to ET: add 3 hours
- CST to ET: add 1 hour
- MST to ET: add 2 hours
- All reply times must be in the calendar's timezone

### 3. Scheduling Algorithm
- For each request, find the **earliest** available slot that fits the duration within the sender's time window
- **Global constraint**: ensure all scheduled meetings are compatible (no overlaps)
- If two requests compete for the same slot, schedule the one whose earliest possible start is earlier first, then shift the other to the next available slot
- Blue/flexible calendar blocks can be overwritten by meeting requests

### 4. Reply File Format
Save each reply as `/root/reply_{messageID}.txt`:

```
Hi,

    Thank you for your meeting request.

    I can be available:

    Date: {day_name}, {month} {DD}, {YYYY}
    Time: {HH:MM AM/PM} - {HH:MM AM/PM}
    Duration: {N} hour(s)

    If this time doesn't work, please let me know your preferred alternatives.

    Best regards,
    ConSkillBench
```

### Formatting Rules
- Date: `{day_name}, {month} {DD}, {YYYY}` — e.g., `Thursday, January 08, 2026` (zero-padded day)
- Time: `{HH:MM AM/PM} - {HH:MM AM/PM}` — e.g., `09:00 AM - 10:30 AM` (zero-padded hour)
- Duration: use decimal for partial hours (e.g., "1.5 hour(s)", "0.75 hour(s)")

### 5. Results File
Save `/root/results.json`:
```json
{
  "sent_results": [
    {"filename": "reply_{id}.txt", "recipient": "email@example.com"}
  ]
}
```
