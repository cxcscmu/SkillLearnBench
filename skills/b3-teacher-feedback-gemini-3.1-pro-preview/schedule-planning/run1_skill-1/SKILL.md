[SKILL]
---
name: pymupdf-visual-calendar-parsing
description: Parse visual PDF calendars by extracting visual elements (horizontal lines, colored event blocks) and mapping their vertical Y-coordinates to time values using PyMuPDF (fitz).
---

When parsing visual calendars in PDF format, events and grid lines are typically drawn as vector graphics rather than plain text. You can use PyMuPDF (`fitz`) to extract text (for the timeline axis labels) and vector drawings (rectangles representing events, and lines representing time intervals).

### 1. Extracting Drawings (Lines and Rectangles)
Use `page.get_drawings()` to extract all vector shapes. You can identify horizontal grid lines and colored event blocks based on the drawing item properties.

```python
import fitz

doc = fitz.open("calendar.pdf")
page = doc[0]
drawings = page.get_drawings()

horizontal_lines = set()
event_blocks = []

for d in drawings:
    # Colors are typically represented as RGB tuples/lists like [0.0, 0.0, 1.0] for blue
    fill_color = d.get("fill") 
    
    for item in d["items"]:
        if item[0] == "l": # It's a line
            p1, p2 = item[1], item[2]
            if p1.y == p2.y: # It's a horizontal line
                horizontal_lines.add(p1.y)
        elif item[0] == "re": # It's a rectangle
            rect = item[1] # A fitz.Rect object
            event_blocks.append({
                "y0": rect.y0,
                "y1": rect.y1,
                "color": fill_color
            })

# Sort lines from top to bottom
sorted_y_lines = sorted(list(horizontal_lines))
```

### 2. Extracting Timeline Text Labels
You must parse text from the PDF to identify the time values corresponding to the axis, and find their vertical coordinates.

```python
text_dict = page.get_text("dict