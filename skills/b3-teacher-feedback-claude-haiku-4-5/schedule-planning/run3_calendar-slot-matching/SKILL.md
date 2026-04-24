---
name: calendar-slot-matching
description: Matches each meeting request against available calendar slots, respecting date and time constraints, and prioritizing flexible (blue) blocks for overwriting. Selects the earliest available slot that accommodates the meeting.
---

# Calendar Slot Matching

## Inputs
- `requests`: list of request objects (from extract-request-details)
- `calendar_metadata`: object with timezone, dates_covered, time_axis_range, slot_duration_minutes
- `appointments`: list of appointment objects (from pdf-calendar-parsing)
- `today_date`: string, today's date in YYYY-MM-DD format

## Outputs
- `matched_slots`: list of objects, each containing:
  - `message_id`: string
  - `proposed_date`: YYYY-MM-DD
  - `proposed_start_time`: HH:MM (24-hour)
  - `proposed_end_time`: HH:MM (24-hour)
  - `duration_minutes`: integer
  - `conflict_status`: string ("no_conflict", "overwrites_flexible", "failed_to_match")
  - `failure_reason`: string (if conflict_status = "failed_to_match")

## Algorithm

### 1. For Each Request (Sequential Processing)
- Process requests in the order provided
- Each request is matched against the current state of appointments
- When a slot is successfully matched, append to appointments list immediately (so subsequent requests see it as booked)

### 2. Determine Candidate Date Range
- Start with request's date_constraint:
  - **specific_date**: candidate_dates = [start_date]
  - **date_range**: candidate_dates = all dates from start_date to end_date (inclusive)
  - **day_of_week**: candidate_dates = next N occurrences of those day names within calendar span, starting from today_date or relative_offset_date
  - **relative**: candidate_dates = [today_date + relative_offset_days]
  - **none**: candidate_dates = all dates in calendar_metadata.dates_covered starting from today_date onwards
- Intersect with calendar_metadata.dates_covered to ensure dates are available in calendar

### 3. Determine Candidate Time Window
- Start with request's time_constraint:
  - **specific_time**: window_start = start_time, window_end = start_time + duration_minutes (rounded to slot boundary)
  - **time_window**: window_start = start_time, window_end = end_time
  - **time_of_day**: 
    - Period "morning" → window_start = 06:00, window_end = 12:00
    - Period "afternoon" → window_start = 12:00, window_end = 17:00
    - Period "evening" → window_start = 17:00, window_end = 21:00
  - **none**: window_start = calendar_metadata.time_axis_range.start_time, window_end = calendar_metadata.time_axis_range.end_time
- Clamp window to calendar operating hours if necessary

### 4. Generate Candidate Slots
- For each candidate date (in order, earliest first):
  - For each 15-minute slot boundary within candidate time window:
    - Candidate slot = [date, slot_start_time, slot_start_time + duration_minutes]
    - Check if this slot fits within calendar operating hours and time window
- Sort candidate slots chronologically

### 5. Check Each Candidate Slot Against Current Appointments
- For each candidate slot:
  - Find all appointments that overlap (same date, time ranges intersect)
  - Categorize overlaps:
    - `no_conflict`: no overlapping appointments → **MATCH FOUND**, record and break
    - `overwrites_flexible`: all overlaps have is_flexible = true → **MATCH FOUND** (note conflict_status), remove flexible appointments, record, break
    - `has_fixed_conflict`: at least one overlap has is_flexible = false → continue to next candidate slot
- If no candidate slot found after checking all:
  - Return failure with reason: "No available slots within constraints"

### 6. Record Matched Slot
- Add matched slot to matched_slots list
- Create a synthetic appointment object and add to appointments list (to block this slot for future requests):
  - date, start_time, end_time from matched slot
  - title = f"Meeting: {message_id}"
  - color = "green" (booked)
  - is_flexible = false
- Continue to next request

### 7. Return Results
- Return matched_slots list