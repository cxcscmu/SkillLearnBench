---
name: run2_pdf-form-filling
description: Complete workflow for filling fillable PDF forms using Claude Code PDF skill scripts with pypdf.
---

# Filling Fillable PDF Forms

## Prerequisites
- Python 3 with pypdf installed
- Scripts located at `/root/.claude/skills/pdf/scripts/`
- **Always run scripts from**: `cd /root/.claude/skills/pdf`

## Step-by-Step Workflow

### 1. Check if PDF has fillable fields
```bash
python3 scripts/check_fillable_fields.py <input.pdf>
```
If fillable, continue below. If not, use the non-fillable annotation workflow in forms.md.

### 2. Extract field metadata
```bash
python3 scripts/extract_form_field_info.py <input.pdf> <field_info.json>
```
Output JSON contains field_id, type, page, rect, and for checkboxes: checked_value/unchecked_value.

### 3. Convert PDF to images for visual mapping
```bash
mkdir -p <output_dir>
python3 scripts/convert_pdf_to_images.py <input.pdf> <output_dir>
```
**Important**: Create the output directory first or the script fails.

### 4. Map fields to visual form elements
- Read the generated images to understand what each field_id corresponds to
- Use field names as hints (e.g., `PlaintiffName1`, `DefendantAddress1`)
- Use bounding box `rect` coordinates to locate fields on the page

### 5. Create field_values.json
```json
[
  {
    "field_id": "exact.field.id.from.extract",
    "description": "Human-readable description",
    "page": 1,
    "value": "text value"
  },
  {
    "field_id": "some.checkbox.field",
    "description": "Check this box",
    "page": 2,
    "value": "/1"
  }
]
```

**Value rules:**
- **Text fields**: Plain string value
- **Checkboxes**: Use `checked_value` from field_info.json to check (e.g., "/1", "/On"), `unchecked_value` to uncheck (e.g., "/Off")
- **Radio groups**: Use one of the `value` entries from `radio_options`
- **Omitted fields**: Left blank/unchanged — only include fields you want to fill

### 6. Fill the form
```bash
python3 scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>
```
Script validates field IDs and values. Fix any error messages and retry.

### 7. Verify output
Convert filled PDF to images and visually inspect each page:
```bash
mkdir -p <verify_dir>
python3 scripts/convert_pdf_to_images.py <output.pdf> <verify_dir>
```

## Common Pitfalls
- **Missing output directory**: `convert_pdf_to_images.py` doesn't create directories automatically
- **Wrong field_id**: Must be exact match from extract_form_field_info.py output
- **Wrong page number**: Must match the page value in field_info.json
- **Checkbox values**: Don't use "true"/"false" — use the exact checked_value/unchecked_value strings
- **Script directory**: Must cd to `/root/.claude/skills/pdf` before running scripts
