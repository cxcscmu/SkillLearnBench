---
name: python-pypdf
description: Guide on using the Python pypdf library to read, write, and fill PDF forms programmatically.
---

# pypdf

The `pypdf` library allows you to manipulate PDF files in Python. This skill focuses on reading PDF form fields and filling them out programmatically.

## Installation

```bash
pip install pypdf
```

## Reading PDF Form Fields

You can read all form fields from a PDF to understand their names and types:

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")
fields = reader.get_fields()

for field_name, field_data in fields.items():
    print(f"Field: {field_name}, Type: {field_data.get('/FT')}, Value: {field_data.get('/V')}")
```

## Filling PDF Forms

You can create a writer object, append the pages from the reader, and then use the `update_page_form_field_values` method to fill fields:

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append_pages_from_reader(reader)

# Define a dictionary mapping field names to values.
data = {
    "FieldName1": "Value1",
    "Checkbox1": "/Yes"  # Checkboxes usually expect "/Yes" or "/Off"
}

writer.update_page_form_field_values(writer.pages[0], data)

with open("filled.pdf", "wb") as f:
    writer.write(f)
```
