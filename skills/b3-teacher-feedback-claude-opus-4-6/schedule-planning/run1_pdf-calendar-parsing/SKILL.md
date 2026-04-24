---
name: pdf-calendar-parsing
description: Use this skill when you need to extract calendar/schedule information from a PDF file, including measuring visual positions of appointment blocks, identifying colors of blocks, and determining time slots based on grid lines. Specifically useful for parsing visual calendars where time is encoded by position relative to horizontal grid lines.
---

## PDF Calendar Parsing

### Approach Overview
To extract schedule data from a visual PDF calendar, you need to:
1. Convert the PDF to an image or parse its vector/text content
2. Identify the time axis and grid lines
3. Detect colored blocks representing appointments
4. Map pixel positions to actual times

### Tools and Libraries

**Python libraries:**
- `pdfplumber` — extracts text, lines, and rectangles from PDFs with precise coordinates
- `PyMuPDF` (fitz) — renders PDF pages to images, extracts drawings and text with positions
- `pdf2image` + `Pillow` — converts PDF to images for pixel-level analysis
- `tabula-py` or `camelot` — for table extraction (less useful for visual calendars)

### Extracting Horizontal Lines with pdfplumber

```python
import pdfplumber

with pdfplumber.open("/root/calendar.pdf") as pdf:
    page = pdf.pages[0]
    # Get all lines
    lines = page.lines
    # Filter horizontal lines (y0 == y1 or nearly equal)
    horizontal_lines = [l for l in lines if abs(l['top'] - l['bottom']) < 2]
    # Sort by vertical position
    horizontal_lines.sort(key=lambda l: l['top'])
```

### Extracting Rectangles/Blocks with pdfplumber

```python
    rects = page.rects
    for rect in rects:
        print(rect)  # Keys: x0, y0, x1, y1, top, bottom, fill color, etc.
```

### Extracting Colored Blocks with PyMuPDF

```python
import fitz

doc = fitz.open("/root/calendar.pdf")
page = doc[0]

# Get drawings (vector graphics)
drawings = page.get_drawings()
for d in drawings:
    for item in d["items"]:
        # item is a tuple like ("re", rect) for rectangles
        pass
    fill_color = d.get("fill")  # RGB tuple, e.g., (0, 0, 1) for blue
    rect = d.get("rect")        # fitz.Rect object
```

### Identifying Blue Blocks

Blue blocks typically have RGB fill values where:
- Blue channel is dominant (close to 1.0)
- Red and Green channels are low

```python
def is_blue(color):
    if color is None:
        return False
    r, g, b = color[:3]
    return b > 0.5 and r < 0.5 and g < 0.5
```

### Mapping Positions to Times

Given that the space between two adjacent horizontal lines = 15 minutes:

```python
# After sorting horizontal lines by y-position
line_positions = sorted(set(l['top'] for l in horizontal_lines))

# Determine the starting time from text labels on the calendar
# e.g., if the first line corresponds to 8:00 AM
start_time = datetime.strptime("08:00 AM", "%I:%M %p")

def y_to_time(y, line_positions, start_time):
    """Convert a y-coordinate to a time based on grid lines."""
    from datetime import timedelta
    # Find which interval the y falls in
    for i in range(len(line_positions) - 1):
        if line_positions[i] <= y <= line_positions[i + 1]:
            # Interpolate within the interval
            frac = (y - line_positions[i]) / (line_positions[i + 1] - line_positions[i])
            minutes = (i + frac) * 15
            return start_time + timedelta(minutes=minutes)
    # If beyond last line
    idx = len(line_positions) - 1
    extra = (y - line_positions[-1]) / (line_positions[1] - line_positions[0])
    minutes = (idx + extra) * 15
    return start_time + timedelta(minutes=minutes)
```

### Extracting Text Labels

```python
# With pdfplumber
words = page.extract_words()
for w in words:
    print(w['text'], w['top'], w['x0'])  # text content and position
```

### Determining Day Columns

If the calendar has multiple days (columns):
1. Extract day/date headers from text at the top
2. Identify column boundaries from vertical lines or header positions
3. Map each block's x-position to the appropriate day column

```python
vertical_lines = [l for l in lines if abs(l['x0'] - l['x1']) < 2]
vertical_lines.sort(key=lambda l: l['x0'])
column_boundaries = [l['x0'] for l in vertical_lines]

def x_to_day(x, column_boundaries, day_labels):
    for i in range(len(column_boundaries) - 1):
        if column_boundaries[i] <= x < column_boundaries[i + 1]:
            return day_labels[i]
    return day_labels[-1]
```

### Image-Based Color Detection (Fallback)

If vector extraction doesn't yield colors reliably:

```python
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

images = convert_from_path("/root/calendar.pdf", dpi=200)
img = np.array(images[0])

# Check pixel color at specific coordinates
# Blue pixels: high B channel, low R and G
blue_mask = (img[:,:,2] > 150) & (img[:,:,0] < 100) & (img[:,:,1] < 100)
```

### Tips
- PDF coordinate systems typically have origin at bottom-left, but `pdfplumber` uses top-left
- Always verify coordinate system by cross-referencing text positions with known labels
- Account for small floating-point differences when comparing positions
- Group nearby horizontal lines that might be duplicates (borders vs grid lines)