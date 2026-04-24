---
name: itinerary-generator
description: Handles the structural requirements and formatting of the 7-day travel itinerary JSON.
---
# Itinerary Generator Skill

This skill provides a template for constructing the 7-day itinerary JSON.

## Structure
Ensure the output JSON at `/app/output/itinerary.json` contains:
- `plan`: Array of 7 objects (days 1-7).
- `data_sources`: List of files used from the `/app/data/` directory.

## Fields per Day
- `day` (int)
- `current_city` (string)
- `transportation` (string, no flights)
- `breakfast`, `lunch`, `dinner` (string, or "-")
- `attraction` (string, list separated by ;)
- `accommodation` (string, pet-friendly)
