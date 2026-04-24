Recruiting has already approved the compensation details and candidate information for a new hire. Your job is to turn that handoff into the final outbound offer letter.

Use the Word template at `offer_letter_template.docx`. It contains placeholders such as `{{CANDIDATE_FULL_NAME}}`, `{{POSITION}}`, and related fields. The finalized values to use are in `employee_data.json`.

Generate the completed offer letter by replacing all placeholders in the template and save the finished document to `/root/offer_letter_filled.docx`.

The template also contains a conditional block in the form `{{IF_RELOCATION}}...{{END_IF_RELOCATION}}`. If `RELOCATION_PACKAGE` is `Yes`, keep the relocation content but remove the marker tags. If `RELOCATION_PACKAGE` is `No`, remove that relocation block entirely from the final document.
