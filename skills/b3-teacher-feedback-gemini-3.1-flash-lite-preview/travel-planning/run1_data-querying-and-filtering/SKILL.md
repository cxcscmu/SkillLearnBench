---
name: data-querying-and-filtering
description: Instructions for querying the provided datasets to ensure constraints regarding pet-friendly lodging, specific cuisines, and valid locations are met.
---
### Querying Protocol
1. **Pet-Friendly Lodging:** Filter `accommodations/clean_accommodations_2022.csv` for records tagged as "pet-friendly" within the chosen Ohio cities.
2. **Restaurant Selection:** Filter `restaurants/clean_restaurant_2022.csv` to find American, Mediterranean, Chinese, and Italian options in the target cities.
3. **Attractions:** Cross-reference `attractions/attractions.csv` with the city coordinates to populate daily itineraries.
4. **Validation:** Ensure all selected data sources are appended to the `data_sources` array in the final JSON output.