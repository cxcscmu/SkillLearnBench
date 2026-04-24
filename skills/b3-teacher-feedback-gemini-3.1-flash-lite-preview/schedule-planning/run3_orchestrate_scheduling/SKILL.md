---
name: orchestrate_scheduling
description: Resolves scheduling conflicts between email requests and calendar availability, prioritizing meeting requests over blue (flexible) blocks.
---

1. **Availability Modeling**: Create a timeline representing the working day. Mark all "busy" blocks (from `pdf_calendar_parser`) as `unavailable`.
2. **Constraint Resolution**: 
    - Sort meeting requests by priority or chronologically.
    - For each request:
        - Check for gaps of duration >= `meeting_duration`.
        - Treat "blue/flexible" blocks as `available` space.
        - Check for overlaps with "busy" blocks.
    - Use a greedy algorithm to assign the earliest available slot that satisfies the `meeting_duration` and recipient constraints.
3. **Output Generation**: 
    - Format dates as `{day_name}, {month} {DD}, {YYYY}` and times as `{HH:MM AM/PM} - {HH:MM AM/PM}`.
    - Generate `/root/reply_{messageID}.txt` using the required template.
    - Compile a list of successfully scheduled requests for `results.json` in the specified format.