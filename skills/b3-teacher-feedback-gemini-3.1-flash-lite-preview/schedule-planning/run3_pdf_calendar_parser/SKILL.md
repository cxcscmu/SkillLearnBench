---
name: pdf_calendar_parser
description: Parses /root/calendar.pdf to extract appointment timings, color-coded blocks, and time-axis mappings using pdfplumber.
---

1. **Initialize PDF Analysis**: Use `pdfplumber` to open `/root/calendar.pdf`. Iterate through pages to extract both text objects (to locate time labels) and graphical shapes (to identify rectangles).
2. **Calculate Scaling**: Identify horizontal lines in the PDF. Calculate `pixels_per_15min` by measuring the vertical distance between two consecutive horizontal time-marker lines. 
3. **Map Coordinates to Time**:
    - Extract the text timestamps (e.g., "09:00 AM", "09:15 AM") and their corresponding Y-coordinates.
    - Create a reference dictionary mapping Y-offsets to absolute time.
    - Calculate the start time of the calendar grid based on the top-most time label.
4. **Identify Appointments and Colors**:
    - Extract rectangles from `page.rects`. Access `rect['non_stroking_color']` or `rect['stroking_color']` to identify color properties.
    - Classify rectangles: if color is blue (check for specific RGB/CMYK values representing the "low-priority" color), tag as `flexible`. Otherwise, tag as `busy`.
    - Convert rectangle Y-coordinates into `start_time` and `end_time` using the `pixels_per_15min` ratio.
5. **Output**: Return a list of objects containing `start`, `end`, and `is_flexible` (boolean) for each block.