---
name: run2_itinerary-planning
description: Plan multi-city driving itineraries with proper day allocation, cuisine variety, and format compliance.
---

# Itinerary Planning (Improved)

## Route Selection for Ohio Trip from Minneapolis
Best 3-city combinations considering drive times:
- Cleveland + Dayton + Cincinnati: Good loop, varied distances
- Cleveland + Columbus + Cincinnati: Major cities, good attractions
- Route: Minneapolis → City1 → City2 → City3 → Minneapolis

## Day Allocation Strategy
- Day 1: Long drive to first Ohio city (skip breakfast/lunch or eat before departure)
- Days 2-6: Explore cities, with short travel days between cities
- Day 7: Long drive back to Minneapolis (breakfast only, skip lunch/dinner)
- Allocate 2 days per city (1 travel + 1 full day, or 2 full days)

## Output Format Requirements
- `current_city`: exact city name OR "from CityA to CityB"
- `transportation`: "Self-driving: from CityA to CityB, duration" or "-"
- Meals: "Restaurant Name, City" format; use "-" for skipped meals
- `attraction`: semicolon-separated, MUST end with semicolon; use "-" if none
- `accommodation`: "Accommodation Name, City" or "-" on last day

## Cuisine Distribution
Ensure all 4 requested cuisines appear:
- American: at least 2-3 meals
- Mediterranean: at least 2-3 meals
- Chinese: at least 2-3 meals
- Italian: at least 2-3 meals

## Budget Calculation
Total = Σ(accommodation price × nights) + Σ(restaurant avg cost × 2 people)
Must stay under $5,100.
