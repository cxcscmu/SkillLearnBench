---
name: run2_data-analysis
description: "Improved data querying skill for finding pet-friendly accommodations and specific restaurant cuisines in a given city."
---
# Data Analysis Skill
Use pandas to filter CSV files in `/app/data/`.
Refined filtering:
- For pet-friendly: Filter rows where `house_rules` does NOT contain "No pets".
- For restaurants: Filter by `City` AND by checking `Cuisines` column using string matching.
