---
name: meeting-scheduler
description: Logic for finding the earliest possible meeting slot based on calendar availability and email request constraints. Use this skill whenever you need to propose a meeting time from a set of constraints and an existing schedule.
---

# Meeting Scheduler

This skill provides the logic needed to find an optimal meeting slot.

## Scheduling logic
1. **Gather Constraints**: Collect the requested duration and any date/time limitations from the email.
2. **Scan Available Slots**: Look for any empty time slots on the requested date that are long enough to accommodate the duration.
3. **Handle Flexible Slots**: If no empty slot is found, identify "blue" slots on the calendar. Treat these blue slots as available time.
4. **Earliest Time First**: Prioritize the earliest compatible time that fits all requests.
5. **Timezone awareness**: Ensure all times are consistent with the calendar's timezone.

## Conflict resolution
- **Fixed slots**: Never schedule over a non-blue appointment.
- **Blue slots**: Can be overwritten to fit a higher-priority meeting request.
- **Overlapping requests**: Ensure that multiple meeting requests are handled sequentially so they do not overlap with each other.
