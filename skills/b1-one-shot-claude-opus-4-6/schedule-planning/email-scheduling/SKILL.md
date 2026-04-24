---
name: email-scheduling
description: Workflow for parsing meeting request emails, matching constraints to calendar availability, and generating reply files.
---

# Email-Based Meeting Scheduling

## Workflow

### 1. Parse Email Requests
Extract from each email:
- **Duration**: e.g., "one-hour", "1.5 hour", "45-minute"
- **Date constraint**: e.g., "March 9th, 2026"
- **Time window**: e.g., "10:00am to 2:00pm", "1:00 PM and 5:00 PM PST"
- **Sender email**: from the `from_email` field

### 2. Timezone Conversion
- If the request specifies a timezone different from the calendar, convert:
  - PST to ET: add 3 hours (e.g., 1:00 PM PST = 4:00 PM ET)
  - CST to ET: add 1 hour
  - MST to ET: add 2 hours

### 3. Scheduling Strategy
- Find the **earliest** available slot that satisfies all constraints
- When multiple requests target the same day, schedule them so all can be accommodated
- Blue (low-priority) calendar blocks can be overwritten
- Never overlap with non-overwritable blocks

### 4. Reply Template Format
```
Hi,

    Thank you for your meeting request.

    I can be available:

    Date: {day_name}, {month} {DD}, {YYYY}
    Time: {HH:MM AM/PM} - {HH:MM AM/PM}
    Duration: {meetingDuration} hour(s)

    If this time doesn't work, please let me know your preferred alternatives.

    Best regards,
    ConSkillBench
```

### 5. Formatting Rules
- Date: `Monday, March 09, 2026` (zero-padded day, full month name)
- Time: `09:00 AM - 10:30 AM` (zero-padded hours, AM/PM with space)
- Duration: use "hour(s)" as unit; for 45 min use "0.75 hour(s)"
