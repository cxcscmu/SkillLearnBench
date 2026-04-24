---
name: run2_pdf-parser
description: An improved skill to programmatically parse PDF calendars, mapping drawing coordinates to precise time intervals using PyMuPDF.
---

# Improved PDF Schedule Parsing

This advanced skill automates the extraction of schedules from visual PDFs. Instead of manual inference, it mathematically calculates time blocks by using baseline anchor lines.

## Dynamic Time Calculation
By identifying the top-most timeline grid line (e.g., the 12:00 AM line), you can calculate any Y-coordinate's corresponding time.

```python
import fitz

def parse_calendar(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    
    # Extract lines to find the 15-minute grid spacing
    lines = [d["rect"] for d in page.get_drawings() if d.get("fill") is None and d["rect"].height < 2]
    lines.sort(key=lambda r: r.y0)
    
    base_y = lines[0].y0  # The 12:00 AM line
    interval_y = lines[1].y0 - lines[0].y0  # Height of 15 minutes
    hour_height = interval_y * 4
    
    # Extract rectangles (appointments)
    # Exclude the background/grid lines and thin borders by checking width/height and colors
    blocks = []
    for d in page.get_drawings():
        rect = d["rect"]
        color = d.get("fill")
        if color and rect.width > 100:  # Assuming meeting blocks span the column width
            start_hour = (rect.y0 - base_y) / hour_height
            end_hour = (rect.y1 - base_y) / hour_height
            blocks.append({
                "start": start_hour,
                "end": end_hour,
                "color": color
            })
    return blocks
```

## Identifying Flexible Slots
By checking the RGB values of the `fill` color, we can identify "blue-colored" blocks that denote flexible time and drop them from our strict occupied schedule list.

