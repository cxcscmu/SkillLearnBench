name: itinerary-planner
description: How to construct a 7-day travel itinerary with constraints. Use this skill when organizing days, managing budget, and ensuring all user requirements (pet-friendly, cuisine, no flights) are met.

## Planning Workflow

### 1. Route Optimization
- Start from the origin (Minneapolis).
- Sequence cities to minimize backtracking and excessive driving on a single day (except for the long hauls from/to Minneapolis).
- Use `distance.csv` to validate the route.

### 2. Constraint Checklist
- **7 Days:** Ensure exactly 7 day objects in the final JSON.
- **Three Cities:** Cover the requested number of target cities.
- **Pet-Friendly:** Every accommodation MUST have a rule allowing pets.
- **Cuisines:** Incorporate preferred cuisines (American, Mediterranean, Chinese, Italian) across the meals.
- **Budget:** Keep total cost (Accommodations + Meals + Estimated Fuel) under the limit ($5,100).
  - *Fuel Estimate:* $0.15 per km (roughly).
  - *Meal Estimate:* Use `Average Cost` from restaurant data.

### 3. Output Format
- Strictly follow the JSON structure provided in the task description.
- Ensure `current_city` accurately reflects the location or the movement (e.g., "from A to B").
- `attraction` field must end with `;`.
