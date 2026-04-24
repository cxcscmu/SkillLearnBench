---
name: Fill California Small Claims Form SC-100
description: Use this skill to fill the California Small Claims Court form (SC-100) with plaintiff and defendant information, case details, and amounts. Requires actual field names from the PDF — run Extract PDF Form Field Names skill first.
---

# Fill California Small Claims Form SC-100

## Purpose
Populate the SC-100 form with case information including plaintiff/defendant details, addresses, phone/email, claim amount, and case description.

## Prerequisites
- Run "Extract PDF Form Field Names" skill first to get actual field names
- Have case details: names, addresses, phone, email, amount, dates, description

## Implementation

```python
import pdfrw
from datetime import datetime

def fill_sc100_form(pdf_blank_path, pdf_output_path, case_data):
    """
    Fill SC-100 form with case information.
    
    Args:
        pdf_blank_path: Path to blank SC-100 PDF
        pdf_output_path: Path to save filled PDF
        case_data: Dictionary with all case information
    """
    # Load the blank form
    template = pdfrw.PdfReader(pdf_blank_path)
    
    # Create mapping based on actual field names discovered
    # IMPORTANT: These names must match the output from Extract PDF Form Field Names skill
    field_mapping = {
        # Plaintiff information
        'plaintiff_name': case_data.get('plaintiff_name', ''),
        'plaintiff_street': case_data.get('plaintiff_street', ''),
        'plaintiff_city': case_data.get('plaintiff_city', ''),
        'plaintiff_state': case_data.get('plaintiff_state', ''),
        'plaintiff_zip': case_data.get('plaintiff_zip', ''),
        'plaintiff_phone': case_data.get('plaintiff_phone', ''),
        'plaintiff_email': case_data.get('plaintiff_email', ''),
        
        # Defendant information
        'defendant_name': case_data.get('defendant_name', ''),
        'defendant_street': case_data.get('defendant_street', ''),
        'defendant_city': case_data.get('defendant_city', ''),
        'defendant_state': case_data.get('defendant_state', ''),
        'defendant_zip': case_data.get('defendant_zip', ''),
        'defendant_phone': case_data.get('defendant_phone', ''),
        
        # Case information
        'amount_demanded': case_data.get('amount_demanded', ''),
        'claim_description': case_data.get('claim_description', ''),
        'date_incident_from': case_data.get('date_incident_from', ''),
        'date_incident_to': case_data.get('date_incident_to', ''),
        'date_filed': case_data.get('date_filed', ''),
    }
    
    # Update fields in PDF
    for field_name, field_value in field_mapping.items():
        update_field(template, field_name, field_value)
    
    # Write filled PDF
    pdfrw.PdfWriter().write(pdf_output_path, template)
    print(f"Form saved to {pdf_output_path}")


def update_field(pdf_template, field_name, value):
    """
    Update a single form field in the PDF.
    
    Args:
        pdf_template: The PDF template object
        field_name: Exact field name from form
        value: Value to set (string)
    """
    if not value:
        return
    
    # Search through all pages and annotations
    for page in pdf_template.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                if annotation["/Subtype"] == "/Widget":
                    field = annotation.get("/T")
                    if field:
                        # Clean the field name
                        clean_field_name = field[1:-1] if field.startswith('(') else field
                        
                        # Match against target field name
                        if clean_field_name == field_name:
                            # Set the value WITHOUT parentheses wrapping
                            annotation.update(
                                AP=None,
                                AS=pdfrw.objects.PdfName(value) if value in ['Yes', 'No', 'Off', 'On'] else None,
                                V=f'({value})'
                            )
                            return
    
    print(f"Warning: Field '{field_name}' not found in PDF")


# Prepare case data from the case description
case_data = {
    'plaintiff_name': 'Joyce He',
    'plaintiff_street': '655 S Fair Oaks Ave',
    'plaintiff_city': 'Sunnyvale',
    'plaintiff_state': 'CA',
    'plaintiff_zip': '94086',
    'plaintiff_phone': '4125886066',
    'plaintiff_email': 'he1998@gmail.com',
    
    'defendant_name': 'Zhi Chen',
    'defendant_street': '299 W Washington Ave',
    'defendant_city': 'Sunnyvale',
    'defendant_state': 'CA',
    'defendant_zip': '94086',
    'defendant_phone': '5125658878',
    
    'amount_demanded': '1500',
    'claim_description': 'Failed to return security deposit of $1500 based on signed roommate sublease contract after moving out. Multiple requests via text message have been ignored.',
    'date_incident_from': '2025-09-30',
    'date_incident_to': '2026-01-19',
    'date_filed': '2026-01-19',
}

# Fill the form
fill_sc100_form('/root/sc100-blank.pdf', '/root/sc100-filled.pdf', case_data)
```

## Key Points
- **Field names must be exact** — use output from Extract PDF Form Field Names skill
- **Address fields may be separate** — map street, city, state, zip individually
- **Date format**: Use `YYYY-MM-DD` format without parentheses in the actual field
- **Special field handling**: Yes/No and checkbox fields use AS property; text fields use V property
- **Leave AP=None** to let the PDF renderer handle appearance
- **Don't add parentheses** when setting value string — pdfrw handles this internally

## Notes
- Only fill fields that have data — leave others empty as instructed
- Phone numbers stored as strings to preserve leading zeros
- Case description should summarize the claim concisely
- Date format must be exactly `YYYY-MM-DD`