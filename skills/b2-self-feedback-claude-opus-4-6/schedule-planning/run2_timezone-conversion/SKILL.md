---
name: run2_timezone-conversion
description: Convert between US time zones for scheduling, defaulting unspecified zones to calendar timezone.
---

# US Timezone Conversion for Scheduling

## Standard Offsets (from UTC)
| Zone | Offset |
|------|--------|
| EST  | UTC-5  |
| CST  | UTC-6  |
| MST  | UTC-7  |
| PST  | UTC-8  |

## Rules
1. If email specifies a timezone (e.g., "PST"), convert to calendar timezone.
   - PST to EST: add 3 hours. Example: 1:00 PM PST = 4:00 PM EST.
2. If email does NOT specify timezone, assume calendar timezone (Eastern in this case).
3. All reply times MUST be in calendar timezone.
4. Be aware of DST: March 9, 2026 is after spring-forward (March 8, 2026), so Eastern = EDT (UTC-4) and Pacific = PDT (UTC-7). However, if the email says "PST" explicitly, honor the stated zone.

## DST Note for March 9, 2026
- DST spring forward is March 8, 2026. After this, Eastern is EDT (UTC-4) and Pacific is PDT (UTC-7).
- But the calendar header says "Eastern Time" which covers both EST/EDT automatically.
- If email says "PST" (not "PDT" or "PT"), the difference is still 3 hours from Eastern Time on this date (EDT=UTC-4, PST=UTC-8 → 4 hours... but this is unusual since PST isn't observed in March).
- Conservative approach: treat "PST" as "Pacific Time" = PDT on this date = UTC-7, so difference to EDT = 3 hours.
