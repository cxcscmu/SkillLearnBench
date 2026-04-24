---
name: fill-sc100-small-claims-form
description: Use this skill to fill in the California SC-100 Small Claims Court PDF form with case data and save the filled PDF. Handles text fields, checkboxes, and radio buttons using pypdf. Run the inspection skill first to confirm field names, then use this skill to write the filled PDF to /root/sc100-filled.pdf.
---

## Fill SC-100 Small Claims Court Form

### Step 1: Inspect the form fields first

```python
# Save as /root/inspect_sc100.py and run it
import pypdf

reader = pypdf.PdfReader("/root/sc100-blank.pdf")
fields = reader.get_fields()

if not fields:
    print("No fields found!")
else:
    for name, obj in fields.items():
        ft = obj.get("/FT", "?")
        val = obj.get("/V", "")
        ap = obj.get("/AP", {})
        on_states = []
        if ft == "/Btn" and ap:
            n = ap.get("/N", {})
            if hasattr(n, 'keys'):
                on_states = [k for k in n.keys() if k != "/Off"]
        print(f"{repr(name):60s} type={ft}  val={repr(val)}  on_states={on_states}")
```

```bash
python3 /root/inspect_sc100.py
```

### Step 2: Fill the form

```python
# Save as /root/fill_sc100.py and run it
import pypdf
from pypdf.generic import (
    NameObject, StringObject, BooleanObject, ArrayObject,
    DictionaryObject, NumberObject
)
import copy

def fill_pdf(input_path, output_path, field_values, checkbox_values):
    reader = pypdf.PdfReader(input_path)
    writer = pypdf.PdfWriter()
    writer.append(reader)
    
    # Fill text fields
    for page in writer.pages:
        writer.update_page_form_field_values(page, field_values)
    
    # Handle checkboxes/radio buttons separately
    if checkbox_values:
        for page in writer.pages:
            if "/Annots" in page:
                for annot_ref in page["/Annots"]:
                    annot = annot_ref.get_object()
                    if annot.get("/Subtype") == "/Widget":
                        ft = annot.get("/FT", "")
                        t = annot.get("/T", "")
                        # Also check parent for field name
                        parent = annot.get("/Parent", None)
                        field_name = str(t)
                        if parent:
                            parent_obj = parent.get_object() if hasattr(parent, 'get_object') else parent
                            parent_t = parent_obj.get("/T", "")
                            if parent_t:
                                field_name = str(parent_t)
                        
                        if ft == "/Btn" and field_name in checkbox_values:
                            export_val = checkbox_values[field_name]
                            annot_obj = annot
                            annot_obj.update({
                                NameObject("/V"): NameObject(export_val),
                                NameObject("/AS"): NameObject(export_val),
                            })
    
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"Saved filled PDF to {output_path}")

# ── Case data ──────────────────────────────────────────────────────────────
# These field names are placeholders — replace with actual names from inspection
# Common SC-100 field name patterns are used below

text_fields = {
    # Plaintiff info
    "plaintiff_name":           "Joyce He",
    "plaintiff_address":        "655 S Fair Oaks Ave",
    "plaintiff_city_state_zip": "Sunnyvale, CA 94086",
    "plaintiff_phone":          "4125886066",
    "plaintiff_email":          "he1998@gmail.com",
    
    # Defendant info
    "defendant_name":           "Zhi Chen",
    "defendant_address":        "299 W Washington Ave",
    "defendant_city_state_zip": "Sunnyvale, CA 94086",
    "defendant_phone":          "5125658878",
    
    # Claim info
    "amount":                   "1500",
    "claim_description":        "Defendant failed to return security deposit of $1500 per signed roommate sublease contract after moving out.",
    "date_from":                "2025-09-30",
    "date_to":                  "2026-01-19",
    "filing_date":              "2026-01-19",
    
    # Venue reason
    "venue_reason":             "Defendant lives in this court district.",
}

# Checkbox/radio export values (use actual export values from inspection)
checkbox_fields = {
    "first_time_plaintiff":     "Yes",   # Joyce's first time suing
    "venue_defendant_lives":    "Yes",   # Defendant lives in district
}

fill_pdf(
    "/root/sc100-blank.pdf",
    "/root/sc100-filled.pdf",
    text_fields,
    checkbox_fields
)
```

```bash
python3 /root/fill_sc100.py
```

### Step 3: Verify the output

```python
# Save as /root/verify_sc100.py
import pypdf

reader = pypdf.PdfReader("/root/sc100-filled.pdf")
fields = reader.get_fields()
for name, obj in fields.items():
    val = obj.get("/V", "")
    if val and val not in ("", "/Off"):
        print(f"{name}: {repr(val)}")
```

```bash
python3 /root/verify_sc100.py
```

### Step 4: If field names differ, use this robust filler

If the above doesn't work due to field name mismatches, use this approach after inspecting:

```python
# Save as /root/fill_sc100_robust.py
import pypdf
from pypdf.generic import NameObject, StringObject

def get_all_widget_annotations(writer):
    """Get all widget annotations with their field names."""
    widgets = []
    for page_num, page in enumerate(writer.pages):
        if "/Annots" in page:
            for annot_ref in page["/Annots"]:
                annot = annot_ref.get_object()
                if annot.get("/Subtype") == "/Widget":
                    # Walk up parent chain to get full field name
                    t_parts = []
                    obj = annot
                    while obj:
                        t = obj.get("/T")
                        if t:
                            t_parts.insert(0, str(t))
                        parent_ref = obj.get("/Parent")
                        if parent_ref:
                            obj = parent_ref.get_object()
                        else:
                            break
                    full_name = ".".join(t_parts)
                    ft = annot.get("/FT", "")
                    # Check parent FT if not on annot
                    if not ft:
                        par = annot.get("/Parent")
                        if par:
                            ft = par.get_object().get("/FT", "")
                    widgets.append((full_name, ft, annot, annot_ref, page_num))
    return widgets

reader = pypdf.PdfReader("/root/sc100-blank.pdf")
writer = pypdf.PdfWriter()
writer.append(reader)

widgets = get_all_widget_annotations(writer)
print(f"Found {len(widgets)} widgets")
for name, ft, annot, ref, pg in widgets:
    val = annot.get("/V", "")
    ap = annot.get("/AP", {})
    on_states = []
    if ft == "/Btn" and ap:
        n = ap.get("/N", {})
        if hasattr(n, 'keys'):
            on_states = [k for k in n.keys() if k != "/Off"]
    print(f"  Page {pg+1} | {repr(name):50s} | FT={ft} | V={repr(val)} | on={on_states}")
```

```bash
python3 /root/fill_sc100_robust.py
```

### Step 5: Final fill using exact field names from inspection

After confirming exact field names, update and run:

```python
# /root/fill_sc100_final.py
import pypdf
from pypdf.generic import NameObject, StringObject

reader = pypdf.PdfReader("/root/sc100-blank.pdf")
writer = pypdf.PdfWriter()
writer.append(reader)

# Update text fields using writer method
# Replace keys with exact field names from inspection output
text_data = {}  # populated below after inspection

# Fill all pages
for page in writer.pages:
    if text_data:
        writer.update_page_form_field_values(page, text_data)

# Set checkbox/radio values directly on annotations
for page in writer.pages:
    if "/Annots" not in page:
        continue
    for annot_ref in page["/Annots"]:
        annot = annot_ref.get_object()
        if annot.get("/Subtype") != "/Widget":
            continue
        
        # Get field name
        t = annot.get("/T", "")
        parent = annot.get("/Parent")
        if parent:
            p_obj = parent.get_object()
            pt = p_obj.get("/T", "")
            if pt:
                t = pt
        field_name = str(t)
        
        ft = annot.get("/FT", "")
        if not ft and parent:
            ft = parent.get_object().get("/FT", "")
        
        # Set checkbox ON
        # (fill these in after inspection)
        checkbox_map = {}  # e.g. {"field_name": "/Yes"}
        
        if ft == "/Btn" and field_name in checkbox_map:
            export = checkbox_map[field_name]
            annot.update({
                NameObject("/V"): NameObject(export),
                NameObject("/AS"): NameObject(export),
            })

with open("/root/sc100-filled.pdf", "wb") as f:
    writer.write(f)
print("Done — saved /root/sc100-filled.pdf")
```