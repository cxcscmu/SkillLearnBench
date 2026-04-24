---
name: python-docx-advanced-manipulation
description: Techniques for replacing text placeholders, safely deleting paragraphs, and handling custom multi-paragraph conditionals (like IF/END_IF markers) in Microsoft Word documents using python-docx.
---

# Advanced Word Document Manipulation with `python-docx`

When generating documents like offer letters from templates, you frequently need to replace placeholder text (e.g., `{{CANDIDATE_NAME}}`) and evaluate conditional sections (e.g., showing a relocation package only if applicable). The `python-docx` library is the standard tool for this, but requires specific techniques to handle formatting and paragraph deletion safely.

## 1. Safely Deleting Paragraphs

Unlike adding text, `python-docx` does not have a built-in `paragraph.delete()` method. To properly remove a paragraph (which is essential for removing conditional markers like `{{IF_RELOCATION}}`), you must drop down to the underlying XML element (lxml).

```python
def delete_paragraph(paragraph):
    """Deletes a paragraph safely by removing its XML element."""
    p = paragraph._element
    p.getparent().remove(p)
    paragraph._p = paragraph._element = None
```

## 2. Handling Conditional Sections

Custom conditional sections in a template often span multiple paragraphs and are flanked by markers like `{{IF_CONDITION}}` and `{{END_IF_CONDITION}}`.

To process these:
1. Iterate through all paragraphs.
2. Track whether you are currently "inside" a conditional block.
3. Keep track of paragraphs that need to be deleted (the markers themselves, plus the content if the condition is false).
4. Delete the collected paragraphs at the end.

```python
def process_conditionals(doc, condition_name, keep_content):
    """
    Finds {{IF_<condition_name>}} and {{END_IF_<condition_name>}}.
    Removes the markers. Removes the content in between if keep_content is False.
    """
    start_marker = f"{{{{IF_{condition_name}}}}}"
    end_marker = f"{{{{END_IF_{condition_name}}}}}"
    
    in_conditional = False
    paragraphs_to_delete = []

    for p in doc.paragraphs:
        if start_marker in p.text:
            in_conditional = True
            paragraphs_to_delete.append(p)
            continue
            
        if end_marker in p.text:
            in_conditional = False
            paragraphs_to_delete.append(p)
            continue
            
        if in_conditional and not keep_content:
            paragraphs_to_delete.append(p)

    # Delete the collected paragraphs safely
    for p in paragraphs_to_delete:
        delete_paragraph(p)
```

## 3. Replacing Text Placeholders

Replacing text in `python-docx` can be tricky because Word often splits text into multiple `Run` objects based on spelling checks, minor formatting changes, or save history. `{{PLACEHOLDER}}` might be split into `Run 1: "{{"`, `Run 2: "PLACEHOLDER"`, `Run 3: "}}"`.

A robust hybrid approach attempts to replace text within a single run first (to preserve exact formatting). If the placeholder is split across runs, it falls back to replacing the text at the `Paragraph` level (which resets paragraph formatting to its default style but guarantees the text is replaced).

```python
def replace_placeholder(doc, placeholder, replacement_value):
    """Replaces placeholders in both paragraphs and tables."""
    
    # 1. Process Document Paragraphs
    for p in doc.paragraphs:
        if placeholder in p.text:
            _replace_in_paragraph(p, placeholder, replacement_value)
            
    # 2. Process Tables (Placeholders are often inside table cells)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if placeholder in p.text:
                        _replace_in_paragraph(p, placeholder, replacement_value)

def _replace_in_paragraph(p, placeholder, replacement):
    # Try inline run replacement first (preserves formatting if placeholder is in 1 run)
    for run in p.runs:
        if placeholder in run.text:
            run.text = run.text.replace(placeholder, replacement)
            
    # Fallback: if placeholder spans multiple runs, overwrite the paragraph text
    if placeholder in p.text:
        p.text = p.text.replace(placeholder, replacement)
```

## 4. Putting It Together

When implementing your template filler:
1. Load the document: `doc = Document('template.docx')`
2. Extract your context data (e.g., `json.load(open('data.json'))`)
3. Process conditionals first using the `process_conditionals` function.
4. Replace the standard variables iterating over your key-value pairs using `replace_placeholder`.
5. Save the output: `doc.save('filled_output.docx')`