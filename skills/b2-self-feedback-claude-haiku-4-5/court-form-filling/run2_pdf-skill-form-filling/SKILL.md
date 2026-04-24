---
name: run2_pdf-skill-form-filling
description: Fill PDF forms using the PDF skill's form-filling scripts and workflow
---

# Filling PDF Forms with the PDF Skill

## Overview
The PDF skill provides specialized Python scripts for filling PDF forms that have fillable form fields. This is the recommended approach for working with AcroForm PDFs.

## Prerequisite Check
Before attempting to fill a form, verify the PDF has fillable fields:
```bash
python3 scripts/check_fillable_fields.py <pdf_file>
```
- If output is "This PDF has fillable form fields" → proceed with steps below
- If output is "This PDF does not have fillable form fields" → use annotation-based approach instead

## Workflow for Fillable Forms

### Step 1: Extract Form Field Information
Extract all form fields and their metadata:
```bash
python3 scripts/extract_form_field_info.py <input.pdf> <output_field_info.json>
```

This creates a JSON file with all fields including:
- `field_id`: Unique identifier for the field (use this in field_values.json)
- `type`: "text", "checkbox", "radio_group", or "choice"
- `page`: Page number (1-based)
- `rect`: Bounding box [left, bottom, right, top] in PDF coordinates
- For checkboxes: `checked_value` and `unchecked_value`
- For radio groups/choices: `radio_options` or `choice_options` with values

### Step 2: Create field_values.json
Create a JSON file with values for each field to fill:

```json
[
  {
    "field_id": "SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName1[0]",
    "description": "Plaintiff's name",
    "page": 2,
    "value": "John Smith"
  },
  {
    "field_id": "SomeCheckboxField",
    "description": "Agreement checkbox",
    "page": 1,
    "value": "/1"  // Use the "checked_value" from field_info for checked checkboxes
  },
  {
    "field_id": "RadioGroupField",
    "description": "Choose option",
    "page": 1,
    "value": "/Yes"  // Use one of the "value" entries from radio_options
  }
]
```

**Key Rules:**
- `field_id`: Must match exactly from field_info.json (case-sensitive)
- `value`: For text fields, use a string; for checkboxes/radio, use the `checked_value` or option `value`
- `page`: Must match the page number in field_info.json
- `description`: Optional, but helpful for documentation

### Step 3: Fill the Form
Run the fill script to create the filled PDF:
```bash
python3 scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>
```

The script will:
- Verify all field_ids and values are valid
- Print error messages if there are issues
- Create the output PDF if successful

## Important Notes

### Field ID Matching
- Field IDs are case-sensitive and must be exact matches
- Field IDs use XPath-like notation (e.g., `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName1[0]`)
- Do not modify or abbreviate field IDs

### Value Formats
- **Text fields**: Plain strings (no special formatting needed)
- **Checkboxes**: Use the `checked_value` when you want to check; omit the field or use `unchecked_value` to leave unchecked
- **Radio buttons**: Use one of the values from the `radio_options` list
- **Dropdowns**: Use one of the values from the `choice_options` list

### Common Issues
- If script reports "Invalid field_id" → copy the exact ID from field_info.json
- If checkbox doesn't appear checked → use the correct `checked_value` (often "/1" or "/2")
- If script reports "Invalid value for field" → verify the value matches an option from field_info

### Optional Fields
- To leave a field empty, simply omit it from field_values.json
- Court-filled fields (like case number, trial date) should be left empty/omitted
- Don't include signature or date fields that the court fills in

## File Path Usage
The scripts must be run from the `/root/.claude/skills/pdf` directory or with full paths:
```bash
cd /root/.claude/skills/pdf
python3 scripts/fill_fillable_fields.py /path/to/input.pdf /path/to/field_values.json /path/to/output.pdf
```
