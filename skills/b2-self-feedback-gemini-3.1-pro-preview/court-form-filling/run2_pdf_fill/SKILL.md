---
name: run2_pdf_fill
description: A comprehensive skill for mapping, understanding, and filling complex interactive PDF forms using PyMuPDF (fitz).
---

# PDF Form Filling with PyMuPDF

This skill demonstrates how to map and fill interactive PDF forms (AcroForm/XFA) programmatically in Python using `PyMuPDF` (`fitz`).

## Requirements
```bash
pip install PyMuPDF
```

## 1. Finding and Understanding PDF Form Fields

PDF form fields often have cryptic names (e.g., `Checkbox50[0]`). To understand what a field represents, you can find the text visually near the field.

```python
import fitz

def map_fields_with_context(pdf_path):
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        words = page.get_text("words")  # List of words with their bounding boxes
        for w in page.widgets():
            # Expand the widget's bounding box to find nearby text
            rect = fitz.Rect(w.rect)
            rect.x0 -= 100
            rect.x1 += 100
            rect.y0 -= 20
            rect.y1 += 20
            
            # Find words that intersect with the expanded rectangle
            nearby_words = [word[4] for word in words if fitz.Rect(word[:4]).intersects(rect)]
            context_text = " ".join(nearby_words)
            
            # Print field info
            print(f"Page {i+1} | Field: {w.field_name} | Type: {w.field_type}")
            print(f"  Context: {context_text[:100]}...")
            
            # For Checkboxes and Radio Buttons, print their "On" state
            if w.field_type in [fitz.PDF_WIDGET_TYPE_CHECKBOX, fitz.PDF_WIDGET_TYPE_RADIOBUTTON]:
                print(f"  On State Value: {w.on_state()}")
```

## 2. Filling Form Fields

To fill the fields, match the exact `field_name`. Text fields accept strings. For checkboxes and radio buttons, assigning `True` automatically applies the correct internal "On" value (e.g., `"Yes"`, `"1"`, `"Choice1"`).

```python
import fitz

def fill_pdf_form(input_pdf, output_pdf, data_dict):
    """
    Fills a PDF form based on a dictionary mapping field_name -> value.
    """
    doc = fitz.open(input_pdf)
    for page in doc:
        for w in page.widgets():
            if w.field_name in data_dict:
                val = data_dict[w.field_name]
                
                # Checkboxes/Radio buttons can be checked by setting field_value to True
                if w.field_type in [fitz.PDF_WIDGET_TYPE_CHECKBOX, fitz.PDF_WIDGET_TYPE_RADIOBUTTON]:
                    if val is True:
                        w.field_value = w.on_state() # or simply w.field_value = True
                    elif val is False:
                        w.field_value = "Off" # Standard "Off" state
                else:
                    # Text and other fields
                    w.field_value = str(val)
                w.update()
    doc.save(output_pdf)

# Example usage
data = {
    "PlaintiffName[0]": "Joyce He",
    "Checkbox50[0]": True  # Ticks the checkbox
}
fill_pdf_form('input.pdf', 'output.pdf', data)
```