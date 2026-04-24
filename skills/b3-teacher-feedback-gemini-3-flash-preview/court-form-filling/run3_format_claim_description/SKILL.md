---
name: format_claim_description
description: Splits a long string of text (like a claim description or reason) into multiple parts that fit into sequential PDF field keys. Use this when the SC-100 form provides multiple lines (e.g., 'Reason_Line1', 'Reason_Line2') for a single explanation.
---

def format_claim_description(text: str, line_length: int, num_lines: int):
    """
    Splits a long text string into a list of strings of roughly equal length 
    to fit into multiple form field lines.
    """
    import textwrap
    # Wrap text to the specified line length
    lines = textwrap.wrap(text, width=line_length)
    
    # Ensure the list matches the number of available field lines
    result = lines[:num_lines]
    while len(result) < num_lines:
        result.append("")
    return result