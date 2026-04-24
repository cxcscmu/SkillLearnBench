---
name: python-pdf-form-filling
description: Use this skill when you need to programmatically fill PDF form fields using Python. Covers inspecting field names and writing values to fillable PDFs.
---

# Filling PDF Forms with Python

## Recommended Libraries

### Option 1: PyPDF2 / PyPDF (pypdf)
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

# Clone the original
writer.append(reader)

# Inspect field names
fields = reader.get_fields()
for field_name, field_obj in fields.items():
    print(f"Field: {field_name}, Type: {field_obj.get('/FT')}, Value: {field_obj.get('/V')}")
```

Filling fields:
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("sc100-blank.pdf")
writer = PdfWriter()
writer.append(reader)

# Fill fields by name
fill_data = {
    "FieldName1": "Value1",
    "FieldName2": "Value2",
}

writer.update_page_form_field_values(writer.pages[0], fill_data)
# For multi-page forms, repeat for each page index

with open("sc100-filled.pdf", "wb") as f:
    writer.write(f)
```

### Option 2: pdfrw
```python
import pdfrw

template = pdfrw.PdfReader("sc100-blank.pdf")

# Iterate annotations to find fields
for page in template.pages:
    annotations = page.get('/Annots')
    if annotations:
        for annot in annotations:
            field_name = annot.get('/T')
            field_type = annot.get('/FT')
            print(f"Field: {field_name}, Type: {field_type}")
```

Filling with pdfrw:
```python
import pdfrw

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

template = pdfrw.PdfReader("sc100-blank.pdf")

data = {
    "(FieldName1)": "Value1",
    "(FieldName2)": "Value2",
}

for page in template.pages:
    annotations = page.get(ANNOT_KEY)
    if annotations:
        for annot in annotations:
            field_name = annot.get(ANNOT_FIELD_KEY)
            if field_name in data:
                annot.update(pdfrw.PdfDict(V=data[field_name]))
                # For text fields, also set appearance if needed
                annot.update(pdfrw.PdfDict(AP=''))  # Reset appearance

pdfrw.PdfWriter().write("sc100-filled.pdf", template)
```

### Option 3: fillpdf / pdftk wrapper
```python
from fillpdf import fillpdfs

# Get field names
fields = fillpdfs.get_form_fields("sc100-blank.pdf")
print(fields)

# Fill the form
data_dict = {
    "FieldName1": "Value1",
    "FieldName2": "Value2",
}
fillpdfs.write_fillable_pdf("sc100-blank.pdf", "sc100-filled.pdf", data_dict)
```

### Option 4: pikepdf
```python
import pikepdf

pdf = pikepdf.open("sc100-blank.pdf")

# Access AcroForm
if '/AcroForm' in pdf.Root:
    fields = pdf.Root.AcroForm.get('/Fields', [])
    for field_ref in fields:
        field = field_ref
        name = str(field.get('/T', ''))
        print(f"Field: {name}, Type: {field.get('/FT')}")
```

## Handling Checkboxes

Checkboxes have specific "on" values. To find the valid value:
```python
# With pypdf
fields = reader.get_fields()
for name, field in fields.items():
    if field.get('/FT') == '/Btn':
        # Check the appearance dictionary for valid states
        print(f"Checkbox: {name}")
        # The widget annotation's /AP/N dictionary keys show valid states
```

Common checkbox patterns:
- Set to `/Yes` or the export value found in `/AP/N` keys
- Uncheck by setting to `/Off`

For pypdf:
```python
# To check a checkbox, you often need:
writer.update_page_form_field_values(
    writer.pages[0],
    {"CheckboxFieldName": "/Yes"},  # or "Yes" or True depending on form
    auto_regenerate=False
)
```

## Key Tips
1. **Always inspect field names first** — PDF field names are not standardized.
2. **Flatten vs non-flatten**: Some approaches flatten the form (making fields non-editable). Use `flatten=False` if you want to keep fields editable.
3. **Multi-page forms**: Ensure you fill fields on the correct page.
4. **Field hierarchy**: Some PDFs use hierarchical field names like `parent.child`. The full qualified name matters.
5. **Encoding**: Use `pdfrw.PdfString.encode()` for pdfrw string values if needed.