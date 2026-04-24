---
name: timezone-conversion
description: Convert meeting availability times between different timezones (e.g. PST to EST). Use when a meeting request specifies availability in a timezone different from the calendar's timezone.
---

# Timezone Conversion Skill

## Common Offsets (Standard Time)
- EST (Eastern Standard Time) = UTC-5
- PST (Pacific Standard Time) = UTC-8
- CST (Central Standard Time) = UTC-6
- MST (Mountain Standard Time) = UTC-7

## Common Offsets (Daylight Saving Time)
- EDT = UTC-4
- PDT = UTC-7

## March 2026 Note
In March 2026, Daylight Saving Time begins on March 8 for the US.
- After March 8: Eastern = EDT (UTC-4), Pacific = PDT (UTC-7)
- Difference: EDT is 3 hours AHEAD of PDT

## Converting PST/PDT to EST/EDT

For dates after March 8 (DST active):
- PDT to EDT: add 3 hours
- Example: 1:00 PM PDT = 4:00 PM EDT
- Example: 5:00 PM PDT = 8:00 PM EDT

## Workflow
1. Identify the timezone in the meeting request
2. Identify the calendar's timezone
3. Apply the correct offset based on DST status for the date
4. Convert the availability window before finding slots
