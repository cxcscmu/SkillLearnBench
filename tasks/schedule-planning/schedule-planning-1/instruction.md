You need to read meeting schedule request emails from `/root/test_input.json`. You should parse your internal calendar `/root/calendar.pdf` to propose a meeting time for all requests. The time between two adjacent horizontal lines in the calendar is 15 minutes.

## Workflow
1. Extract Request Details: From each email in `/root/test_input.json`, extract the meeting duration and any specific time/date constraints mentioned in the message body.
2. Access and read `/root/calendar.pdf`. Extract any existing appointments listed in this document. Determine the start and end times for each appointment block by measuring its position and span relative to the calendar's timeline axis.
3. Specifically identify blue-colored blocks, which represent low-priority or flexible tasks. Treat these blue slots as available time that can be overwritten; if a meeting request overlaps with a blue-colored entry, prioritize the meeting and consider the slot open. Ensure that the earliest compatible time is selected, provided that all requests can be accommodated.
4. Generate the reply content and save as a .txt file:
For each email, instead of sending a reply, generate the content based on the template below and save it as an individual text file (e.g., `/root/reply_{messageID}.txt`):

    """Hi,

        Thank you for your meeting request.

        I can be available:

        Date: {day_name}, {date_formatted}
        Time: {time_range}
        Duration: {meetingDuration} hour(s)

        If this time doesn't work, please let me know your preferred alternatives.

        Best regards,
        ConSkillBench"""

   - The date format should be `{day_name}, {month} {DD}, {YYYY}`. For example: `Thursday, January 08, 2026` (NOT `January 8th, 2026` or `January 8, 2026`)
   - The time format should be `{HH:MM AM/PM} - {HH:MM AM/PM}`. For example: `09:00 AM - 10:30 AM` (NOT `9:00 AM - 10:30 AM`)
   - All the time should be set according to the time zone in the calendar.
5. Save the results in results.json:
Log the filenames of all generated text files in `/root/results.json` using the following format:
{
  "sent_results": [
    {"filename": "reply_{messageID1}.txt", "recipient": <email of recipient1>},
    {"filename": "reply_{messageID2}.txt", "recipient": <email of recipient2>}
  ]
}