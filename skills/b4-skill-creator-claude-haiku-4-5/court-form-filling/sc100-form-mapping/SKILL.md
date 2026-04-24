---
name: sc100-form-mapping
description: Map case information to California Small Claims Court Form SC-100 fields. Use this skill whenever you need to fill the SC-100 form, understand its structure, extract field names, or map plaintiff/defendant information to the correct form sections.
---

# SC-100 Form Mapping (California Small Claims Court)

## Form Overview

The SC-100 is California's Small Claims Court statement form. It contains sections for:
- Plaintiff (party suing) information
- Defendant (party being sued) information
- Court location selection
- Case description and amount claimed
- Filing date

## Standard Field Structure

The form typically has these field groups:

### Plaintiff Information (Top Section)
```
Plaintiff_Name: Full name
Plaintiff_StreetAddress: Street address
Plaintiff_City: City
Plaintiff_State: State
Plaintiff_ZipCode: ZIP code
Plaintiff_Phone: Phone number
Plaintiff_Email: Email address
```

### Defendant Information (Second Section)
```
Defendant_Name: Full name
Defendant_StreetAddress: Street address
Defendant_City: City
Defendant_State: State
Defendant_ZipCode: ZIP code
Defendant_Phone: Phone number
```

### Court Information
```
County: County name (derived from defendant address)
Court_Location: Court location
FilingDate: Date filed (format: YYYY-MM-DD or as form requires)
```

### Case Details
```
CaseDescription: Summary of claim
Amount: Dollar amount of claim
```

## Data Mapping Strategy

When given a case description, extract:

1. **Plaintiff data**: Name, full address, phone, email
2. **Defendant data**: Name, full address, phone
3. **Dates**: Incident date, filing date
4. **Claim amount**: Dollar amount
5. **Description**: Summary of the dispute

## Common Address Parsing

Extract address components:
```
Street: "655 S Fair Oaks Ave" → "655 S Fair Oaks Ave"
City: From address or explicit mention
State: "CA"
ZIP: 5-digit code
```

## County Determination

California has 58 counties. For address lookup:
- **Sunnyvale**: Santa Clara County
- Use defendant's address to determine jurisdiction county

## Special Considerations

- **First-time filer**: Check if there's a first-time filer checkbox
- **Lease/Contract dates**: Include relevant dates (start, end, incident date)
- **Amount format**: Typically numeric without dollar sign (e.g., "1500")
- **Optional fields**: Leave court-filled fields empty (judge name, case number, etc.)
- **Phone format**: Can be numeric or formatted (both usually accepted)

## Date Formatting

Always use `YYYY-MM-DD` unless the form specifies otherwise. Verify the form's expected format before filling.

## Example Field Mapping

For a security deposit case:
```
Plaintiff_Name: "Joyce He"
Plaintiff_StreetAddress: "655 S Fair Oaks Ave"
Plaintiff_City: "Sunnyvale"
Plaintiff_State: "CA"
Plaintiff_ZipCode: "94086"
Plaintiff_Phone: "4125886066"
Plaintiff_Email: "he1998@gmail.com"

Defendant_Name: "Zhi Chen"
Defendant_StreetAddress: "299 W Washington Ave"
Defendant_City: "Sunnyvale"
Defendant_State: "CA"
Defendant_ZipCode: "94086"
Defendant_Phone: "5125658878"

County: "Santa Clara"
FilingDate: "2026-01-19"
Amount: "1500"
CaseDescription: "Defendant failed to return security deposit of $1500 based on signed roommate sublease contract."
```

## Process

1. Extract all information from case description
2. Identify the PDF field names using `get_fields()`
3. Map extracted data to field names
4. Fill only non-empty required fields
5. Leave court-filled and optional fields empty
6. Save with appropriate filename

## See Also

- Use `pdf-form-filler` skill for the actual PDF manipulation
- California court forms: courts.ca.gov
