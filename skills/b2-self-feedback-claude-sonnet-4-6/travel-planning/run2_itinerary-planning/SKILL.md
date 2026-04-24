---
name: run2_itinerary-planning
description: Build a multi-city road-trip travel itinerary from dataset files with complete budget tracking, pet-friendly constraints, cuisine coverage, and correct JSON output format.
---

# Multi-City Road-Trip Itinerary Planning (Improved)

## Planning Checklist

### Step 1: Route and Day Assignment
- Identify origin and N destination cities
- Fetch driving distances for all pairs
- Assign city days:
  - Day 1: Origin → City 1 (driving day, ~full day)
  - Days 2..k1: City 1 exploration
  - Day k1+1: City 1 → City 2 (driving day)
  - ...
  - Last day: Last City → Origin (driving day, no accommodation needed)

### Step 2: Accommodation Selection
**Filters (all must pass):**
1. `city` column matches target city (case-insensitive, exact city name)
2. `house_rules` does NOT contain "No pets"
3. `maximum occupancy` >= number of travelers
4. `minimum nights` <= number of nights planned

**Sort preference:** Higher review rate, lower price.

### Step 3: Restaurant Selection
- Use `Cuisines` column to match preferred cuisine types
- Spread cuisine variety across days (American, Mediterranean, Chinese, Italian)
- Avoid assigning restaurants from wrong city
- Different restaurants per meal where possible

### Step 4: Budget Calculation
```
total_cost = 0
for each city:
    total_cost += accommodation.price * nights_in_city

for each meal (not "-"):
    total_cost += restaurant.avg_cost * num_travelers

assert total_cost <= budget
```

### Step 5: Attraction Selection
- Use `attractions.csv` with exact city match
- List multiple attractions on exploration days
- Use `"-"` for driving-only days (unless short drive arrives early)

## JSON Output Format Rules

```json
{
  "plan": [
    {
      "day": 1,
      "current_city": "from Minneapolis to Cleveland",
      "transportation": "Self-driving: from Minneapolis to Cleveland, 11 hours 14 mins, 1,219 km",
      "breakfast": "Restaurant Name, City",
      "lunch": "-",
      "dinner": "Restaurant Name, City",
      "attraction": "-",
      "accommodation": "Accommodation NAME, City"
    }
  ],
  "data_sources": [...]
}
```

**Field rules:**
- `current_city`: `"from A to B"` on transit days; city name on stay days
- `transportation`: `"Self-driving: from A to B, DURATION, DISTANCE"` on transit days; `"-"` on stay days
- `attraction`: semicolon-separated ending with `;`; `"-"` on full driving days
- `accommodation`: `"NAME, City"` using exact NAME from CSV; `"-"` on final return day
- Meal fields: `"Restaurant Name, City"` or `"-"` if skipped
- Lunch may be `"-"` on long driving days

## Budget Example (2 people, 7 days, $5,100, 3 Ohio cities)

| Item | Calculation | Cost |
|------|------------|------|
| Cleveland accommodation (2 nights) | 2 × $408 | $816 |
| Columbus accommodation (2 nights) | 2 × $861 | $1,722 |
| Cincinnati accommodation (2 nights) | 2 × $264 | $528 |
| Day 1 meals (2 people) | ($14+$27) × 2 | $82 |
| Day 2 meals (2 people) | ($36+$54+$80) × 2 | $340 |
| Day 3 meals (2 people) | ($25+$65+$31) × 2 | $242 |
| Day 4 meals (2 people) | ($24+$55+$70) × 2 | $298 |
| Day 5 meals (2 people) | ($86+$67+$62) × 2 | $430 |
| Day 6 meals (2 people) | ($26+$20+$93) × 2 | $278 |
| Day 7 meals (2 people) | $26 × 2 | $52 |
| **TOTAL** | | **$4,788** |

Budget remaining: $312 (within $5,100 budget ✓)

## Cuisine Coverage Table
Track coverage to ensure each preferred cuisine appears multiple times:

| Cuisine | Meals |
|---------|-------|
| American | Day2-lunch, Day4-breakfast, Day5-breakfast, Day6-breakfast, Day7-breakfast |
| Mediterranean | Day1-breakfast, Day2-breakfast, Day3-lunch, Day5-dinner |
| Chinese | Day3-breakfast, Day4-lunch, Day5-lunch, Day6-dinner |
| Italian | Day1-dinner, Day2-dinner, Day3-dinner, Day4-dinner, Day6-lunch |
