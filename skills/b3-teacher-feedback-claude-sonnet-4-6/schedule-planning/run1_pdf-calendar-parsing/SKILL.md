---
name: pdf-calendar-parsing
description: Use this skill to extract visual calendar data from a PDF file using PyMuPDF (fitz), including reading text for time labels and appointments, detecting colored rectangular blocks, and measuring their vertical positions to determine start/end times based on a 15-minute-per-row grid.
---

## Parsing a Visual Calendar PDF with PyMuPDF

### Installation
```bash
pip install pymupdf
```

### Core Approach
The calendar is a visual grid where:
- Horizontal lines divide time into 15-minute slots
- Appointments are colored rectangular blocks spanning one or more slots
- Time labels (e.g., "9:00 AM") appear along a vertical axis
- **Blue blocks** = low-priority/flexible, treat as free time

### Step 1: Open PDF and Extract Page

```python
import fitz  # PyMuPDF

doc = fitz.open('/root/calendar.pdf')
page = doc[0]  # Usually single page

# Get page dimensions
width = page.rect.width
height = page.rect.height
print(f"Page size: {width} x {height}")
```

### Step 2: Extract All Drawn Rectangles/Blocks

```python
def get_colored_blocks(page):
    """Extract filled rectangles with their colors and positions."""
    blocks = []
    
    # Get drawing paths/shapes
    drawings = page.get_drawings()
    
    for drawing in drawings:
        rect = drawing.get('rect')
        fill = drawing.get('fill')  # RGB tuple or None
        color = drawing.get('color')  # stroke color
        
        if rect and fill:
            blocks.append({
                'rect': rect,  # fitz.Rect: (x0, y0, x1, y1)
                'fill': fill,  # (r, g, b) floats 0-1
                'x0': rect.x0, 'y0': rect.y0,
                'x1': rect.x1, 'y1': rect.y1,
                'width': rect.width,
                'height': rect.height,
            })
    
    return blocks
```

### Step 3: Detect Blue Blocks

```python
def is_blue(fill_color):
    """Detect blue fill color. fill_color is (r, g, b) with values 0-1."""
    if fill_color is None:
        return False
    r, g, b = fill_color
    # Blue: high blue channel, lower red and green
    return b > 0.4 and b > r + 0.15 and b > g + 0.05

def classify_blocks(blocks):
    for block in blocks:
        block['is_blue'] = is_blue(block.get('fill'))
        block['is_appointment'] = not block['is_blue']  # adjust as needed
    return blocks
```

### Step 4: Extract Text with Positions

```python
def get_text_with_positions(page):
    """Get all text spans with their bounding boxes."""
    text_data = []
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if block.get("type") == 0:  # text block
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text_data.append({
                        'text': span['text'].strip(),
                        'bbox': span['bbox'],  # (x0, y0, x1, y1)
                        'y_center': (span['bbox'][1] + span['bbox'][3]) / 2,
                        'x0': span['bbox'][0],
                    })
    return text_data
```

### Step 5: Build Timeline from Horizontal Lines

```python
def extract_horizontal_lines(page):
    """Get Y-coordinates of all horizontal lines (grid lines)."""
    y_coords = set()
    drawings = page.get_drawings()
    
    for d in drawings:
        # Lines have 'items' list with ('l', p1, p2) for line segments
        for item in d.get('items', []):
            if item[0] == 'l':  # line
                p1, p2 = item[1], item[2]
                # Horizontal if y-coords are nearly equal
                if abs(p1.y - p2.y) < 2:
                    y_coords.add(round(p1.y, 1))
    
    return sorted(y_coords)
```

### Step 6: Map Y-Position to Time

```python
def build_time_map(h_lines, time_labels):
    """
    h_lines: sorted list of Y-coordinates for horizontal grid lines
    time_labels: list of {'text': '9:00 AM', 'y_center': float}
    Each interval between adjacent lines = 15 minutes.
    """
    from datetime import datetime, timedelta
    import re
    
    # Parse time labels and match to nearest h_line
    label_map = {}  # y_coord -> parsed time
    for label in time_labels:
        text = label['text']
        # Match time patterns like "9:00", "9:00 AM", "09:00"
        match = re.match(r'(\d{1,2}):(\d{2})\s*(AM|PM)?', text, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            ampm = match.group(3)
            if ampm:
                if ampm.upper() == 'PM' and hour != 12:
                    hour += 12
                elif ampm.upper() == 'AM' and hour == 12:
                    hour = 0
            # Find nearest h_line
            nearest = min(h_lines, key=lambda y: abs(y - label['y_center']))
            label_map[nearest] = (hour, minute)
    
    # Fill in remaining lines using 15-min intervals
    if not label_map:
        return {}
    
    # Sort known anchors
    anchors = sorted(label_map.items())
    full_map = {}
    
    # Use first anchor and count lines from there
    anchor_y, anchor_time = anchors[0]
    anchor_idx = h_lines.index(anchor_y)
    base_dt = datetime(2000, 1, 1, anchor_time[0], anchor_time[1])
    
    for i, y in enumerate(h_lines):
        offset_slots = i - anchor_idx
        slot_time = base_dt + timedelta(minutes=15 * offset_slots)
        full_map[y] = slot_time
    
    return full_map  # y_coord -> datetime (time only meaningful)
```

### Step 7: Determine Appointment Times

```python
def get_appointment_times(block, h_lines, time_map, calendar_date):
    """Convert a block's y0/y1 to start/end times."""
    from datetime import date, datetime, timedelta
    
    # Find the grid line at or just above block top (y0)
    start_y = min(h_lines, key=lambda y: abs(y - block['y0']))
    end_y = min(h_lines, key=lambda y: abs(y - block['y1']))
    
    start_dt = time_map.get(start_y)
    end_dt = time_map.get(end_y)
    
    if start_dt and end_dt:
        return {
            'start': start_dt.time(),
            'end': end_dt.time(),
            'is_blue': block['is_blue'],
        }
    return None
```

### Step 8: Extract Date Headers from Calendar

```python
def extract_calendar_dates(text_data):
    """Find date headers like 'Monday, Jan 6' or 'Mon 1/6' in the calendar."""
    import re
    from datetime import datetime
    
    dates = []
    date_patterns = [
        r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+'
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})',
        r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\d{1,2})/(\d{1,2})',
    ]
    
    for item in text_data:
        for pattern in date_patterns:
            match = re.search(pattern, item['text'], re.IGNORECASE)
            if match:
                dates.append({
                    'text': match.group(0),
                    'x0': item['x0'],
                    'y': item['y_center'],
                })
    return dates
```

### Complete Pipeline

```python
def parse_calendar(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    colored_blocks = get_colored_blocks(page)
    classified_blocks = classify_blocks(colored_blocks)
    text_items = get_text_with_positions(page)
    h_lines = extract_horizontal_lines(page)
    
    # Filter time labels (typically on left margin, x < some threshold)
    time_labels = [t for t in text_items if t['x0'] < 100]  # adjust threshold
    
    time_map = build_time_map(h_lines, time_labels)
    date_headers = extract_calendar_dates(text_items)
    
    appointments = []
    for block in classified_blocks:
        times = get_appointment_times(block, h_lines, time_map, None)
        if times:
            appointments.append(times)
    
    return appointments, date_headers, time_map, h_lines
```

### Notes
- `fitz.Rect` coordinates: y increases downward
- Always sort h_lines ascending (top to bottom = earlier to later time)
- Blocks with `fill` matching blue hues are overwritable
- Text extraction via `get_text("dict")` preserves spatial info
- The calendar timezone is read from text labels in the PDF