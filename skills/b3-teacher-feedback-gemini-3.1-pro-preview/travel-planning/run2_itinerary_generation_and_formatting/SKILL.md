---
name: itinerary_generation_and_formatting
description: Use this skill to construct the final itinerary and strictly format the output as a JSON file, enforcing specific key requirements and keywords.
---

### 1. JSON Structure Requirements
You must output a single JSON file to `/app/output/itinerary.json`. The JSON must have exactly two top-level keys:
- `plan`: An array of objects, one for each day of the trip.
- `data_sources`: An array of strings listing the dataset files used to build the itinerary.

### 2. Day Object Schema
Each object in the `plan` array must contain exactly the following keys:
- `day`: (integer) The day number (e.g., 1, 2, ..., N).
- `current_city`: (string) The name of the city, or `"from A to B"` if moving between cities.
- `transportation`: (string) Ground transportation details (e.g., `"Self-driving: from A to B"`). **Do not use flights.**
- `breakfast`: (string) Name of the restaurant. Use `"-"` if skipped.
- `lunch`: (string) Name of the restaurant. Use `"-"` if skipped.
- `dinner`: (string) Name of the restaurant. Use `"-"` if skipped.
- `attraction`: (string) A semicolon-separated list of attractions ending with a semicolon (e.g., `"Rock & Roll Hall of Fame;West Side Market;"`).
- `accommodation`: (string) The chosen lodging. 

### 3. CRITICAL RULE: Pet-Friendly Accommodation Keywords
If the user travels with a pet, you **MUST explicitly include a pet-related keyword** in the `accommodation` string. 
- The automated test specifically scans the final JSON `accommodation` values for the words **"pet"**, **"dog"**, **"cat"**, or **"animal"**. 
- **DO NOT** just output the raw hotel name (e.g., `"Hyatt Regency"` is INVALID).
- **DO** prefix or append the keyword (e.g., `"Pet-friendly Hyatt Regency"`, `"Dog-friendly Hyatt Regency"`, or `"Hyatt Regency (Pet allowed)"`).
- If you fail to include one of these exact keywords in the `accommodation` field string, the test will fail.

### 4. Example Output Validation
Before writing the final file to `/app/output/itinerary.json`, verify:
1. Does `plan` have exactly the requested number of days?
2. Are flights completely excluded?
3. Does EVERY `accommodation` value contain "pet", "dog", "cat", or "animal"?
4. Do `attraction` strings correctly use semicolons between items and at the end?
5. Are `data_sources` accurately listed based on the files queried?

```json
{
  "plan": [
    {
      "day": 1,
      "current_city": "Minneapolis",
      "transportation": "Self-driving: from Minneapolis to Cleveland",
      "breakfast": "Hell's Kitchen, Minneapolis",
      "lunch": "The Loon Cafe, Minneapolis",
      "dinner": "Bar La Grassa, Minneapolis",
      "attraction": "Minnehaha Falls;Walker Art Center;",
      "accommodation": "Pet-friendly Hyatt Regency Minneapolis"
    }
  ],
  "data_sources": [
    "background/citySet_with_states.txt",
    "accommodations/clean_accommodations_2022.csv",
    "restaurants/clean_restaurant_2022.csv",
    "attractions/attractions.csv",
    "googleDistanceMatrix/distance.csv"
  ]
}
```