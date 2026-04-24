---
name: extract_meeting_requests
description: Extract meeting duration, constraints, and metadata from the input JSON file containing email requests.
---

1. Read the JSON file at `/root/test_input.json`.
2. For each email entry, extract the following fields:
   - `messageID`: Unique identifier for the email.
   - `sender`: The email address of the requester.
   - `subject`: The subject line.
   - `body`: The content of the email.
3. Parse the `body` and `subject` to identify:
   - **Meeting Duration**: Convert requested time (e.g., "1 hour", "30 minutes") into a float representing hours.
   - **Constraints**: Identify specific date or time requirements (e.g., "after 2 PM", "on Monday").
4. Return a list of request objects for sequential processing.