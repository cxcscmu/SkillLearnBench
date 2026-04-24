---
name: itinerary-validation-check
description: A final verification step to ensure the JSON output meets all structural and constraint requirements before delivery.
---

1. **Day Count Verification**: Ensure the `plan` array contains exactly 7 objects representing Day 1 to Day 7.
2. **Attraction Field Validation**: 
    - Iterate through every day object. 
    - Verify that the `attraction` string is not empty ("").
    - Verify that the `attraction` string is not a null-placeholder ("-").
    - Confirm the trailing semicolon format.
3. **Constraint Check**:
    - Confirm `transportation` never mentions "flight" or "plane".
    - Confirm `accommodation` is sourced from the database and is pet-friendly.
    - Confirm `data_sources` lists all files accessed (e.g., distance matrix, restaurant csv, etc.).
4. **City Consistency**: Ensure that if the `current_city` is "from A to B", the restaurants and attractions for that day are located in A, B, or a city on the path between them.
5. **Budget Check**: Sum the estimated costs of restaurants and accommodations (if price data is available in the CSV) to ensure the total is within the $5,100 limit.