---
name: run2_budget-validation
description: Validate travel budget calculations including accommodation nights, meal costs, and constraint compliance.
---

# Budget Validation

## Accommodation Costs
For each city stay:
- Verify minimum_nights <= planned stay
- Verify maximum_occupancy >= 2 (for couple)
- Verify no "No pets" in house_rules
- Cost = price_per_night × number_of_nights

## Meal Costs
- Average Cost in database is per person
- For 2 travelers: meal_cost = avg_cost × 2
- Count all non-"-" meals

## Validation Checklist
1. Total accommodation + meals <= $5,100
2. All 7 days accounted for (March 17-23, 2022)
3. No flights used
4. Pet-friendly accommodations only
5. All 4 cuisine types represented (American, Mediterranean, Chinese, Italian)
6. All entities exist in the database with correct city
7. Attractions end with semicolon
8. Last day accommodation can be "-" (returning home)

## Sample Budget for Cleveland-Dayton-Cincinnati Route
- Cleveland 2 nights: ~$400-600/night
- Dayton 2 nights: ~$400-500/night
- Cincinnati 2 nights: ~$250-300/night
- 15-17 meals × $30-80 avg × 2 people = ~$900-2,700
- Target: keep total under $5,100
