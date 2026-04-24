---
name: run2_docx-conditional-sections
description: Handle {{IF_X}}...{{END_IF_X}} conditional blocks in Word .docx templates — keep or remove content, with correct ordering relative to placeholder replacement.
---

# Conditional Section Handling in Word Templates (Improved)

## Pattern

Templates use conditional blocks like:

```
{{IF_RELOCATION}}You qualify for a ${{RELOCATION_AMOUNT}} relocation package for {{RELOCATION_DAYS}} days.{{END_IF_RELOCATION}}
```

## Critical: Process Conditionals BEFORE General Placeholder Replacement

Conditionals must be resolved first because:
1. The inner content may contain placeholders (e.g., `{{RELOCATION_AMOUNT}}`) that need
   to be replaced only if the section is kept.
2. If you replace placeholders first and then try to remove the section, the markers
   remain and the content is already substituted in.

## Step 1: Inspect the Template

Always inspect before coding — the marker positions affect which handler to use:

```python
from docx import Document

doc = Document('template.docx')
for i, para in enumerate(doc.paragraphs):
    if 'IF_' in para.text or 'END_IF' in para.text:
        print(f'Para[{i}]: {repr(para.text)}')
        for j, run in enumerate(para.runs):
            print(f'  Run[{j}]: {repr(run.text)}')
```

## Case A: Same Paragraph (markers + content in one paragraph)

Identified when `para.text` contains both `{{IF_X}}` and `{{END_IF_X}}`.

```python
def handle_conditional_same_para(para, condition_key, should_include, data):
    """
    Handle a conditional block that is entirely within one paragraph.

    Word may put markers in separate runs, but para.text concatenates them,
    so string slicing on para.text works correctly.
    """
    start = '{{IF_' + condition_key + '}}'
    end = '{{END_IF_' + condition_key + '}}'
    text = para.text

    if start not in text or end not in text:
        return False

    if should_include:
        # Extract content between markers
        inner_start = text.index(start) + len(start)
        inner_end = text.index(end)
        inner = text[inner_start:inner_end]

        # Replace any placeholders inside the conditional content
        for key, value in data.items():
            inner = inner.replace('{{' + key + '}}', str(value))

        # Reconstruct: prefix + resolved_inner + suffix
        prefix = text[:text.index(start)]
        suffix = text[text.index(end) + len(end):]
        new_text = prefix + inner + suffix
    else:
        new_text = ''

    # Write back — collapse all runs into run[0]
    if para.runs:
        para.runs[0].text = new_text
        for run in para.runs[1:]:
            run.text = ''
    return True
```

## Case B: Multi-Paragraph Block (markers on separate lines)

Identified when markers are in different paragraphs.

```python
def handle_conditional_multi_para(doc, condition_key, should_include, data):
    """
    Handle a conditional block spanning multiple paragraphs.

    Note: Clearing runs leaves empty paragraphs (blank lines). To fully remove
    paragraphs from the document XML, use the lxml approach shown below.
    """
    start = '{{IF_' + condition_key + '}}'
    end = '{{END_IF_' + condition_key + '}}'

    paras = doc.paragraphs
    start_idx = next((i for i, p in enumerate(paras) if start in p.text), None)
    end_idx = next((i for i, p in enumerate(paras) if end in p.text), None)

    if start_idx is None or end_idx is None:
        return

    if should_include:
        # Remove marker paragraphs, keep inner content
        _clear_para(paras[start_idx])
        _clear_para(paras[end_idx])
        # Replace placeholders in inner paragraphs
        for para in paras[start_idx + 1:end_idx]:
            text = para.text
            for key, value in data.items():
                text = text.replace('{{' + key + '}}', str(value))
            if text != para.text and para.runs:
                para.runs[0].text = text
                for run in para.runs[1:]:
                    run.text = ''
    else:
        # Clear all paragraphs including markers and content
        for para in paras[start_idx:end_idx + 1]:
            _clear_para(para)

def _clear_para(para):
    """Empty all runs in a paragraph (leaves blank line in document)."""
    for run in para.runs:
        run.text = ''
```

## Auto-Detection and Dispatch

```python
def handle_conditional(doc, condition_key, should_include, data):
    """Auto-detect single vs multi-paragraph conditional and handle accordingly."""
    start = '{{IF_' + condition_key + '}}'
    end = '{{END_IF_' + condition_key + '}}'

    for para in doc.paragraphs:
        if start in para.text and end in para.text:
            # Same paragraph case
            handle_conditional_same_para(para, condition_key, should_include, data)
            return
        elif start in para.text or end in para.text:
            # Multi-paragraph case
            handle_conditional_multi_para(doc, condition_key, should_include, data)
            return
```

## Complete Example

```python
import json
from docx import Document

with open('employee_data.json') as f:
    data = json.load(f)

doc = Document('template.docx')

# Step 1: Handle all conditional sections
relocation_yes = data.get('RELOCATION_PACKAGE', '').strip().lower() == 'yes'
handle_conditional(doc, 'RELOCATION', relocation_yes, data)

# Step 2: Replace remaining placeholders (see run2_python-docx-placeholders skill)
for para in doc.paragraphs:
    replace_in_paragraph(para, data)
# ... tables, headers, footers ...

doc.save('output.docx')
```

## Key Insights from Real Templates

- Even in the "same paragraph" case, the markers (`{{IF_X}}`, `{{END_IF_X}}`) are
  often in **separate runs**. This is fine because we use `para.text` for detection
  and string slicing — run structure doesn't matter.
- The `{{RELOCATION_PACKAGE}}` key in `data` is a flag field (value `"Yes"`/`"No"`),
  not a placeholder in the template. Check it separately to decide `should_include`.
- Always test with `RELOCATION_PACKAGE = "No"` case too.
