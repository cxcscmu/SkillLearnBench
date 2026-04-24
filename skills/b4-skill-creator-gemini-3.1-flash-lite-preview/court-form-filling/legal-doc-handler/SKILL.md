---
name: legal-doc-handler
description: Specialized instructions for reading, modifying, and filling PDF legal forms (e.g., California judicial council forms). Use this for any task involving PDF forms.
---

# Legal Document Handling

## PDF Form Filling Strategy
- Use available PDF libraries (if installed) or CLI utilities (like pdftk or similar tools).
- **CRITICAL**: Always maintain the original document metadata unless explicitly told to modify it.
- **Verification**: Post-filling, inspect the form to confirm that key fields are populated with the correct data.

## Best Practices
- **Data Integrity**: Never truncate or abbreviate information requested in official form fields.
- **Confidentiality**: Be mindful that legal documents contain PII. Avoid logging or printing sensitive document content in the conversation unless necessary for debugging.
- **Workflow**: 
  1. Identify form fields.
  2. Map provided user data to fields.
  3. Perform the fill operation.
  4. Save as a new file (suffix "-filled").
