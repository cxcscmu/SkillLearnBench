---
name: Extract PDF Form Field Names
description: Use this skill first to discover the actual field names in a PDF form. Extracts and prints all form field names from a PDF file to ensure accurate field mapping before filling the form.
---

# Extract PDF Form Field Names

## Purpose
Discover the exact field names in a PDF form before attempting to fill it. This prevents mapping errors and field-not-found issues.

## Implementation

```python
import pdfrw

def extract_pdf_field_names(pdf_path):
    """
    Extract all form field names from a PDF.
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        List of field names
    """
    template = pdfrw.PdfReader(pdf_path)
    field_names = []
    
    if template.Root.AcroForm is None:
        print("No form fields found in PDF")
        return field_names
    
    for page in template.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                if annotation["/Subtype"] == "/Widget":
                    field_name = annotation["/T"]
                    if field_name:
                        # Remove parentheses that pdfrw adds
                        clean_name = field_name[1:-1] if field_name.startswith('(') else field_name
                        field_names.append(clean_name)
                        print(f"Field found: {clean_name}")
    
    return field_names

# Run extraction
pdf_path = "/root/sc100-blank.pdf"
fields = extract_pdf_field_names(pdf_path)
print(f"\nTotal fields found: {len(fields)}")
```

## Steps
1. Load the PDF using pdfrw
2. Check if form exists in Root.AcroForm
3. Iterate through all pages and annotations
4. Extract field names from Widget annotations
5. Clean field names (remove parentheses added by pdfrw)
6. Print each field name for verification
7. Use the printed names for accurate field mapping

## Notes
- Run this skill BEFORE attempting to fill the form
- Document all field names printed to ensure mapping accuracy
- Field names are case-sensitive