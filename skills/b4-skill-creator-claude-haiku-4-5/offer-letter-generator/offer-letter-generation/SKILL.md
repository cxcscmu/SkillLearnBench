---
name: offer-letter-generation
description: Generate filled offer letters from a JSON employee data file and a Word template. Use this skill whenever you need to create offer letters by matching data fields to document placeholders, handling conditional relocation packages, and saving the final document.
---

# Offer Letter Generation

This skill demonstrates the complete workflow for generating personalized offer letters from employee data and a template.

## Workflow Overview

1. **Load employee data** from JSON
2. **Load template** Word document
3. **Map fields** from JSON to template placeholders
4. **Handle conditionals** (e.g., relocation packages)
5. **Fill template** with data
6. **Save output** document

## Data Structure

Employee data should be in JSON format with these typical fields:

```json
{
  "DOC_ID": "OFFER-2024-00847",
  "COMPANY_NAME": "Nexus Technologies Inc.",
  "CANDIDATE_FULL_NAME": "Sarah Chen",
  "POSITION": "Senior Software Engineer",
  "BASE_SALARY": "185,000",
  "RELOCATION_PACKAGE": "Yes",
  "RELOCATION_AMOUNT": "15,000",
  ...
}
```

## Placeholder Mapping

Common placeholders in offer letter templates:

| Placeholder | Data Field | Example |
|---|---|---|
| `{{CANDIDATE_FULL_NAME}}` | CANDIDATE_FULL_NAME | Sarah Chen |
| `{{POSITION}}` | POSITION | Senior Software Engineer |
| `{{COMPANY_NAME}}` | COMPANY_NAME | Nexus Technologies Inc. |
| `{{BASE_SALARY}}` | BASE_SALARY | 185,000 |
| `{{START_DATE}}` | START_DATE | February 12, 2024 |
| `{{STREET_ADDRESS}}` | STREET_ADDRESS | 456 Oak Avenue, Apt 7B |

## Conditional Sections

Offer letters often have optional sections based on employee benefits:

```
{{IF_RELOCATION_PACKAGE}}
Our company is pleased to provide a relocation package of ${{RELOCATION_AMOUNT}}
to assist with your move. You have {{RELOCATION_DAYS}} days from your start date
to complete your relocation.
{{END_IF_RELOCATION_PACKAGE}}
```

**Processing logic:**
- If `RELOCATION_PACKAGE` == "Yes": Keep the section, remove markers
- If `RELOCATION_PACKAGE` != "Yes": Remove entire section including markers

## Implementation Steps

1. **Load JSON data**
   ```python
   import json
   with open('employee_data.json') as f:
       data = json.load(f)
   ```

2. **Create mapping function**
   - Map JSON keys to placeholder names (may differ)
   - Handle boolean conversions (Yes/No to True/False)

3. **Process conditionals**
   - Identify condition name from `IF_FIELDNAME` pattern
   - Check if condition is true/false
   - Keep or remove section accordingly

4. **Fill and save**
   - Replace all placeholders
   - Save to output path

## Example Output Structure

The filled offer letter should:
- Replace all `{{FIELD}}` markers with actual values
- Either include the relocation section with clean text (no IF markers) OR exclude it entirely
- Preserve all formatting from the template
- Be saved as a valid .docx file

## Validation Checklist

After generating the offer letter:
- [ ] All placeholders replaced (no `{{` remaining)
- [ ] Conditional sections properly handled
- [ ] Document opens without errors
- [ ] Formatting is preserved
- [ ] Address block is complete
- [ ] Salary and benefits details correct
