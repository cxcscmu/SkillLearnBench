---
name: run2_docx-expert
description: Advanced techniques for Word document automation, including handling split runs, headers/footers, and complex conditionals.
---

# Advanced Word Document Automation

## Handling Split Runs
Placeholders like `{{NAME}}` are often split across multiple `Run` objects in `python-docx`. Replacing `paragraph.text` destroys formatting. To preserve formatting, use a function that merges runs or carefully replaces text while keeping properties.

### Safe Replacement Strategy
```python
def replace_text_in_paragraph(paragraph, key, value):
    if key not in paragraph.text:
        return
    
    # Simple strategy: If the placeholder is entirely within one run, replace it there.
    # Otherwise, use paragraph.text but be aware formatting is lost.
    # A better approach for preservation:
    full_text = "".join(run.text for run in paragraph.runs)
    if key in full_text:
        new_text = full_text.replace(key, value)
        # Clear runs and add a single run (loses specific bold/italic if mixed)
        # Or, if formatting is critical, use a more complex run-merging algorithm.
        for i in range(len(paragraph.runs)):
            paragraph.runs[i].text = ""
        paragraph.runs[0].text = new_text
```

## Headers and Footers
Templates often have placeholders in headers/footers.
```python
for section in doc.sections:
    for header_p in section.header.paragraphs:
        # process header_p
    for footer_p in section.footer.paragraphs:
        # process footer_p
```

## Robust Conditionals
If `{{IF_TAG}}` is on its own line, removing the paragraph is correct.
If it is inline, you must use string replacement to remove the tags and content.

```python
def handle_conditional_block(doc, condition, start_tag, end_tag):
    # This implementation assumes tags are on their own paragraphs for simplicity,
    # which is common for "blocks" of text like relocation details.
    delete_mode = False
    paragraphs_to_remove = []
    for p in doc.paragraphs:
        if start_tag in p.text:
            delete_mode = not condition
            paragraphs_to_remove.append(p)
            continue
        if end_tag in p.text:
            delete_mode = False
            paragraphs_to_remove.append(p)
            continue
        if delete_mode:
            paragraphs_to_remove.append(p)
    
    for p in paragraphs_to_remove:
        p._element.getparent().remove(p._element)
```
