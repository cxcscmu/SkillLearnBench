---
name: calendar-parser
description: Extract appointments from calendar.pdf. Use whenever you need to determine availability from the calendar.
---
# Calendar Parser Skill

This skill provides instructions on how to parse `/root/calendar.pdf` to identify available time slots.

## Steps to identify availability
1. Read `/root/calendar.pdf`.
2. Measure the vertical position and span of each appointment block.
3. The calendar timeline axis has horizontal lines separating 15-minute intervals.
4. Blue-colored blocks are flexible/low-priority and can be treated as free time.
5. Create a list of busy and free slots based on the visual blocks.
6. When a request overlaps with a blue block, treat it as available.
