---
name: run2_output-generator
description: A refined output generation skill that precisely templates text files and correctly constructs the requested JSON log.
---

# Output and Log Generation

This skill focuses on ensuring strict adherence to formatting templates (e.g., date formats, precise triple-quote templates with specific blank lines).

## Template Matching
```python
def generate_reply(date_str, time_str, duration):
    content = f"""Hi,

Thank you for your meeting request.

I can be available:

Date: {date_str}
Time: {time_str}
Duration: {duration} hour(s)

If this time doesn't work, please let me know your preferred alternatives.

Best regards,
ConSkillBench"""
    return content
```

## Creating Output Directories and Logging Results
When saving the file names back to `results.json`, ensure the dictionary uses the exact required key format (`"sent_results"`).

```python
import json

def log_results(log_path, sent_data):
    # Log sent data
    with open(log_path, "w") as out:
        json.dump({"sent_results": sent_data}, out, indent=2)
```
