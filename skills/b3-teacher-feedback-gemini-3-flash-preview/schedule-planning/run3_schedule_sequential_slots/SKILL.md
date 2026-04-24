---
name: schedule_sequential_slots
description: Find the earliest available meeting slots for multiple requests, treating blue blocks as available and updating the schedule state after each assignment.
---

1. Initialize the calendar state using the data from `analyze_pdf_calendar`. 
2. Define "Available Time" as any slot that is:
   - White space (no block present).
   - Covered by a **blue-colored** flexible block (`RGB 0, 0, 1`).
3. Iterate through the extracted meeting requests in the order they appear in the input:
   - Search for the earliest possible start time that satisfies the duration and constraints of the current request.
   - Ensure the slot does not overlap with any "busy/fixed" blocks.
   - If a slot overlaps with a "blue" block, treat that blue block's time as free.
4. **State Management**: Once a slot is assigned to a request:
   - Mark that specific time range as "Busy" immediately.
   - This slot is now unavailable for all subsequent requests in the loop.
5. Store the resulting assignment (Date, Start Time, End Time, Duration) for each `messageID`.