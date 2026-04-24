---
name: Data Processing and JSON Serialization
description: Used to transform raw GitHub CLI output into the required reporting structure, ensuring data integrity and correct typing.
---

When processing the data, implement the following logic:

1. **Time-to-Merge Calculation:** 
   - Filter for items where `mergedAt` is not null.
   - Use `jq` to compute the difference between `createdAt` and `mergedAt` in seconds, divide by `86400`, and calculate the average. 
   - Apply `round` or `map` to ensure the float has one decimal place.
2. **Bug Report Filtering:**
   - Use `any` or `contains` within `jq` to filter labels: `any(.labels[]; .name | contains("bug"))`.
3. **Empty State Handling:**
   - Use the `//` coalesce operator in `jq` to default empty values to `0` or `null` to ensure the `report.json` structure remains strictly valid even if no data exists for a category.
4. **Validation:**
   - Pipe the final result through `jq '.'` to verify that the generated JSON matches the required schema before writing to `/app/report.json`.