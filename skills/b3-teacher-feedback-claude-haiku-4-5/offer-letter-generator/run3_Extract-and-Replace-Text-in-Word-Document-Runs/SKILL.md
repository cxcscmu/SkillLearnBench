---
name: Extract and Replace Text in Word Document Runs
description: Use this skill to safely find and replace placeholder text in Word document paragraphs at the run level. This handles cases where placeholder text is split across multiple runs, which is common in Word documents and breaks simple string replacement.
---

## Why This Matters

Word documents store text in "runs" — segments with the same formatting. A placeholder like `{{CANDIDATE_FULL_NAME}}` might be split as:
- Run 1: `{{CAND`
- Run 2: `IDATE_FULL`
- Run 3: `_NAME}}`

Direct `.replace()` on `paragraph.text` won't find it.

## Algorithm

```
def replace_placeholders_in_text(paragraph, replacements_dict):
    # Reconstruct full text from all runs
    full_text = ''.join(run.text for run in paragraph.runs)
    
    # Apply all replacements to the full text
    for pattern, value in replacements_dict.items():
        full_text = re.sub(pattern, str(value), full_text)
    
    # Clear all runs
    for run in paragraph.runs:
        run.text = ""
    
    # If paragraph has no runs, create one
    if not paragraph.runs:
        paragraph.add_run(full_text)
    else:
        # Add full text to first run only
        paragraph.runs[0].text = full_text
```

## Key Details

- Use regex patterns for placeholders: `r'{{PLACEHOLDER_NAME}}'`
- Always reconstruct from all runs first—never iterate and modify runs simultaneously
- Escape literal dots in regex (e.g., `\.` not `.`)
- Return `True` if any replacement was made (useful for tracking)