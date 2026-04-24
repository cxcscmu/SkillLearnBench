---
name: generate_formatted_replies
description: Generate meeting confirmation text files based on a specific template and save the results in a JSON log.
---

1. For each scheduled meeting, format the date and time strings with strict adherence to zero-padding:
   - **Date Format**: `Day, Month DD, YYYY` (e.g., `Thursday, January 08, 2026`). Use `%A, %B %d, %Y`. Ensure the day of the month is two digits.
   - **Time Format**: `HH:MM AM/PM - HH:MM AM/PM` (e.g., `09:00 AM - 10:30 AM`). Use `%I:%M %p`. Ensure the hour is two digits (padded with 0).
2. **Template Fidelity**: Create the content for `/root/reply_{messageID}.txt` using the exact whitespace and indentation shown below:
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
3. Save each generated string as a separate `.txt` file named `/root/reply_{messageID}.txt`.
4. After processing all requests, create a `/root/results.json` file following this exact structure:
```json
{
  "sent_results": [
    {"filename": "reply_{messageID1}.txt", "recipient": "email1@example.com"},
    {"filename": "reply_{messageID2}.txt", "recipient": "email2@example.com"}
  ]
}
```