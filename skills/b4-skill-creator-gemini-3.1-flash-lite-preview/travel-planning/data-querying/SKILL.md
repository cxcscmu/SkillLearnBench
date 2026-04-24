---
name: data-querying
description: How to query CSV datasets in /app/data to extract information like accommodations, attractions, and restaurants. Use this skill whenever you need to look up data from files in the /app/data directory.
---
# Data Querying Skill

## Overview
This skill provides instructions for querying CSV datasets located in the `/app/data/` directory to retrieve information for travel itineraries.

## Querying CSV Data
1. **Identify the file:** Determine the correct CSV file in `/app/data/` for the information needed (e.g., `accommodations/`, `attractions/`, `restaurants/`, `flights/`).
2. **Examine the data:** Read the header and first few lines of the CSV file to understand its structure (columns).
   - Use `read_file` with `start_line: 1` and `end_line: 5`.
3. **Filter data:** Use `grep_search` to find relevant entries, or read the file if it's small enough.
4. **Format extracted data:** Present the data in a clear, usable format.

## Best Practices
- Always verify the column names before filtering.
- Use `grep_search` for large files to avoid reading the entire file.
- Combine information from multiple sources (e.g., matching city names across different datasets).
