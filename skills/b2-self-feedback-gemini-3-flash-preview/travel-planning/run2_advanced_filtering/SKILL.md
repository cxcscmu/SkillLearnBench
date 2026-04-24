---
name: run2_advanced_filtering
description: Advanced filtering for pet-friendly and cuisine-specific travel data.
---

# Advanced Filtering for Travel Data

Utilize regular expressions and multi-step filtering for more precise results.

## Filtering Pet-Friendly Lodging
Search for "pet-friendly" or "dog-friendly" in `NAME` and `house_rules`. Use `grep -v "No pets"` to exclude non-pet-friendly locations.

```bash
grep -i "pet" data/accommodations/clean_accommodations_2022.csv | grep -v -i "No pets"
```

## Selecting Cuisines
Combine city and cuisine searches with `grep -E` for more comprehensive results across American, Mediterranean, Chinese, and Italian types.

```bash
grep "Cleveland" data/restaurants/clean_restaurant_2022.csv | grep -E "American|Mediterranean|Chinese|Italian"
```
