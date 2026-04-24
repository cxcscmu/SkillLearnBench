---
name: docx-conditional-sections
description: Handle {{IF_CONDITION}}...{{END_IF_CONDITION}} conditional blocks in Word templates — keep content and strip markers when true, remove entire block when false.
---

# Conditional Sections in Word Templates

## Pattern

Templates use markers like:

```
{{IF_RELOCATION}}You are eligible for a relocation package...{{END_IF_RELOCATION}}
```

Rules:
- **Condition is true**: Keep the content between markers, remove the markers themselves.
- **Condition is false**: Remove the entire block including markers.

## Cases to Handle

Conditional blocks may span:
1. **Single paragraph** — start and end markers are in the same paragraph
2. **Multiple paragraphs** — start marker in one paragraph, end marker in another

## Single-Paragraph Conditional

```python
import re

def handle_single_para_conditional(para, condition_key, should_include, data):
    """Handle {{IF_KEY}}...{{END_IF_KEY}} within a single paragraph."""
    start = '{{IF_' + condition_key + '}}'
    end = '{{END_IF_' + condition_key + '}}'

    text = para.text
    if start not in text or end not in text:
        return False  # Not applicable

    if should_include:
        # Strip markers, keep content, then replace placeholders
        inner = re.search(re.escape(start) + r'(.*?)' + re.escape(end), text, re.DOTALL)
        new_text = inner.group(1) if inner else text.replace(start, '').replace(end, '')
        # Replace any remaining placeholders in the content
        new_text = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: str(data.get(m.group(1), m.group(0))), new_text)
    else:
        new_text = ''

    if para.runs:
        para.runs[0].text = new_text
        for run in para.runs[1:]:
            run.text = ''
    return True
```

## Multi-Paragraph Conditional

When markers span multiple paragraphs, collect and process paragraph-by-paragraph:

```python
from docx.oxml.ns import qn

def remove_paragraph(para):
    """Remove a paragraph element from the document."""
    p = para._element
    p.getparent().remove(p)

def handle_multi_para_conditional(doc, condition_key, should_include, data):
    """Handle conditional block that may span multiple paragraphs."""
    start_marker = '{{IF_' + condition_key + '}}'
    end_marker = '{{END_IF_' + condition_key + '}}'

    paragraphs = list(doc.paragraphs)
    inside = False
    to_remove = []

    for para in paragraphs:
        text = para.text
        starts = start_marker in text
        ends = end_marker in text

        if starts and ends:
            # Entire block in one paragraph
            handle_single_para_conditional(para, condition_key, should_include, data)
        elif starts:
            inside = True
            if not should_include:
                to_remove.append(para)
            else:
                # Strip start marker
                new_text = text.replace(start_marker, '')
                if para.runs:
                    para.runs[0].text = new_text
                    for run in para.runs[1:]: run.text = ''
        elif ends:
            inside = False
            if not should_include:
                to_remove.append(para)
            else:
                new_text = text.replace(end_marker, '')
                if para.runs:
                    para.runs[0].text = new_text
                    for run in para.runs[1:]: run.text = ''
        elif inside:
            if not should_include:
                to_remove.append(para)

    for para in to_remove:
        remove_paragraph(para)
```

## Determining Condition Value

Usually driven by a field in the data:

```python
should_include = data.get('RELOCATION_PACKAGE', '').lower() == 'yes'
handle_multi_para_conditional(doc, 'RELOCATION', should_include, data)
```

## Order of Operations

Always handle conditional sections **before** general placeholder replacement to avoid replacing placeholders inside blocks that will be removed.
