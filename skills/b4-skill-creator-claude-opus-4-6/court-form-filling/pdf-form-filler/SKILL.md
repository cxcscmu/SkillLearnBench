---
name: pdf-form-filler
description: Fill PDF form fields programmatically using Python and pypdf. Use this skill whenever the user needs to fill out a PDF form, set text fields, or check checkboxes in a PDF document.
---

# PDF Form Filler

Fill PDF forms using pypdf (available in the environment).

## Workflow

1. **Extract field names**: Read the PDF and list all form fields with their full hierarchical paths
2. **Identify field types**: `/Tx` = text field, `/Btn` = checkbox/button
3. **Map data to fields**: Match user-provided data to the correct field paths
4. **Fill and save**: Use `pypdf.PdfWriter` to write values

## Key Code Pattern

```python
import pypdf

reader = pypdf.PdfReader("input.pdf")
writer = pypdf.PdfWriter()
writer.append(reader)

# Fill text fields - use the SHORT field name (leaf), not full path
# writer.update_page_form_field_values(writer.pages[page_idx], {"FieldName[0]": "value"})

# For checkboxes, update the annotation directly:
# Find the annotation on the page, then set /V and /AS to the checked state
for page in writer.pages:
    for annot in page.get("/Annots", []):
        obj = annot.get_object()
        if obj.get("/T") == "CheckboxName[0]":
            obj.update({
                pypdf.generic.NameObject("/V"): pypdf.generic.NameObject("/1"),
                pypdf.generic.NameObject("/AS"): pypdf.generic.NameObject("/1"),
            })

writer.write("output.pdf")
```

## Checkbox States

- Check the `/AP` -> `/N` dictionary for valid appearance states (e.g., `/1`, `/2`, `/Off`)
- Set both `/V` and `/AS` to the desired state
- `/Off` typically means unchecked

## Tips

- Field names in annotations use the SHORT leaf name (e.g., `PlaintiffName1[0]`), not the full hierarchical path
- `update_page_form_field_values` works for text fields on a specific page
- For checkboxes, iterate annotations and update directly
- Some PDFs have duplicate field names across pages (e.g., `Plaintiff[0]` on pages 2, 3, 4) - handle each page separately
