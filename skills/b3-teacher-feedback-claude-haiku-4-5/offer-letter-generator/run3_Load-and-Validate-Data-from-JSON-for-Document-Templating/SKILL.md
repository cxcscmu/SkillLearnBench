---
name: Load and Validate Data from JSON for Document Templating
description: Use this skill to read employee/candidate data from a JSON file and validate that all required fields exist before attempting document generation. This prevents placeholder errors caused by missing data.
---

## Algorithm

```
def load_employee_data(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    required_fields = [
        'CANDIDATE_FULL_NAME', 'POSITION', 'START_DATE',
        'SALARY', 'BENEFITS', 'RELOCATION_PACKAGE'
    ]
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    return data
```

## Validation Checks

- Verify all keys match placeholder names exactly (case-sensitive)
- Check that `RELOCATION_PACKAGE` is either "Yes" or "No"
- Ensure salary and date values are in expected formats
- Raise descriptive errors for missing fields

## Return Format

Return a dictionary where keys match placeholder names and values are the data to insert.