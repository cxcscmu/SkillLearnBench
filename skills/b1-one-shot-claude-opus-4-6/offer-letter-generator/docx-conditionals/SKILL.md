---
name: docx-conditionals
description: Handle conditional sections in Word templates with IF/END_IF markers, removing or keeping content based on data values.
---

# Conditional Sections in Word Templates

## Pattern
Templates use `{{IF_TAG}}content{{END_IF_TAG}}` to mark conditional content.

## Logic
1. Check the data field (e.g., `RELOCATION_PACKAGE`) for "Yes"/"No"
2. If "Yes": strip the `{{IF_RELOCATION}}` and `{{END_IF_RELOCATION}}` markers, keep inner content
3. If "No": remove the entire block including markers and content
4. Handle the case where conditional markers and content may span a single paragraph or multiple paragraphs

## Implementation Note
Process conditionals BEFORE placeholder replacement, since the conditional content may itself contain placeholders that should only be replaced if the section is kept.
