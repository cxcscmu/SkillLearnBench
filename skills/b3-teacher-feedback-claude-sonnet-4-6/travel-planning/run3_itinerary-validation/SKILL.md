---
name: itinerary-validation
description: Use this skill to validate a completed itinerary JSON against all task requirements before finalizing output. Run this checklist after formatting and before writing the file.
---

# Itinerary Validation Checklist

Run every check below. If any check fails, revise the itinerary before writing the output file.

## Structure Checks
- ✅ `plan` array contains exactly 7 day objects
- ✅ `day` values are integers 1 through 7 with no gaps or duplicates
- ✅ `data_sources` array is present and lists all files actually queried

## Travel Checks
- ✅ No flights used anywhere in the plan (all transportation is self-driving or `"-"`)
- ✅ Driving days use `"from A to B"` format in `current_city`
- ✅ Driving days use `"Self-driving: from A to B"` in `transportation`
- ✅ Stay days use `"-"` in `transportation`
- ✅ Route is logically ordered (origin → city 1 → city 2 → city 3 → return or similar)

## City Checks
- ✅ Exactly three Ohio cities are covered
- ✅ All cities confirmed as valid in `background/citySet_with_states.txt`
- ✅ Origin city is Minneapolis

## Date and Duration Checks
- ✅ Plan spans March 17–23, 2022 (7 days)

## Accommodation Checks
- ✅ All accommodations are confirmed pet-friendly from the dataset
- ✅ No accommodation is `"-"` except on the final return-home day (if applicable)

## Meal Checks
- ✅ At least one meal per day is assigned (not all three are `"-"`)
- ✅ Cuisine preferences (American, Mediterranean, Chinese, Italian) appear across the plan
- ✅ All restaurants are sourced from `restaurants/clean_restaurant_2022.csv` for the correct city

## Attraction Checks — CRITICAL
- ✅ **Day 1 attraction is not empty or `"-"`** ← Day 1 is the most commonly missed; verify explicitly
- ✅ Every day (Days 1–7) has a non-empty, non-`"-"` attraction string
- ✅ Every attraction string ends with `;`
- ✅ Attractions are sourced from `attractions/attractions.csv` for the correct city
- ✅ No day uses `"-"` for attraction, even if it is a driving/travel day

## Budget Check
- ✅ Total estimated cost ≤ $5,100 for two travelers
- ✅ Budget breakdown covers: driving costs, accommodation, meals, and attraction entry fees

## Final Output Check
- ✅ JSON is valid (no syntax errors)
- ✅ File written to `/app/output/itinerary.json`