---
name: run2_itinerary_logic
description: Plan 7-day itineraries with logical city transitions and transport.
---

# Logical Itinerary Planning

When building a 7-day itinerary, it's essential to account for travel time and logical city transitions.

## City Transitions
- Use "from A to B" for `current_city` when traveling between locations.
- Ensure the `transportation` field matches the travel mode (e.g., "Self-driving").
- Consider travel duration (from `distance.csv`) when planning the day's activities.

## Activity Distribution
- Distribute attractions across cities to avoid overcrowding a single day.
- Ensure breakfast, lunch, and dinner are in the appropriate cities based on the travel schedule.
- Use "-" for meals that are skipped or not applicable (e.g., breakfast on a travel day if starting late).
