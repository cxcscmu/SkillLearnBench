---
name: json-itinerary-formatting
description: Ensures the final output strictly adheres to the requested JSON structure and field requirements.
---
### Formatting Guidelines
- The output must be saved to `/app/output/itinerary.json`.
- The `plan` array must contain exactly 7 objects (days 1 through 7).
- For travel days, use the format `"from A to B"` in the `current_city` field.
- Ensure all attractions are concatenated as a single string ending with a semicolon (e.g., `"A;B;C;"`).
- Use `"-"` for any meal fields if no restaurant is assigned for that time slot.