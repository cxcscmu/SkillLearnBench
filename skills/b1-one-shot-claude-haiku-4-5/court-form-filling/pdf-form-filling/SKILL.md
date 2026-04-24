---
name: pdf-form-filling
description: Fill PDF form fields programmatically using Python libraries like pypdf or pdfrw
---

# PDF Form Filling with Python

## Overview
This skill covers how to identify and fill form fields in PDF documents, particularly for legal forms like court documents.

## Key Libraries

### 1. PyPDF (pypdf)
- Modern, actively maintained library for PDF manipulation
- Can read form field names and fill them
- Installation: `pip install pypdf`

### 2. pdfrw
- Lightweight alternative, good for form filling
- Installation: `pip install pdfrw`

## Common Workflow

### With pypdf:
```python
from pypdf import PdfReader, PdfWriter

# Read the blank form
reader = PdfReader("/path/to/form.pdf")
writer = PdfWriter()

# Get the form fields
fields = reader.get_fields()
print(fields.keys())  # See all available fields

# Create a copy and update fields
for page in reader.pages:
    writer.add_page(page)

# Update fields
writer.update_page_form_field_values(
    writer.pages[0],
    {
        "Field1": "Value1",
        "Field2": "Value2",
    }
)

# Save the result
with open("/path/to/filled.pdf", "wb") as f:
    writer.write(f)
```

### With pdfrw:
```python
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject

# Read template
template = PdfReader("/path/to/form.pdf")

# Inspect available fields
for field in template.Root.AcroForm.Fields:
    print(field.T)  # Field name

# Fill fields
for field in template.Root.AcroForm.Fields:
    if field.T == "FieldName":
        field.V = "Field Value"
        field.AP = None  # Clear appearance stream

# Write output
PdfWriter().write("/path/to/filled.pdf", template)
```

## Inspecting Form Fields

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")
fields = reader.get_fields()

for field_name, field_data in fields.items():
    print(f"{field_name}: {field_data}")
```

## Important Notes

- Form field names are case-sensitive
- Some PDFs have checkboxes/radio buttons requiring "Yes"/"No" or specific values
- Date fields may need specific formatting
- Always check field types before filling
- Keep a copy of the blank form for reference

## California Court Forms Specifics

California court forms often use:
- Multi-page layouts with page numbers
- Standard field naming conventions
- Checkboxes for yes/no selections
- Date fields in specific formats
- Signature/initial areas (typically left blank)

When filling:
1. Always read the form first to understand field names
2. Map case data to appropriate fields
3. Leave court-filled sections empty (dates, case numbers, judge info)
4. Preserve form formatting
