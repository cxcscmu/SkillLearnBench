---
name: inspect_pdf_form
description: Extracts detailed information about form fields in a PDF, including field keys, types, page indices, current values, and allowed export values for checkboxes and radio buttons. Use this to identify how multi-line text is split across different keys (e.g., 'Reason_1', 'Reason_2') and to find the exact string required to check a box (e.g., 'Yes', '1', or 'On').
---

import pypdf

def inspect_pdf_form(pdf_path: str):
    """
    Inspects the PDF to provide a map of field names to their properties.
    Useful for discovering exact keys for multi-line fields and checkbox export values.
    """
    reader = pypdf.PdfReader(pdf_path)
    form_info = []

    # Iterate through pages to find which field belongs to which page
    for page_index, page in enumerate(reader.pages):
        if "/Annots" in page:
            for annot in page["/Annots"]:
                obj = annot.get_object()
                # Only process form fields (Widget annotations with a Title /T)
                if obj.get("/Subtype") == "/Widget" and "/T" in obj:
                    field_key = obj.get("/T")
                    field_type = obj.get("/FT")
                    current_value = obj.get("/V", "")
                    
                    # Extract export values for checkboxes/radio buttons
                    # These are typically found in the /AP (Appearance) or /Opt keys
                    options = []
                    if "/Opt" in obj:
                        options = obj["/Opt"]
                    elif "/AS" in obj or "/AP" in obj:
                        # Check normal appearance states for checkboxes
                        ap = obj.get("/AP")
                        if ap and "/N" in ap:
                            options = list(ap["/N"].keys())

                    form_info.append({
                        "page": page_index,
                        "key": field_key,
                        "type": field_type,
                        "value": current_value,
                        "options": options
                    })

    for info in form_info:
        print(f"Page {info['page']} | Key: {info['key']} | Type: {info['type']} | Options: {info['options']}")
    return form_info