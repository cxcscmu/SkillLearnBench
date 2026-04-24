---
name: fill_pdf_form
description: Fills a PDF form with provided data. It maps field keys to their respective pages and applies values. It handles multi-line text areas by assigning specific strings to the identified sequential keys. For checkboxes, it uses the precise export values found during inspection. All dates must be formatted as 'xxxx-xx-xx'.
---

import pypdf

def fill_pdf_form(input_pdf_path: str, output_pdf_path: str, data: dict):
    """
    Fills a PDF form. 
    'data' should be a flat dictionary where keys match the PDF field names.
    The function automatically identifies the page for each key and updates it.
    """
    reader = pypdf.PdfReader(input_pdf_path)
    writer = pypdf.PdfWriter()
    writer.append_pages_from_reader(reader)

    # Create a mapping of field keys to page indices
    field_to_page = {}
    for page_index, page in enumerate(reader.pages):
        if "/Annots" in page:
            for annot in page["/Annots"]:
                obj = annot.get_object()
                if "/T" in obj:
                    field_to_page[obj["/T"]] = page_index

    # Group data by page index for update_page_form_field_values
    page_updates = {}
    for key, value in data.items():
        if key in field_to_page:
            p_idx = field_to_page[key]
            if p_idx not in page_updates:
                page_updates[p_idx] = {}
            page_updates[p_idx][key] = value

    # Apply updates page by page
    for p_idx, fields in page_updates.items():
        writer.update_page_form_field_values(writer.pages[p_idx], fields)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)