---
name: pdf-form-filling
description: Fill PDF form fields using pypdf library in Python, including text fields and checkboxes.
---

# PDF Form Filling with pypdf

## When to Use
When you need to programmatically fill in PDF forms (AcroForms) with text values and checkbox selections.

## Setup
```bash
pip install pypdf
```

## Key Concepts

### Reading Form Fields
```python
import pypdf
reader = pypdf.PdfReader('form.pdf')
fields = reader.get_fields()
for name, field in fields.items():
    print(f"{name} | type={field.get('/FT')} | states={field.get('/_States_', [])}")
```

- `/FT` = `/Tx` → text field
- `/FT` = `/Btn` → checkbox/button
- `/_States_` shows valid values for checkboxes (e.g., `['/1', '/Off']`)

### Filling the Form
```python
reader = pypdf.PdfReader('blank.pdf')
writer = pypdf.PdfWriter()
writer.append(reader)

# Build field data dict - keys are FULL field paths
field_data = {
    "Form[0].Page1[0].TextField[0]": "value",
}

# For checkboxes, use the "on" state value from _States_ (e.g., '/1', '/2')
field_data["Form[0].Checkbox[0]"] = "/1"  # checked
# Use '/Off' for unchecked (usually default)

# Update fields on specific pages
writer.update_page_form_field_values(writer.pages[page_idx], field_data)

with open('filled.pdf', 'wb') as f:
    writer.write(f)
```

### Important Notes
- Field names are hierarchical paths like `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName1[0]`
- `update_page_form_field_values` only updates fields present on the specified page
- For radio-button-style checkboxes (Yes/No pairs), each option has its own field with different "on" states (`/1` for first, `/2` for second)
- Always use the full field path as the key
- Auto-formatting may not work; set `/NeedAppearances` if text doesn't display
