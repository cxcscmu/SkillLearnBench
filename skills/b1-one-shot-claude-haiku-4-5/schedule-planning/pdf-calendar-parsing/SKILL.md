---
name: pdf-calendar-parsing
description: Extract calendar events, blocks, and time slots from PDF calendar files using pdfplumber
---

# PDF Calendar Parsing Skill

## Overview
This skill covers extracting calendar events and time blocks from PDF calendar documents using `pdfplumber`, a Python library for extracting text and tables from PDF files.

## Installation
```bash
pip install pdfplumber
```

## Key Concepts

### How pdfplumber Works
- Opens PDF files and extracts text with position information
- Can identify text bounding boxes (x0, y0, x1, y1 coordinates)
- Supports extracting tables and structured data

### Calendar Grid Extraction
For a calendar with hourly/time-based layout:
1. Extract all text from the PDF with position data
2. Identify time labels (hours on the left axis)
3. Identify event blocks by text content and bounding boxes
4. Calculate event duration by comparing Y-coordinates

## Code Examples

### Basic PDF Opening
```python
import pdfplumber

with pdfplumber.open('/root/calendar.pdf') as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    print(text)
```

### Extracting Text with Positions
```python
import pdfplumber

with pdfplumber.open('/root/calendar.pdf') as pdf:
    page = pdf.pages[0]

    # Get all text objects with their positions
    for char in page.chars:
        print(f"Text: {char['text']}, X: {char['x0']}, Y: {char['y0']}")
```

### Identifying Calendar Events
```python
import pdfplumber

def extract_calendar_events(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]

        # Get all text with positions
        text_data = page.extract_text_with_layout()

        # Extract words and their bounding boxes
        words = page.extract_words()

        events = []
        for word in words:
            # word contains: 'text', 'x0', 'y0', 'x1', 'y1', 'size', 'font'
            if word['text'] not in ['12am', '1am', '2am']:  # Skip time labels
                events.append({
                    'text': word['text'],
                    'x0': word['x0'],
                    'y0': word['y0'],
                    'x1': word['x1'],
                    'y1': word['y1']
                })

        return events
```

### Time Extraction from Layout
```python
def extract_time_labels(page):
    """Extract hour labels from calendar time axis"""
    words = page.extract_words()
    time_labels = {}

    for word in words:
        text = word['text']
        # Match patterns like "10am", "2pm", "12am"
        if any(text.endswith(suffix) for suffix in ['am', 'pm']):
            y_position = word['y0']  # Vertical position
            time_labels[text] = y_position

    return sorted(time_labels.items(), key=lambda x: x[1])
```

### Calculating Block Duration
```python
def get_block_duration(y_start, y_end, time_lines, interval_minutes=15):
    """
    Calculate duration of a calendar block

    time_lines: list of (time_string, y_position) tuples, sorted by y
    interval_minutes: minutes between adjacent horizontal lines
    """
    # Find which time lines bracket this block
    start_time = None
    end_time = None

    for i, (time_str, y_pos) in enumerate(time_lines):
        if y_pos <= y_start and (i+1 >= len(time_lines) or time_lines[i+1][1] > y_start):
            start_time = time_str
        if y_pos <= y_end and (i+1 >= len(time_lines) or time_lines[i+1][1] >= y_end):
            end_time = time_str

    return start_time, end_time
```

## Common Pitfalls
- Y-coordinates increase downward in PDFs (unlike normal coordinate systems)
- Text extraction might include artifacts or formatting characters
- Font sizes and positions can vary; use threshold matching
- Event blocks may have overlapping text; use grouping strategies

## Best Practices
1. Always verify extracted text against visual inspection
2. Sort time labels by Y-coordinate to create accurate mapping
3. Use relative positioning (Y-coordinates) to determine time ranges
4. Store both start and end times for accuracy
5. Validate extracted times are within expected calendar hours
