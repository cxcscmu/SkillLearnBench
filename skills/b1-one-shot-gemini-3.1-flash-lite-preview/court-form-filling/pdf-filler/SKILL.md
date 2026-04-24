---
name: pdf-filler
description: Provides guidelines for filling out PDF forms using programming tools.
---

# PDF Filler Skill

## Overview
This skill provides instructions for filling out existing PDF form fields using Python libraries like `pypdf` or `pdfrw`.

## Prerequisites
- Python 3.x
- `pypdf` library

## Installation
```bash
pip install pypdf
```

## Usage Pattern
```python
from pypdf import PdfReader, PdfWriter

def fill_pdf(input_path, output_path, data_dict):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Copy pages
    for page in reader.pages:
        writer.add_page(page)

    # Fill fields
    writer.update_page_form_field_values(
        writer.pages[0], data_dict
    )

    with open(output_path, "wb") as output_stream:
        writer.write(output_stream)
```
