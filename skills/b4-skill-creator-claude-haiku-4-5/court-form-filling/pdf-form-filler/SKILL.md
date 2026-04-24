---
name: pdf-form-filler
description: Fill PDF forms programmatically using pypdf library. Use this skill whenever you need to fill in PDF forms with field data, extract field names from PDFs, or generate filled PDF documents. Essential for automating form completion tasks.
---

# PDF Form Filler

## Overview

Fill interactive PDF forms programmatically using the `pypdf` library. This skill handles reading form fields, populating them with data, and saving the result.

## Library Setup

```python
from pypdf import PdfReader, PdfWriter
```

The `pypdf` library is the primary tool for PDF manipulation in Python 3.8+.

## Key Operations

### 1. Reading PDF Form Fields

Discover available fields in a PDF form:

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")
if reader.get_fields():
    for field_name, field_info in reader.get_fields().items():
        print(f"Field: {field_name}, Type: {field_info.get('/FT')}")
else:
    print("No form fields found")
```

**Output:** Dictionary of field names and their types (Text, Button, Choice, etc.)

### 2. Filling Form Fields

Populate form fields and save the filled PDF:

```python
from pypdf import PdfReader, PdfWriter

# Read the PDF
reader = PdfReader("blank_form.pdf")
writer = PdfWriter()

# Copy all pages
for page in reader.pages:
    writer.add_page(page)

# Update form fields
update_page_form_field_values(
    writer=writer,
    fields={
        "field_name_1": "value 1",
        "field_name_2": "value 2",
    }
)

# Save the result
with open("filled_form.pdf", "wb") as output_file:
    writer.write(output_file)
```

### 3. Common Field Types

- **Text fields**: Simple string input (`/FT` = "/Tx")
- **Button/Checkbox fields**: Boolean values (`/FT` = "/Btn")
- **Choice/Dropdown fields**: Select from options (`/FT` = "/Ch")
- **Signature fields**: Reserved for signatures (`/FT` = "/Sig")

## Field Value Format

When filling fields:
- **Text**: String values work directly
- **Checkboxes**: Use "On"/"Off" or True/False
- **Radio buttons**: Use the specific option value
- **Dates**: Format as string (e.g., "01/15/2026")

## Date Format Handling

Always confirm the expected date format before filling. Common formats:
- `MM/DD/YYYY` (US standard)
- `YYYY-MM-DD` (ISO format)
- Check the form specification for requirements

## Troubleshooting

**Fields not appearing after filling:**
- Verify field names match exactly (case-sensitive)
- Confirm field exists using `get_fields()`
- Some fields may be read-only or hidden

**Empty values overwriting existing data:**
- Only pass fields you want to fill in the dictionary
- Empty strings may clear field values

## See Also

- pypdf documentation: https://pypdf.readthedocs.io/
- When working with California court forms, use the `sc100-form-mapping` skill
