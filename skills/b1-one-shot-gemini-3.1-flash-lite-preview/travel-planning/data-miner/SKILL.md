---
name: data-miner
description: Provides methods to search, parse, and filter local CSV files in /app/data/.
---
# Data Mining Skill

This skill explains how to extract information from the provided local datasets.

## Strategy
1. **Locate Files:** Use `grep_search` or standard `ls` in `/app/data/` to find relevant files.
2. **Read Content:** Use `read_file` to inspect the structure of CSV files (`restaurants`, `accommodations`, `attractions`).
3. **Filter Data:**
   - **Pet-friendly:** Search for "pet" or "dog" in the accommodations CSV.
   - **Cuisine:** Use `grep_search` to find "American", "Mediterranean", "Chinese", or "Italian" in `restaurants`.
   - **Location:** Search for Ohio cities using the provided `citySet.txt` as a reference.
4. **Distance Matrix:** Use `googleDistanceMatrix/distance.csv` to plan travel between Ohio cities.
