---
name: sc100-case-data-extraction
description: Use this skill to extract and organize case data from a natural language case description for filling the SC-100 form. Maps case facts to form fields.
---

# Extracting Case Data for SC-100 Form

## Data Mapping from Case Description

Given a case description, extract and map these elements:

### Plaintiff Information
| Data Point | How to Extract | Form Field |
|---|---|---|
| Full Name | "I am [Name]" | Plaintiff name field |
| Address | "I live in [address]" | Plaintiff street, city, state, zip |
| Phone | "my phone # is [number]" | Plaintiff phone field |
| Email | "email: [email]" | Plaintiff email field |

### Defendant Information
| Data Point | How to Extract | Form Field |
|---|---|---|
| Full Name | "I want to sue [Name]" | Defendant name field |
| Address | "in [address]" after defendant name | Defendant street, city, state, zip |
| Phone | "His/Her phone #: [number]" | Defendant phone field |

### Claim Details
| Data Point | How to Extract | Form Field |
|---|---|---|
| Amount | "security deposit of amount $X" | Dollar amount claimed |
| Basis | "failed to return security deposit based on..." | What happened / claim description |
| Date range | "happened from [date] until [date]" | Date fields for incident |
| Venue reason | "filing where defendant lives" | Checkbox: defendant lives in jurisdiction |
| Demand made | "asked him to return money multiple times" | Yes, asked defendant to pay |
| Filing date | "file it with date: [date]" | Date of filing |
| Prior claims | "first time suing by small claims" | Number of prior claims = 0 or first-time indicator |
| Amount source | "listed on the signed roommate sublease contract" | How amount was calculated |

### Example Data for This Case

```python
case_data = {
    # Plaintiff
    "plaintiff_name": "Joyce He",
    "plaintiff_street": "655 S Fair Oaks Ave",
    "plaintiff_city": "Sunnyvale",
    "plaintiff_state": "CA",
    "plaintiff_zip": "94086",
    "plaintiff_phone": "4125886066",
    "plaintiff_email": "he1998@gmail.com",

    # Defendant
    "defendant_name": "Zhi Chen",
    "defendant_street": "299 W Washington Ave",
    "defendant_city": "Sunnyvale",
    "defendant_state": "CA",
    "defendant_zip": "94086",
    "defendant_phone": "5125658878",

    # Claim
    "claim_amount": "1500.00",  # or "1,500.00"
    "claim_description": "Defendant failed to return my security deposit of $1,500 after moving out, based on the signed roommate sublease contract.",
    "incident_start_date": "2025-09-30",
    "incident_end_date": "2026-01-19",
    "venue_reason": "Where defendant lives/has a business",
    "asked_to_pay": True,
    "how_asked": "Asked defendant to return the money multiple times via text but defendant is not responding.",
    "amount_basis": "The amount is listed on the signed roommate sublease contract.",
    "filing_date": "2026-01-19",
    "num_prior_claims": 0,  # first time suing
    "is_individual": True,
}
```

### Phone Number Formatting
Phone numbers may need formatting depending on the form:
- Raw: `4125886066`
- Formatted: `(412) 588-6066` or `412-588-6066`
- Check form field expectations; if single field, may use either format

### Address Parsing
Break addresses into components:
- `655 S Fair Oaks Ave, Sunnyvale, CA 94086`
  - Street: `655 S Fair Oaks Ave`
  - City: `Sunnyvale`
  - State: `CA`
  - ZIP: `94086`

### Venue Selection (Item 3)
The case says "filing where defendant lives" → Check the radio button or checkbox for "Where the defendant lives" or equivalent wording on the SC-100 form.

### Number of Claims (Item 7 equivalent)
"First time suing by small claims" → The count of prior SC claims in last 12 months = 0, and check any "first time" indicator.