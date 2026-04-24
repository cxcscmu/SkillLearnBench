---
name: pdf-inspection
description: Techniques for inspecting PDF form fields and their properties using Python libraries like pypdf.
---

# PDF Inspection Skill

This skill covers how to identify and list form fields in a PDF document using the `pypdf` library.

## Prerequisites

- Python 3.x
- `pypdf` library (`pip install pypdf`)

## Usage Patterns

### Listing All Fields

To list all fields and their types:

```python
import pypdf

def list_pdf_fields(file_path):
    reader = pypdf.PdfReader(file_path)
    fields = reader.get_fields()
    if not fields:
        print("No fields found.")
        return
    
    for name, field in fields.items():
        field_type = field.get("/FT")
        print(f"Field Name: {name}, Type: {field_type}")

list_pdf_fields("document.pdf")
```

### Understanding Field Types

- `/Tx`: Text field
- `/Btn`: Button (checkbox or radio button)
- `/Ch`: Choice field (dropdown or list box)
- `/Sig`: Signature field

### Identifying Checkbox Values

Checkboxes often use "Off" and another value (like "Yes" or "On"). You can find these in the `/AP` or `/V` keys if they have a value.

```python
field_props = reader.get_fields()["field_name"]
print(field_props.get("/V")) # Current value
```
