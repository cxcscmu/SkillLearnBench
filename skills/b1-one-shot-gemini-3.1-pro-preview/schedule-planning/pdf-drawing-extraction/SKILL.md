---
name: pdf-drawing-extraction
description: Extracts vector graphics, colors, and text from PDF files using PyMuPDF to analyze calendars or visual schedules.
---

# PDF Drawing Extraction with PyMuPDF

This skill demonstrates how to use `PyMuPDF` (`fitz`) to extract vector drawings and rectangles from a PDF. This is particularly useful for extracting calendar blocks and colors.

## Setup
Ensure PyMuPDF is installed:
```bash
pip install PyMuPDF
```

## Basic Usage

```python
import fitz

def extract_colored_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0] # first page
    
    # Get all drawings
    drawings = page.get_drawings()
    
    blocks = []
    for d in drawings:
        rect = d.get('rect')
        color = d.get('color')
        fill = d.get('fill')
        
        # Determine color (RGB values typically 0.0 to 1.0)
        # Assuming fill color is used for block background
        if fill:
            r, g, b = fill
            is_blue = (b > r and b > g) # basic blue check
            
            blocks.append({
                'rect': rect,
                'is_blue': is_blue,
                'fill': fill
            })
            
    return blocks
```

This extracts bounding boxes (`fitz.Rect`) and their associated fill colors. You can correlate these boxes with text in the same PDF by using `page.get_text("dict")` or checking overlaps between text rectangles and drawing rectangles.
