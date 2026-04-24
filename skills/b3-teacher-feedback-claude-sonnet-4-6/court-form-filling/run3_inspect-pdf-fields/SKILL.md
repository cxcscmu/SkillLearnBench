---
name: inspect-pdf-fields
description: Use this skill to inspect all form fields in a PDF file, printing their names, types, and current values/export values. Useful for understanding the structure of a PDF form before filling it.
---

## Inspect PDF Form Fields

```python
import pypdf
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "/root/sc100-blank.pdf"

reader = pypdf.PdfReader(pdf_path)

print(f"Number of pages: {len(reader.pages)}")
print(f"Number of fields: {len(reader.get_fields()) if reader.get_fields() else 0}")
print()

fields = reader.get_fields()
if not fields:
    print("No form fields found.")
else:
    for field_name, field_obj in fields.items():
        field_type = field_obj.get("/FT", "Unknown")
        field_value = field_obj.get("/V", "")
        field_default = field_obj.get("/DV", "")
        
        # Get export values for checkboxes/radio buttons
        ap = field_obj.get("/AP", {})
        kids = field_obj.get("/Kids", [])
        
        print(f"Field Name: {repr(field_name)}")
        print(f"  Type: {field_type}")
        print(f"  Value: {repr(field_value)}")
        print(f"  Default: {repr(field_default)}")
        
        # Try to get export values
        if field_type in ["/Btn"]:
            opt = field_obj.get("/Opt", [])
            print(f"  Options: {opt}")
            # Check AP for on state name
            if ap:
                n_dict = ap.get("/N", {})
                if hasattr(n_dict, 'keys'):
                    print(f"  AP/N keys (export values): {list(n_dict.keys())}")
        
        print()
```

Run this script to see all fields:
```bash
python3 /root/inspect_fields.py /root/sc100-blank.pdf 2>&1 | head -200
```