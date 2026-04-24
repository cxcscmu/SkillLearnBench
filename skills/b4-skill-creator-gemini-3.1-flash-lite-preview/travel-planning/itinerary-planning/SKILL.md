---
name: itinerary-planning
description: How to construct a 7-day, pet-friendly travel itinerary for three Ohio cities starting from Minneapolis without using flights. Use this skill for planning, organizing the itinerary data, and formatting the final JSON output.
---
# Itinerary Planning Skill

## Overview
This skill outlines the process for building a 7-day, non-flight travel itinerary across three cities in Ohio, starting from Minneapolis.

## Planning Steps
1. **Identify Cities:** Select three cities in Ohio from `data/background/citySet.txt` or `citySet_with_states.txt`.
2. **Timeline:** Plan the 7 days (March 17th - March 23rd, 2022).
3. **Route:** Plan the driving route from Minneapolis to the first Ohio city and between subsequent Ohio cities.
4. **Logistics:** Ensure accommodations are marked as pet-friendly (check `data/accommodations/`).
5. **Cuisine:** Plan daily meals (American, Mediterranean, Chinese, Italian).
6. **Activities:** Select attractions from `data/attractions/`.

## JSON Format
Your final output must be a single JSON object at `/app/output/itinerary.json` with:
- `plan`: Array of 7 day objects (day, current_city, transportation, breakfast, lunch, dinner, attraction, accommodation).
- `data_sources`: Array of file paths used for the plan.

## Constraints
- **NO FLIGHTS:** Use road travel only.
- **BUDGET:** Maximum $5,100.
- **PETS:** Accommodations MUST be pet-friendly.
- **DURATION:** 7 days.
- **LOCATIONS:** Three cities in Ohio.
