---
name: calendar-scheduler
description: Logic for calculating meeting slots based on constraints and availability.
---

# Calendar Scheduler Skill
Use this skill for calculating available time slots while considering constraints and blocking out busy periods.

## Usage
1. Parse existing events from a schedule.
2. Filter for specific colors (e.g., blue as flexible).
3. Identify gaps >= requested duration.
4. Format dates as `Day_name, Month DD, YYYY` and times as `HH:MM AM/PM - HH:MM AM/PM`.
