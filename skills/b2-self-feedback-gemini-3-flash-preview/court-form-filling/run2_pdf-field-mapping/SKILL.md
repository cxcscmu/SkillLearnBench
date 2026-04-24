---
name: run2_pdf-field-mapping
description: Techniques for mapping case descriptions to PDF form fields.
---
# PDF Field Mapping

When mapping case data to PDF fields:

1. **Analyze Field IDs**: Look for keywords in the `field_id` (e.g., `PlaintiffName`, `DefendantAddress`, `ClaimAmount`).
2. **Use Bounding Boxes**: If IDs are cryptic, use the `rect` (bounding box) and the page number to identify the field's position on the form.
3. **Handle Checkboxes**: Identify the `checked_value` for "Yes" or "No" options. Usually, `/1` is Yes and `/2` or `/Off` is No, but verify in `field_info.json`.
4. **Consistency Check**: Ensure that data like names and addresses are consistent across different sections of the form (e.g., caption vs. detailed info).
