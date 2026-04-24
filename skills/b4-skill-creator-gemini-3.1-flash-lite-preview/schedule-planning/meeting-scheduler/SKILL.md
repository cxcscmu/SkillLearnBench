---
name: meeting-scheduler
description: Schedule meetings and generate response text files. Use whenever you have a meeting request to process and confirm.
---
# Meeting Scheduler Skill

This skill provides instructions on how to generate response emails and log results.

## Reply Template
Use this template for every meeting request:

Hi,

Thank you for your meeting request.

I can be available:

Date: {day_name}, {month} {DD}, {YYYY}
Time: {time_range}
Duration: {meetingDuration} hour(s)

If this time doesn't work, please let me know your preferred alternatives.

Best regards,
ConSkillBench

## Formatting Rules
- Date format: {day_name}, {Month} {DD}, {YYYY} (e.g., Thursday, January 08, 2026)
- Time format: {HH:MM AM/PM} - {HH:MM AM/PM} (e.g., 09:00 AM - 10:30 AM)

## Result Logging
After saving the reply as `/root/reply_{messageID}.txt`, log it in `/root/results.json`:
{
  "sent_results": [
    {"filename": "reply_{messageID}.txt", "recipient": <recipient_email>}
  ]
}
