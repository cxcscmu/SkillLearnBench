---
name: meeting-response-formatting
description: Generate properly formatted meeting confirmation emails and save results. This skill handles creating reply text files with exact formatting (date format with day name and full date, time format with leading zeros), generating results.json with metadata, and ensuring compliance with the response template. Use this whenever you need to format meeting confirmations or generate scheduled meeting documentation.
---

# Meeting Response Formatting

## Overview

This skill generates properly formatted meeting replies and tracks results by:
- Creating text files with consistent template format
- Using correct date formatting (day name, month, date with leading zeros)
- Using correct time formatting (24-hour or 12-hour with leading zeros)
- Generating results.json with filenames and recipient info

## Response Template

Each reply file should use this exact template:

```
Hi,

Thank you for your meeting request.

I can be available:

Date: {day_name}, {month} {DD}, {YYYY}
Time: {HH:MM AM/PM} - {HH:MM AM/PM}
Duration: {meetingDuration} hour(s)

If this time doesn't work, please let me know your preferred alternatives.

Best regards,
ConSkillBench
```

## Date Formatting Rules

**Format**: `{day_name}, {month} {DD}, {YYYY}`

**Requirements**:
- Day name: Full name (Monday, Tuesday, Wednesday, etc.)
- Month: Full name (January, February, March, April, etc.)
- DD: Two-digit day with leading zero (01, 02, ..., 31)
- YYYY: Four-digit year (2026)

**Examples**:
- ✓ Thursday, January 08, 2026
- ✓ Tuesday, March 25, 2026
- ✓ Saturday, December 31, 2026
- ✗ Thursday, January 8, 2026 (missing leading zero)
- ✗ January 8, 2026 (missing day name)
- ✗ January 8th, 2026 (ordinal suffix not allowed)

## Time Formatting Rules

**Format**: `{HH:MM AM/PM} - {HH:MM AM/PM}`

**Requirements**:
- Use 12-hour clock with AM/PM
- HH: Two-digit hour with leading zero (01-12)
- MM: Two-digit minutes with leading zero (00-59)
- Space before and after the hyphen
- Always "AM" or "PM" in capitals

**Examples**:
- ✓ 09:00 AM - 10:30 AM
- ✓ 01:00 PM - 02:00 PM
- ✓ 08:30 AM - 09:00 AM
- ✗ 9:00 AM - 10:30 AM (missing leading zero)
- ✗ 09:00am - 10:30am (lowercase am/pm)
- ✗ 09:00 - 10:30 (missing AM/PM)

## Duration Formatting

**Format**: `{meetingDuration} hour(s)`

**Rules**:
- Use integer or decimal: 1, 0.5, 1.5, 2
- Always include "hour(s)" suffix
- Use "hour" for 1.0, "hours" for anything else

**Examples**:
- ✓ 1 hour(s)
- ✓ 0.5 hour(s)
- ✓ 2 hour(s)

## Generating Reply Files

### Step 1: Prepare Data

Gather for each scheduled meeting:
- messageID (from request)
- recipient email
- scheduled_date, day_name, month, day, year
- start_time (in HH:MM format), end_time
- duration_hours
- timezone (if applicable)

### Step 2: Format Strings

Convert raw data to formatted strings:

1. **Date string**:
   ```
   date_object = parse scheduled_date
   day_name = date_object.strftime("%A")  # Full day name
   month = date_object.strftime("%B")     # Full month name
   DD = date_object.strftime("%d")        # Zero-padded day
   YYYY = date_object.strftime("%Y")      # Year
   date_formatted = f"{day_name}, {month} {DD}, {YYYY}"
   ```

2. **Time strings**:
   ```
   start_12h = convert_24h_to_12h(start_time)  # "09:00 AM"
   end_12h = convert_24h_to_12h(end_time)      # "10:00 AM"
   time_range = f"{start_12h} - {end_12h}"
   ```

3. **Duration string**:
   ```
   duration_text = f"{duration_hours} hour(s)"
   ```

### Step 3: Generate Content

Substitute into template:

```
Hi,

Thank you for your meeting request.

I can be available:

Date: {date_formatted}
Time: {time_range}
Duration: {duration_text}

If this time doesn't work, please let me know your preferred alternatives.

Best regards,
ConSkillBench
```

### Step 4: Save Reply File

Filename format: `reply_{messageID}.txt`

Example: `reply_msg123.txt`

Location: `/root/reply_{messageID}.txt`

### Step 5: Update results.json

For all generated replies, create or update `/root/results.json`:

```json
{
  "sent_results": [
    {
      "filename": "reply_msg123.txt",
      "recipient": "user1@example.com"
    },
    {
      "filename": "reply_msg456.txt",
      "recipient": "user2@example.com"
    }
  ]
}
```

**File format rules**:
- Pretty-print JSON with 2-space indentation
- Include all replies in sent_results array
- Maintain array in order of processing

## 12-Hour Time Conversion

If calendar uses 24-hour format, convert to 12-hour AM/PM:

```
00:00 → 12:00 AM
09:00 → 09:00 AM
12:00 → 12:00 PM
13:00 → 01:00 PM
17:30 → 05:30 PM
23:59 → 11:59 PM
```

## Validation Checklist

Before saving reply files, verify:
- [ ] Day name matches actual day of scheduled date
- [ ] All dates use full month names, not abbreviations
- [ ] All times have leading zeros (HH:MM format)
- [ ] All times use AM/PM, not 24-hour format
- [ ] Duration properly formatted with hour(s) suffix
- [ ] Template structure exactly matches specification
- [ ] Filename format is `reply_{messageID}.txt`
- [ ] results.json is valid JSON format
