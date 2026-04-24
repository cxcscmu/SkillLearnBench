---
name: docx_custom_conditional_logic
description: Manually processes non-standard conditional markers like `{{IF_VARIABLE}}` and `{{END_IF_VARIABLE}}` in a Word document. It identifies blocks of text to either retain (removing markers) or delete (removing the block) based on data.
---

When a template uses custom markers (not Jinja2) for conditional logic, use the following manual detection strategy:

1.  **State Tracking**: Maintain a boolean flag (e.g., `is_inside_block`) and a list to collect paragraphs belonging to a conditional section.
2.  **Detection**: Iterate through all paragraphs in the document. 
    *   If a paragraph contains `{{IF_KEY}}`, start tracking. 
    *   If a paragraph contains `{{END_IF_KEY}}`, stop tracking and process the collected block.
3.  **Content Manipulation**:
    *   **Condition Met (e.g., RELOCATION_PACKAGE == "Yes")**: Simply find the paragraphs containing the markers and use `.text.replace()` to remove the `{{IF_...}}` and `{{END_IF_...}}` strings, leaving the content in between intact.
    *   **Condition Not Met**: Identify all paragraphs starting from the one containing the `IF` marker through the one containing the `END_IF` marker. To "remove" them in `python-docx`, you can clear their text (`p.text = ""`) or use internal element removal methods (though clearing text is often sufficient for basic templates).
4.  **Note on Tables**: If conditional markers wrap rows within a table, you must apply this logic while iterating through `table.rows`, checking the text content of the cells.

Example logic:
```python
def handle_conditionals(paragraphs, condition_key, should_keep):
    active = False
    for p in paragraphs:
        if f"{{{{IF_{condition_key}}}}}" in p.text:
            active = True
            p.text = p.text.replace(f"{{{{IF_{condition_key}}}}}", "")
        
        if active and not should_keep:
            # If the condition is false, clear text inside the block
            # Note: The END_IF check happens below to ensure the end marker is also cleared
            pass 

        if f"{{{{END_IF_{condition_key}}}}}" in p.text:
            p.text = p.text.replace(f"{{{{END_IF_{condition_key}}}}}", "")
            active = False
        
        if active and not should_keep:
             p.text = "" # Clear content if condition fails
```