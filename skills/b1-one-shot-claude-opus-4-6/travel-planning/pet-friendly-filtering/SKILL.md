---
name: pet-friendly-filtering
description: Filtering accommodations for pet-friendly stays by analyzing house_rules field in accommodation data.
---

# Pet-Friendly Accommodation Filtering

## How It Works
The `house_rules` column in `clean_accommodations_2022.csv` contains rules separated by " & ".
Common rules: "No pets", "No smoking", "No parties", "No children under 10", "No visitors".

## Filtering Logic
- **Pet-friendly**: Any accommodation where `house_rules` does NOT contain "No pets"
- An empty `house_rules` field means no restrictions — pets are allowed
- Rules like "No smoking" or "No parties" do NOT exclude pets

## Command
```bash
grep -i "cityname" data/accommodations/clean_accommodations_2022.csv | grep -iv "no pets"
```

## Additional Checks
- Verify `maximum occupancy >= number of travelers`
- Verify `minimum nights <= planned stay length`
- Consider `room type`: "Entire home/apt" is generally better for pets than "Shared room"
