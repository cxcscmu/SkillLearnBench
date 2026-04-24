---
name: extract-request-details
description: Parses email messages from JSON input file to extract meeting duration, date constraints, time-of-day constraints, and recipient contact information for each meeting request.
---

# Extract Request Details

## Inputs
- `input_json_path`: string, path to `/root/test_input.json`
- `today_date`: string, today's date in YYYY-MM-DD format

## Outputs
- `requests`: list of objects, each containing:
  - `message_id`: string (unique identifier)
  - `recipient_email`: string
  - `duration_minutes`: integer
  - `date_constraint`: object with:
    - `type`: string ("specific_date", "date_range", "day_of_week", "relative", "none")
    - `start_date`: YYYY-MM-DD (or null if no constraint)
    - `end_date`: YYYY-MM-DD (or null if single date or none)
    - `day_names`: list of strings (e.g., ["Monday", "Tuesday"]) if recurring day constraint
    - `relative_offset_days`: integer (e.g., 1 for "tomorrow", 0 for "today")
  - `time_constraint`: object with:
    - `type`: string ("specific_time", "time_window", "time_of_day", "none")
    - `start_time`: HH:MM (24-hour) or null
    - `end_time`: HH:MM (24-hour) or null
    - `period`: string ("morning", "afternoon", "evening") or null
  - `raw_email_body`: string (original message text)

## Algorithm

### 1. Load and Parse JSON
- Read `/root/test_input.json`
- Validate JSON structure; expect array of email objects
- For each email, extract: `message_id`, `from` (or `sender_email`), `subject`, `body` (or `message_body`)

### 2. Parse Duration
- Search email body for patterns:
  - "X hour" → `duration_minutes = X * 60`
  - "X minute" → `duration_minutes = X`
  - "X min" → `duration_minutes = X`
  - "30 mins", "1.5 hours" → parse decimal
  - "half hour" → `duration_minutes = 30`
  - If no duration found, flag as error and set `duration_minutes = null`

### 3. Parse Date Constraint
- Search for date/day patterns in body:
  - **Specific date**: "January 8", "Jan 8, 2026", "01/08/2026"
    - Parse and normalize to YYYY-MM-DD
    - If year omitted, apply year inference logic (see below)
    - Type: "specific_date", set start_date = end_date
  - **Date range**: "Jan 5-7", "January 5 to 7", "between Jan 5 and Jan 8"
    - Type: "date_range", extract start_date and end_date
    - Apply year inference if needed
  - **Day of week**: "next Monday", "any Tuesday or Wednesday", "Mondays"
    - Type: "day_of_week", populate day_names list
    - Set relative_offset_days if "next" or "this" qualifier present
  - **Relative**: "tomorrow", "next week", "in 3 days"
    - Type: "relative", calculate offset from today_date
  - **None found**: type = "none", all date fields null

### 4. Parse Time Constraint
- Search for time patterns in body:
  - **Specific time**: "9:00 AM", "14:30", "2:30 PM"
    - Type: "specific_time", set start_time, set end_time = null (will be calculated from duration)
  - **Time window**: "9:00 AM - 10:30 AM", "between 2 PM and 4 PM"
    - Type: "time_window", extract start_time and end_time
  - **Time of day**: "morning", "afternoon", "evening", "before noon", "after 5 PM"
    - Type: "time_of_day", extract period or convert to approximate start_time/end_time:
      - Morning: 06:00 - 12:00
      - Afternoon: 12:00 - 17:00
      - Evening: 17:00 - 21:00
  - **None found**: type = "none", all time fields null

### 5. Year Inference Logic
- If a date is parsed without a year (e.g., "January 8"):
  - Extract month and day from parsed date
  - If (month, day) >= (today_date.month, today_date.day), assume current year
  - Else, assume next year
  - Example: if today is 2026-01-15, "January 8" → 2027-01-08; "January 20" → 2026-01-20

### 6. Extract Recipient Email
- Use `from`, `sender_email`, or `sender` field from JSON object
- Validate format (should contain "@")

### 7. Return Results
- Compile all requests into list and return