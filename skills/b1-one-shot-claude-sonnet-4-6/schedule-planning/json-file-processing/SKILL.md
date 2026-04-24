---
name: json-file-processing
description: Read input JSON files with email requests and write results.json with reply filenames and recipients.
---

# JSON File Processing for Meeting Scheduler

## Reading Input
```python
import json

with open("/root/test_input.json") as f:
    emails = json.load(f)

# Each item has: email_text, from_email
for i, email in enumerate(emails, start=1):
    msg_id = i
    text = email["email_text"]
    sender = email["from_email"]
```

## Writing Reply Files
```python
def save_reply(msg_id, content):
    filename = f"/root/reply_{msg_id}.txt"
    with open(filename, "w") as f:
        f.write(content)
    return f"reply_{msg_id}.txt"
```

## Writing results.json
```python
results = {
    "sent_results": [
        {"filename": f"reply_{msg_id}.txt", "recipient": sender}
        for msg_id, sender in ...
    ]
}
with open("/root/results.json", "w") as f:
    json.dump(results, f, indent=2)
```

## Date Formatting Rules
- Day name: full name, e.g. "Monday"
- Month: full name, e.g. "March"
- Day: zero-padded two digits, e.g. "09"
- Year: four digits, e.g. "2026"
- Example: "Monday, March 09, 2026"

## Time Formatting Rules
- Hours: zero-padded two digits, e.g. "09", "10", "11"
- Minutes: zero-padded two digits, e.g. "00", "30"
- Period: "AM" or "PM"
- Example: "09:00 AM - 10:30 AM"
