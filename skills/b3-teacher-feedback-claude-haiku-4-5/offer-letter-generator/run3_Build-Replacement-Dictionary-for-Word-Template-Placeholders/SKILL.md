---
name: Build Replacement Dictionary for Word Template Placeholders
description: Use this skill to create the regex patterns and replacement values needed to fill placeholders in a Word template. Organize patterns for easy iteration and ensure proper escaping.
---

## Algorithm

```
def build_replacement_dict(employee_data):
    return {
        r'{{CANDIDATE_FULL_NAME}}': employee_data['CANDIDATE_FULL_NAME'],
        r'{{POSITION}}': employee_data['POSITION'],
        r'{{START_DATE}}': employee_data['START_DATE'],
        r'{{SALARY}}': employee_data['SALARY'],
        r'{{BENEFITS}}': employee_data['BENEFITS'],
    }
```

## Key Details

- Use raw strings (`r'...'`) for regex patterns
- Patterns should match placeholder text exactly, including braces
- Do not include conditional placeholders (`IF_*`, `END_IF_*`) here—handle those separately
- Return a dictionary for easy iteration in replacement loops