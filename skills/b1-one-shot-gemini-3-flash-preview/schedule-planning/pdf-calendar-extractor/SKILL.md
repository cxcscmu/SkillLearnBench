---
name: pdf-calendar-extractor
description: Extract text and identifying colored regions (e.g., rectangles) from a PDF using pdfplumber.
---

# PDF Calendar Extractor

This skill provides a way to extract text elements and graphical shapes (like rectangles) from a PDF, including their positions and color properties. This is useful for processing visual calendars where appointments are represented by colored blocks.

## Requirements
- `pdfplumber`

## Example Usage: Extract Rectangles and Text

```python
import pdfplumber

def extract_calendar_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        
        # Extract text with positions
        text_elements = page.extract_text_full() # or extract_words()
        words = page.extract_words()
        
        # Extract rectangles (appointments)
        rects = page.rects
        
        # For each rectangle, you can get:
        # rect['top'], rect['bottom'], rect['left'], rect['right']
        # rect['non_stroking_color'] (fill color)
        
        return words, rects

# Identifying 'blue' blocks
# Blue in RGB is often (0, 0, 1) or a similar variation.
# pdfplumber color formats can vary (RGB, CMYK, etc.)
```

## Tips for Measuring Time
If the calendar has horizontal lines representing 15-minute intervals:
1. Identify all horizontal lines (`page.lines` where `y0 == y1`).
2. Sort them by vertical position (`top`).
3. Calculate the height of a 15-minute block.
4. Map rectangle `top` and `bottom` to specific times based on their position relative to the lines.
