---
name: meeting-response-generator
description: Generates reply text files and the final result log with specific formatting for date, time, and JSON. Use this skill whenever you need to provide a professional meeting proposal in a fixed format.
---

# Meeting Response Generator

This skill ensures that all proposed meeting replies and the final results log are formatted correctly.

## Date format
- **Standard**: `{day_name}, {month} {DD}, {YYYY}`
- **Example**: `Thursday, January 08, 2026` (Must use leading zero for DD and full year)

## Time format
- **Standard**: `{HH:MM AM/PM} - {HH:MM AM/PM}`
- **Example**: `09:00 AM - 10:30 AM` (Must use leading zero for HH)

## Reply text file template
For each email, create a file `reply_{messageID}.txt`:
"""Hi,

    Thank you for your meeting request.

    I can be available:

    Date: {day_name}, {date_formatted}
    Time: {time_range}
    Duration: {meetingDuration} hour(s)

    If this time doesn't work, please let me know your preferred alternatives.

    Best regards,
    ConSkillBench"""

## Results JSON format
Create `results.json`:
```json
{
  "sent_results": [
    {"filename": "reply_{messageID1}.txt", "recipient": <email of recipient1>},
    {"filename": "reply_{messageID2}.txt", "recipient": <email of recipient2>}
  ]
}
```
Ensure all `filename` and `recipient` pairs are correctly logged.
