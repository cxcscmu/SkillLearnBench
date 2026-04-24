---
name: docx-template-manipulation
description: Strategies for programmatically modifying .docx files, handling placeholders, and performing conditional text removal.
---

### Handling Template Placeholders
Since the source is a `.docx` file, standard text replacement is not possible because Word files are zipped XML structures.

1. **Library Selection:** Use the `python-docx` or `docxtpl` library to interact with the file structure. `docxtpl` is recommended as it natively supports Jinja2-style syntax (`{{VAR}}`).
2. **Standard Replacement:** Iterate through the document's paragraphs and tables to swap placeholders like `{{CANDIDATE_FULL_NAME}}` with the corresponding value from the JSON data.

### Conditional Content Logic
To handle the `{{IF_RELOCATION}}` blocks:
1. **Evaluation:** Check the `RELOCATION_PACKAGE` boolean or string from the JSON data.
2. **Processing:**
   - **If "Yes":** Remove the `{{IF_RELOCATION}}` and `{{END_IF_RELOCATION}}` markers while keeping the text contained between them.
   - **If "No" (or empty):** Remove the entire block, including the markers and the text contained within them.
3. **Save:** Once modifications are complete, save the object as `/root/offer_letter_filled.docx`.