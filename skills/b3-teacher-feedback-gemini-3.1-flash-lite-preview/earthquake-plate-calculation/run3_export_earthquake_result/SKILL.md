---
name: export_earthquake_result
description: Format and save the identified earthquake data as a JSON file.
---
Extract the required attributes from the identified earthquake record and write to `/root/answer.json`:

1. Extract: `id`, `place`, `time`, `magnitude`, `latitude`, `longitude`, and the calculated `distance_km`.
2. Format the `time` field to ISO 8601 (YYYY-MM-DDTHH:MM:SSZ).
3. Construct a dictionary with these fields and save it using the `json` module to ensure valid JSON structure.