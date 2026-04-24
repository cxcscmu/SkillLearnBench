---
name: ground-transport-route-logic
description: Logic for planning itineraries that rely on ground transportation (driving) rather than flights, ensuring travel feasibility and daily activity engagement.
---

1. **Travel Feasibility**: Use `googleDistanceMatrix/distance.csv` to calculate travel times between cities. Since flights are prohibited, all transitions must be labeled as "Self-driving: from [City A] to [City B]".
2. **Activity Loading**: Even on heavy travel days (e.g., driving from Minneapolis to Ohio), you must schedule at least one attraction. 
3. **Transit Attractions**: If a drive consumes most of the day, populate the `attraction` field by:
    - Selecting an attraction in the departure city before leaving.
    - Selecting an attraction in a transit city found along the route in the database.
    - Selecting a short-duration attraction in the destination city upon arrival.
4. **Minimum Activity Threshold**: Never allow a day to have zero attractions or a value of "-". Every day of the 7-day plan must include at least one point of interest.
5. **Route Continuity**: Ensure the `current_city` reflects the movement (e.g., "from Minneapolis to Cleveland") and the `accommodation` for that night is located in the arrival city.