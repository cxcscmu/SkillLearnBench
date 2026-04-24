---
name: email_request_parser
description: Extracts meeting requirements from /root/test_input.json, handling variable constraints and field parsing.
---

1. **Load Data**: Read `/root/test_input.json`.
2. **Extraction Logic**: Iterate through each email entry. 
    - Extract `messageID` and `sender_email`.
    - Parse the body to find `meeting_duration` (standardize to hours/minutes).
    - Parse constraints: Look for patterns indicating specific date preferences (e.g., "next Tuesday", "after 2 PM").
3. **Normalization**: Return a structured list of requests, mapping each to a required duration and a list of forbidden/preferred time windows based on the input text.