---
name: analyze_pdf_calendar
description: Parse the calendar PDF to identify existing appointments, flexible blue slots, and the 15-minute grid coordinate mapping.
---

1. Open `/root/calendar.pdf` using a PDF parsing library (e.g., `pdfminer` or `PyMuPDF`).
2. **Timezone Identification**: Search the text content of the PDF for a timezone string (e.g., "PST", "EST", "UTC") to ensure all scheduled times match the document's context.
3. **Coordinate Mapping**:
   - Identify horizontal lines across the calendar timeline.
   - Determine the vertical distance (Δy) between any two adjacent horizontal lines. This distance represents exactly 15 minutes.
   - Establish a reference Y-coordinate for a known time (e.g., the top line of the workday).
4. **Appointment Extraction**:
   - Extract all rectangular path objects/shapes from the PDF.
   - Determine the start and end times of each block by mapping its top and bottom Y-coordinates to the timeline grid.
   - **Color Detection**: Inspect the color metadata for each block. Use the RGB color space. 
     - Blocks with an RGB value of `(0, 0, 1)` (pure blue) are identified as **flexible/low-priority** slots.
     - Blocks of other colors (e.g., grey, red) are identified as **busy/fixed** slots.
5. **Output**: A structured timeline of busy and flexible blocks, the coordinate-to-time ratio, and the detected timezone.