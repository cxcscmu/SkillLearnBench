---
name: Generate Community Pulse Report JSON
description: Compile gathered PR and issue metrics into a properly formatted JSON file at /app/report.json with the exact required structure and data types.
---

# Generate Community Pulse Report JSON

## Overview
Create a report.json file in the `/app/` directory containing all gathered metrics in the specified JSON structure.

## Step 1: Structure Validation
Ensure the JSON follows this exact structure:

```json
{
  "pr": {
    "total": <integer>,
    "merged": <integer>,
    "closed": <integer>,
    "avg_merge_days": <float>,
    "top_contributor": <string>
  },
  "issue": {
    "total": <integer>,
    "bug": <integer>,
    "resolved_bugs": <integer>
  }
}
```

**Data Type Requirements:**
- `total`, `merged`, `closed`: Integers (no decimals)
- `avg_merge_days`: Float with exactly 1 decimal place (e.g., `1.2`, `15.8`)
- `top_contributor`: String (author login, e.g., `"octocat"`)
- `bug`, `resolved_bugs`: Integers

## Step 2: Data Compilation
Gather all metrics from previous steps:
- **PR metrics:** total count, merged count, closed count, average merge days, top contributor name
- **Issue metrics:** total count, bug count, resolved bug count

## Step 3: File Creation
Write the JSON object to `/app/report.json`:
- Use standard JSON formatting (valid syntax, proper escaping)
- Ensure file is readable and valid JSON (test with JSON validator)
- Verify the file path is exactly `/app/report.json`

## Step 4: Validation Checklist
Before finalizing:
- [ ] All integer fields contain integers (not floats or strings)
- [ ] `avg_merge_days` is a float with exactly 1 decimal place
- [ ] `top_contributor` is a non-empty string
- [ ] File is valid JSON (no syntax errors)
- [ ] File location is `/app/report.json`
- [ ] Numbers match expected ranges (totals not inflated, averages reasonable)

## Example Output
```json
{
  "pr": {
    "total": 45,
    "merged": 42,
    "closed": 3,
    "avg_merge_days": 1.2,
    "top_contributor": "octocat"
  },
  "issue": {
    "total": 30,
    "bug": 9,
    "resolved_bugs": 8
  }
}
```