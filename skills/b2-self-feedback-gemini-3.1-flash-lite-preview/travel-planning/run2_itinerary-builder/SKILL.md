---
name: run2_itinerary-builder
description: "Improved itinerary builder focusing on constraint adherence, logically connecting cities, and robust JSON schema generation."
---
# Itinerary Builder Skill
Structure the itinerary as a dictionary with `plan` and `data_sources`.
Best practices:
- Logical flow: Start city -> Moving -> End City -> Moving -> Start city.
- Ensure all meal types (American, Mediterranean, Chinese, Italian) are used.
- Include all necessary datasets in `data_sources`.
