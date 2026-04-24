---
name: itinerary-planning
description: Use this skill to build a multi-day travel itinerary from structured requirements (origin, cities, dates, budget, constraints). It queries available database files and produces a day-by-day plan with transportation, meals, attractions, and accommodations.
---

# Itinerary Planning Skill

## Step 1: Parse Requirements
Extract the following from the user's request:
- **Origin city** (e.g., Minneapolis)
- **Destination cities** (e.g., three Ohio cities)
- **Travel dates** (start date → end date, total days)
- **Number of travelers**
- **Budget** (total, in USD)
- **Constraints**: no flights, pet-friendly, cuisine preferences, etc.

## Step 2: Select Cities and Routing
- Query `background/citySet_with_states.txt` to confirm valid Ohio cities (e.g., Cleveland, Columbus, Cincinnati).
- Query `googleDistanceMatrix/distance.csv` to find driving distances and durations between Minneapolis and each Ohio city, and between Ohio cities.
- Choose a logical driving route that minimizes total driving time and fits within 7 days.
- Assign driving days (typically Day 1 and one or two mid-trip transition days).

## Step 3: Assign Daily Structure
For each of the 7 days, assign:
- `current_city`: use `"from A to B"` format on driving days
- `transportation`: `"Self-driving: from A to B"` on driving days; `"-"` on stay days
- `breakfast`, `lunch`, `dinner`: select from `restaurants/clean_restaurant_2022.csv` filtered by city and preferred cuisines
- `attraction`: **Always assign at least one attraction per day, including Day 1 and all other travel/driving days.** On driving days, include a stop en route or an attraction at the destination city upon arrival. Never leave attraction as `"-"` or empty.
- `accommodation`: select from `accommodations/clean_accommodations_2022.csv` filtered by city and pet-friendly flag; use `"-"` only on the final departure day if the traveler returns home

### Day 1 Special Rule
Day 1 is a driving day from the origin to the first destination city. It **must still contain at least one attraction** — either a notable stop along the driving route, or an attraction visited upon arriving at the destination city. Do not leave Day 1 attraction empty.

## Step 4: Budget Tracking
Estimate costs across all 7 days:
- **Transportation**: use distance × per-mile cost estimate (~$0.18/mile for self-driving)
- **Accommodation**: nightly rate × nights from the accommodations dataset
- **Meals**: average meal cost × number of meals × 2 travelers
- **Attractions**: entry fees where applicable
- Confirm total ≤ stated budget (e.g., $5,100)

## Step 5: Pet-Friendly Filter
- All accommodations must be flagged as pet-friendly in the dataset.
- Do not select any hotel/motel without confirmed pet-friendly status.

## Step 6: Output
Produce a valid JSON object matching the required output schema (see task Output Format).