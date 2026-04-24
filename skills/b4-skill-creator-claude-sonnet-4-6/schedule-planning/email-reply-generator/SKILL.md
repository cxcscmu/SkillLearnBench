---
name: email-reply-generator
description: Generate formatted meeting reply emails and save them as .txt files, then log results to results.json. Use when you need to respond to meeting scheduling requests with proposed time slots.
---

# Email Reply Generator Skill

## Reply Template

```
Hi,

    Thank you for your meeting request.

    I can be available:

    Date: {day_name}, {date_formatted}
    Time: {time_range}
    Duration: {meetingDuration} hour(s)

    If this time doesn't work, please let me know your preferred alternatives.

    Best regards,
    ConSkillBench
```

## Date Format Rules
- Format: `{day_name}, {month} {DD}, {YYYY}`
- Day name: Full name (Monday, Tuesday, etc.)
- Month: Full name (January, February, etc.)
- Day: Zero-padded two digits (01, 02, ..., 09, 10, ...)
- Example: `Monday, March 09, 2026` ✓
- NOT: `March 9th, 2026` ✗ or `March 9, 2026` ✗

## Time Format Rules
- Format: `{HH:MM AM/PM} - {HH:MM AM/PM}`
- Hours: Zero-padded two digits (09, 10, 11, 12, 01, ...)
- Example: `09:00 AM - 10:00 AM` ✓
- NOT: `9:00 AM - 10:00 AM` ✗

## Duration Format
- Express in hours: 1 hour meeting → `1`, 1.5 hour → `1.5`, 45 min → `0.75`
- Template says `{meetingDuration} hour(s)` — use the decimal hour value

## File Naming
- Save each reply as `/root/reply_{messageID}.txt`
- MessageIDs are assigned sequentially: 1, 2, 3, ...

## results.json Format
```json
{
  "sent_results": [
    {"filename": "reply_1.txt", "recipient": "email@example.com"},
    {"filename": "reply_2.txt", "recipient": "email2@example.com"}
  ]
}
```
Save to `/root/results.json`.
