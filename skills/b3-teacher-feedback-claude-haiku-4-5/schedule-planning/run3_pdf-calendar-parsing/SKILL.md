---
name: pdf-calendar-parsing
description: Extracts calendar structure, time slots, existing appointments, and timezone from a PDF calendar document. Maps pixel positions to actual times using axis labels, identifies appointment blocks with their colors, and determines which dates are covered by the calendar.
---

# PDF Calendar Parsing

## Inputs
- `calendar_pdf_path`: string, path to `/root/calendar.pdf`
- `today_date`: string, today's date in YYYY-MM-DD format (for context)

## Outputs
- `calendar_metadata`: object containing:
  - `timezone`: string (e.g., "EST", "UTC", "PST")
  - `dates_covered`: list of dates in YYYY-MM-DD format shown on calendar
  - `time_axis_range`: {start_time, end_time} in HH:MM format
  - `slot_duration_minutes`: integer (typically 15)
- `appointments`: list of objects, each containing:
  - `date`: YYYY-MM-DD
  - `start_time`: HH:MM (24-hour format)
  - `end_time`: HH:MM (24-hour format)
  - `title`: string
  - `color`: string ("blue", "red", "green", etc.)
  - `is_flexible`: boolean (true if blue/flexible block)

## Algorithm

### 1. Extract Calendar Metadata
- Use `pdfplumber` to load the PDF and inspect pages
- Search for timezone indicator in document text (look for patterns like "EST", "PST", "UTC", timezone label in header/footer)
- If timezone not found as text, default to "UTC" and flag as inferred
- Extract all text labels from calendar axes:
  - **Time axis (vertical)**: Read all time labels (e.g., "9:00 AM", "9:15 AM") from left margin or axis; record pixel y-coordinates for each
  - **Date axis (horizontal)**: Read all date/day labels from top/header; record pixel x-coordinates for each
- Build lookup tables: pixel_y → time and pixel_x → date
- Calculate `slot_duration_minutes` from difference between consecutive axis time labels divided by their pixel distance

### 2. Extract Calendar Dimensions & Gridlines
- Identify calendar grid bounds (top-left to bottom-right corners in pixels)
- Extract all horizontal and vertical lines from the PDF using `pdfplumber`'s line extraction
- Filter to only lines within calendar bounds
- Record pixel positions of gridlines

### 3. Extract Appointments with Color Detection
- Use `pdfplumber.objects` to find all rectangles/shapes within calendar bounds
- For each rectangle, extract:
  - **Position**: x0, y0 (top-left), x1, y1 (bottom-right) in pixels
  - **Color**: Use `fill` or `stroke` RGB values from the rectangle object
    - If RGB values present, convert to color name:
      - Blue-ish (high B, low R/G): `color = "blue"`, `is_flexible = true`
      - Red-ish (high R): `color = "red"`, `is_flexible = false`
      - Other: extract as-is, assume `is_flexible = false`
    - If color data unavailable, check if rectangle has `fill=None` (outline only) vs. filled
- Map pixel coordinates to calendar time/date:
  - Use pixel_y → time lookup to get start_time and end_time
  - Use pixel_x → date lookup to get date
  - Round times to nearest slot_duration_minutes boundary
- Extract appointment title/label from text within or near the rectangle
- Store in `appointments` list

### 4. Validate and Return
- Ensure all appointments have valid start_time < end_time
- Ensure all dates are within dates_covered range
- Return structured metadata and appointments list