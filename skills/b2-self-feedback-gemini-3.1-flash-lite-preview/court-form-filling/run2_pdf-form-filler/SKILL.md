---
name: run2_pdf-form-filler
description: Improved skill for filling XFA/non-standard PDFs using FreeText annotations when field mapping is unavailable.
---

# PDF Form Filler Skill (Round 2)

This skill addresses XFA/complex PDF form challenges by using `FreeText` annotations for field population.

## Usage
When field-based filling (via `update_page_form_field_values`) fails due to XFA structure or non-standard forms, utilize annotation-based filling.

## Steps
1. Identify fields manually or via `get_fields()`.
2. Map fields to visual page coordinates.
3. Use a script to overlay text using `FreeText` annotations.
4. Execute via the `scripts/fill_pdf_form_with_annotations.py` utility.

## Example
```python
# Create a JSON configuration mapping pages, bounding boxes, and field values.
# Use the annotation script:
# python scripts/fill_pdf_form_with_annotations.py input.pdf fields.json output.pdf
```
