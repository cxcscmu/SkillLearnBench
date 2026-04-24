---
name: offer-letter-data-mapping
description: Logic for mapping employee JSON data to offer letter template placeholders. Includes handling of conditional fields like relocation packages. Use this skill when preparing data for offer letter generation.
---

# offer-letter-data-mapping

## Mapping Rules
When preparing data for the `offer_letter_template.docx`, ensure the following mappings are correctly handled:

| JSON Key | Placeholder | Logic/Format |
|----------|-------------|--------------|
| `CANDIDATE_FULL_NAME` | `{{CANDIDATE_FULL_NAME}}` | Direct mapping |
| `POSITION` | `{{POSITION}}` | Direct mapping |
| `RELOCATION_PACKAGE` | `{{IF_RELOCATION}}` | If value is "Yes", enable relocation block |

## Conditional Logic: Relocation
The relocation section in the template is wrapped in:
`{{IF_RELOCATION}}`
...
`{{END_IF_RELOCATION}}`

**Decision Matrix:**
- If `RELOCATION_PACKAGE == "Yes"`: 
  - Set internal flag `is_relocation_enabled = True`.
  - Replace placeholders inside the block (e.g., `{{RELOCATION_AMOUNT}}`).
  - Remove the `{{IF_RELOCATION}}` and `{{END_IF_RELOCATION}}` markers.
- If `RELOCATION_PACKAGE == "No"`:
  - Set internal flag `is_relocation_enabled = False`.
  - Remove the entire block from the document.

## Data Sanitization
- Ensure currency values (e.g., `BASE_SALARY`) are formatted with commas.
- Ensure dates are in a readable format (e.g., `January 15, 2024`).
- All keys in the data dictionary should match the uppercase placeholders in the Word document.
