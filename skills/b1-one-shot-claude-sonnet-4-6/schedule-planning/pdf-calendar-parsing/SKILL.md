---
name: pdf-calendar-parsing
description: Use PyMuPDF (fitz) to extract visual calendar blocks from a PDF, including color detection and pixel-to-time conversion.
---

# PDF Calendar Parsing with PyMuPDF

## Installation
```bash
pip install pymupdf
```

## Core Concepts

### Open and render a PDF page
```python
import fitz  # PyMuPDF

doc = fitz.open("calendar.pdf")
page = doc[0]  # First page

# Get page dimensions
rect = page.rect
print(rect.width, rect.height)

# Render to image for pixel-level inspection
mat = fitz.Matrix(2, 2)  # 2x zoom for clarity
pix = page.get_pixmap(matrix=mat)
pix.save("calendar_render.png")
```

### Extract drawings/rectangles (color blocks)
```python
drawings = page.get_drawings()
for d in drawings:
    rect = d["rect"]          # (x0, y0, x1, y1)
    fill = d["fill"]          # (R, G, B) normalized 0-1
    color = d["color"]        # stroke color
    print(rect, fill)
```

### Detect blue/purple blocks (low priority)
```python
def is_blue(fill):
    if fill is None:
        return False
    r, g, b = fill
    # Blue/purple: high blue, moderate green, low-mid red
    return b > 0.5 and b > r and (g < 0.7 or r < 0.5)

def is_blocking(fill):
    """Salmon/red or gray blocks that cannot be overwritten"""
    if fill is None:
        return False
    r, g, b = fill
    # Salmon/red: high red, moderate green, low blue
    return r > 0.6 and g < 0.6 and b < 0.5
```

### Convert pixel Y coordinate to time
```python
def y_to_time(y, page_height, timeline_start_y, timeline_end_y,
              start_hour=0, end_hour=24):
    """
    Convert y pixel position to hour (float).
    timeline_start_y: y-pixel where 12am starts
    timeline_end_y: y-pixel where 11:59pm ends
    """
    total_hours = end_hour - start_hour
    ratio = (y - timeline_start_y) / (timeline_end_y - timeline_start_y)
    hour = start_hour + ratio * total_hours
    return hour  # float, e.g. 10.5 = 10:30am

def hour_to_time_str(hour):
    h = int(hour)
    m = int((hour - h) * 60)
    period = "AM" if h < 12 else "PM"
    if h == 0: h = 12
    elif h > 12: h -= 12
    return f"{h:02d}:{m:02d} {period}"
```

### Extract text blocks with positions
```python
blocks = page.get_text("blocks")
for block in blocks:
    x0, y0, x1, y1, text, block_no, block_type = block
    print(f"Text: {text.strip()!r} at y={y0:.1f}-{y1:.1f}")
```

### Full workflow
```python
import fitz

doc = fitz.open("calendar.pdf")
page = doc[0]

# 1. Get all colored rectangles
drawings = page.get_drawings()

# 2. Find timeline boundaries by locating hour labels
# The leftmost column with hour labels defines the timeline axis
text_blocks = page.get_text("dict")["blocks"]

# 3. For each drawing, determine if it's blue (overwritable) or blocking
events = []
for d in drawings:
    fill = d.get("fill")
    if fill and d["rect"].height > 5:  # filter tiny artifacts
        events.append({
            "rect": d["rect"],
            "fill": fill,
            "is_blue": is_blue(fill),
            "is_blocking": is_blocking(fill)
        })
```

## Tips
- Calendar hour markers (12am, 1am, ...) appear as text at fixed y-positions; use these to calibrate the pixel-to-time mapping
- 15-minute intervals are visible as dashed horizontal lines between hour markers
- Blue/purple fill typically has RGB values around (0.4-0.6, 0.4-0.6, 0.7-0.9)
- Gray "Out of office" blocks have roughly equal R, G, B values around 0.4-0.6
