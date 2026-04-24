---
name: pdf-form-filling
description: Methods for programmatically filling PDF forms (AcroForms) and saving the results using pypdf.
---

# PDF Form Filling Skill

This skill covers how to fill out AcroForms in a PDF document using `pypdf`.

## Prerequisites

- Python 3.x
- `pypdf` library (`pip install pypdf`)

## Usage Patterns

### Filling Text Fields and Checkboxes

```python
from pypdf import PdfReader, PdfWriter

def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Fill form fields
    writer.update_page_form_field_values(writer.pages[0], data_dict)
    
    # Note: If fields span multiple pages, you might need to iterate 
    # through writer.pages and apply relevant parts of data_dict.
    # However, writer.update_page_form_field_values can often find the fields
    # globally if they are properly indexed.

    with open(output_pdf_path, "wb") as output_stream:
        writer.write(output_stream)

# Example data_dict
# For text fields: {"field_name": "Value"}
# For checkboxes: {"checkbox_name": "/Yes"} or similar
data = {
    "full_name": "John Doe",
    "is_citizen": "/Yes"
}

fill_pdf("blank.pdf", "filled.pdf", data)
```

### Important Considerations

1. **Field Naming**: Use the full hierarchical name found during inspection (e.g., `SC-100[0].Page1[0].Field[0]`).
2. **Appearance Streams**: Some PDF readers might not show the filled value until you click on the field unless `/NeedAppearances` is set to true in the PDF's Interactive Form Dictionary. `pypdf` handles basic filling, but complex forms might need flattening or specific appearance settings.
3. **Checkboxes**: Checkbox values are typically `/Yes` (or other export value) and `/Off`.
