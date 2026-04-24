---
name: california-small-claims-form
description: How to fill out California Small Claims Court forms (SC-100 and related). Use this skill whenever the user needs to complete a California small claims court filing, fill in plaintiff/defendant information, describe a claim, or prepare court documents for small claims cases.
---

# California Small Claims Court Form (SC-100)

## Overview

This skill covers filling out the California SC-100 (Plaintiff's Claim and ORDER to Go to Small Claims Court) form. The form is typically a fillable PDF with standard fields.

## Key Sections in SC-100

### Court Information (top)
- Court name, address, city/state/zip — leave blank unless specified (court fills these)
- Case number — leave blank (court assigns)

### Plaintiff Information (Section 1)
- Full name, address, phone, email
- "First time suing" checkbox

### Defendant Information (Section 2)
- Full name, address, phone
- Multiple defendants possible

### Claim Description (Section 4-6)
- Amount claimed in dollars
- Date(s) the situation occurred (from/to dates)
- Description of why defendant owes money
- What plaintiff has done to collect

### Venue (where to file)
- Checkbox for reason court has jurisdiction (e.g., defendant lives/does business in this county)

### Declaration/Signature
- Date filed
- Plaintiff signature

## Date Format

Use `xxxx-xx-xx` format (ISO 8601: YYYY-MM-DD) when specified. For example: `2026-01-19`.

## Tips for Filling

1. Run `check_fillable_fields.py` first to determine if PDF has fillable fields
2. If fillable, use `extract_form_field_info.py` to get field IDs, then convert to images to understand field purposes
3. Only fill fields relevant to the case — leave court-assigned and optional fields empty
4. For checkboxes: use the `checked_value` from field info
5. For "first time suing": check the appropriate box
6. Defendant address should be complete with street, city, state, zip

## Common Field Patterns

- Plaintiff name: typically "plaintiff_name" or similar
- Phone numbers: no special format required unless form specifies
- Amount: dollar amount without $ sign or with, depending on field
- Dates: use YYYY-MM-DD format when specified

## Script Usage (from /root/.claude/skills/pdf/ directory)

```bash
# Check if PDF has fillable fields
python scripts/check_fillable_fields.py <file.pdf>

# Extract field info to JSON
python scripts/extract_form_field_info.py <input.pdf> <field_info.json>

# Convert to images for visual analysis
python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>

# Fill the form
python scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>
```
