---
name: itinerary-budget-planning
description: Planning multi-city travel itineraries with budget constraints, route optimization, and cuisine diversity.
---

# Itinerary Budget Planning

## Route Optimization
- Choose cities that minimize total driving time
- Consider geographic clustering (e.g., Cleveland→Dayton→Cincinnati forms a logical loop)
- Start and end at the origin city for round trips

## Budget Components
1. **Accommodations**: price × nights per city
2. **Meals**: restaurant average cost × number of meals
3. **Transportation**: Self-driving costs (gas estimated from distances)

## Cuisine Diversity Strategy
- Map required cuisines (American, Mediterranean, Chinese, Italian) across meals
- Use restaurant `Cuisines` field to match — many restaurants serve multiple cuisines
- Spread different cuisines across breakfast, lunch, and dinner slots

## Accommodation Selection Criteria
- Check `maximum occupancy >= party size`
- Check `minimum nights <= planned stay duration`
- Filter by `house_rules` for specific needs (pets, children, smoking)
- Balance price vs. review rating

## Day Planning Template
- Travel days: skip meals during long drives (use "-")
- City days: 3 meals + 2-3 attractions
- Transition days: breakfast in departing city, lunch/dinner in arriving city

## Output Format
JSON with `plan` array (7 day objects) and `data_sources` array.
Each day: day, current_city, transportation, breakfast, lunch, dinner, attraction, accommodation.
