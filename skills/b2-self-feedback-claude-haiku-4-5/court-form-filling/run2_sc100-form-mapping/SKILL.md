---
name: run2_sc100-form-mapping
description: SC-100 California Small Claims form field ID mappings and data entry guidelines
---

# SC-100 Form Field Mapping Reference

## Form Overview
- **Name**: SC-100 Plaintiff's Claim and ORDER to Go to Small Claims Court
- **Pages**: 6 pages (courts fill pages 1 and 5-6; plaintiff fills pages 2-4)
- **Max Claim**: $12,500 for individuals, $6,250 for businesses
- **Court**: California Superior Court

## Critical: Court-Filled vs. Plaintiff-Filled Fields

**DO NOT FILL THESE (Court fills automatically):**
- Case Number field
- Trial Date, Time, Department
- Clerk signature and date
- Pages 5-6 (defendant information, help information)

**PLAINTIFF MUST FILL:**
- Pages 2-4 with claim details, party information, and declarations

## Page 2: Plaintiff Information

### Section 1 - Plaintiff Details
| Data | Field ID | Notes |
|------|----------|-------|
| Name | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName1[0]` | Full name |
| Phone | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffPhone1[0]` | 10-digit phone |
| Street Address | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffAddress1[0]` | Street and number only |
| City | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffCity1[0]` | City name |
| State | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffState1[0]` | 2-letter state code (CA) |
| Zip | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffZip1[0]` | 5-digit zip code |
| Email | `SC-100[0].Page2[0].List1[0].Item1[0].EmailAdd1[0]` | Email address |
| Mailing Address (if different) | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffMailingAddress1[0]` | Leave empty if same |
| Mailing City | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffMailingCity1[0]` | Leave empty if same |
| Mailing State | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffMailingState1[0]` | Leave empty if same |
| Mailing Zip | `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffMailingZip1[0]` | Leave empty if same |

**Multiple Plaintiffs**: If more than one plaintiff, fill PlaintiffName2, PlaintiffPhone2, PlaintiffAddress2, etc.

**Checkboxes on Page 2**:
- `SC-100[0].Page2[0].List1[0].Item1[0].Checkbox1[0]`: More than 2 plaintiffs (check with "/1", omit if not applicable)
- `SC-100[0].Page2[0].List1[0].Item1[0].Checkbox2[0]`: Fictitious business name (check with "/1", omit if not)
- `SC-100[0].Page2[0].List1[0].Item1[0].Checkbox3[0]`: Licensee/payday lender (check with "/1", omit if not)

### Section 2 - Defendant Information
| Data | Field ID | Notes |
|------|----------|-------|
| Name | `SC-100[0].Page2[0].List2[0].item2[0].DefendantName1[0]` | Full name or business name |
| Phone | `SC-100[0].Page2[0].List2[0].item2[0].DefendantPhone1[0]` | 10-digit phone if available |
| Street Address | `SC-100[0].Page2[0].List2[0].item2[0].DefendantAddress1[0]` | Street and number |
| City | `SC-100[0].Page2[0].List2[0].item2[0].DefendantCity1[0]` | City name |
| State | `SC-100[0].Page2[0].List2[0].item2[0].DefendantState1[0]` | 2-letter state code |
| Zip | `SC-100[0].Page2[0].List2[0].item2[0].DefendantZip1[0]` | 5-digit zip code |
| Mailing Address (if different) | `SC-100[0].Page2[0].List2[0].item2[0].DefendantMailingAddress1[0]` | Leave empty if same |
| Mailing City | `SC-100[0].Page2[0].List2[0].item2[0].DefendantMailingCity1[0]` | Leave empty if same |
| Mailing State | `SC-100[0].Page2[0].List2[0].item2[0].DefendantMailingState1[0]` | Leave empty if same |
| Mailing Zip | `SC-100[0].Page2[0].List2[0].item2[0].DefendantMailingZip1[0]` | Leave empty if same |
| Service Agent Name (for corporations) | `SC-100[0].Page2[0].List2[0].item2[0].DefendantName2[0]` | Only if defendant is corporation |
| Service Agent Job Title | `SC-100[0].Page2[0].List2[0].item2[0].DefendantJob1[0]` | Only if defendant is corporation |

**Checkboxes on Page 2**:
- `SC-100[0].Page2[0].List2[0].item2[0].Checkbox4[0]`: Multiple defendants (check with "/1", omit if not)
- `SC-100[0].Page2[0].List2[0].item2[0].Checkbox5[0]`: Defendant on active military duty (check with "/1", omit if not)

### Section 3 - Claim Information
| Data | Field ID | Notes |
|------|----------|-------|
| Claim Amount $ | `SC-100[0].Page2[0].List3[0].PlaintiffClaimAmount1[0]` | Dollar amount only (e.g., "1500") |
| Why does defendant owe money | `SC-100[0].Page2[0].List3[0].Lia[0].FillField2[0]` | Narrative explanation of claim |

## Page 3: Claim Details and Jurisdiction

### Section 3b - When Did This Happen?
| Data | Field ID | Notes |
|------|----------|-------|
| Specific Date OR Start Date | `SC-100[0].Page3[0].List3[0].Lib[0].Date1[0]` | Format: YYYY-MM-DD |
| Through Date (if range) | `SC-100[0].Page3[0].List3[0].Lib[0].Date2[0]` | Format: YYYY-MM-DD |
| Through Date (alt field) | `SC-100[0].Page3[0].List3[0].Lib[0].Date3[0]` | Alternative through date field |

### Section 3c - How Calculated
| Data | Field ID | Notes |
|------|----------|-------|
| Money Calculation Explanation | `SC-100[0].Page3[0].List3[0].Lic[0].FillField1[0]` | Explain how amount was calculated |

### Section 4 - Demand Before Suit
**Question**: "Have you asked the defendant (in person, in writing, or by phone) to pay you before you sue?"

| Choice | Field ID | Value |
|--------|----------|-------|
| **YES** | `SC-100[0].Page3[0].List4[0].Item4[0].Checkbox50[0]` | Use "/1" to check |
| **NO** (with explanation) | `SC-100[0].Page3[0].List4[0].Item4[0].Checkbox50[1]` | Use "/2" to check |
| Explanation (if NO) | `SC-100[0].Page3[0].List4[0].Item4[0].FillField2[0]` | Only fill if answer is NO |

### Section 5 - Jurisdiction (Why Filing at This Courthouse)
Select ONE of the following:

| Jurisdiction Reason | Field ID | Value |
|---------------------|----------|-------|
| (1) Where defendant lives/does business | `SC-100[0].Page3[0].List5[0].Lia[0].Checkbox5cb[0]` | "/1" |
| (2) Where plaintiff's property was damaged | `SC-100[0].Page3[0].List5[0].Lib[0].Checkbox5cb[0]` | "/2" |
| (3) Where plaintiff was injured | `SC-100[0].Page3[0].List5[0].Lic[0].Checkbox5cb[0]` | "/3" |
| (4) Where contract was made/performed/broken | `SC-100[0].Page3[0].List5[0].Lid[0].Checkbox5cb[0]` | "/4" |
| (5) Other (specify) | `SC-100[0].Page3[0].List5[0].Lie[0].Checkbox5cb[0]` | "/5" |
| Other explanation (if selected) | `SC-100[0].Page3[0].List5[0].Lie[0].FillField55[0]` | Explanation |

### Section 6 - Zip Code
| Data | Field ID | Notes |
|------|----------|-------|
| Zip Code | `SC-100[0].Page3[0].List6[0].item6[0].ZipCode1[0]` | Zip of jurisdiction location |

### Section 7 - Attorney-Client Fee Dispute
**Question**: "Is your claim about an attorney-client fee dispute?"

| Choice | Field ID | Value |
|--------|----------|-------|
| **YES** | `SC-100[0].Page3[0].List7[0].item7[0].Checkbox60[0]` | "/1" |
| **NO** | `SC-100[0].Page3[0].List7[0].item7[0].Checkbox60[1]` | "/2" |
| Arbitration checkbox (if YES) | `SC-100[0].Page3[0].List7[0].item7[0].Checkbox11[0]` | "/1" if arbitration done |

### Section 8 - Public Entity
**Question**: "Are you suing a public entity?"

| Choice | Field ID | Value |
|--------|----------|-------|
| **YES** | `SC-100[0].Page3[0].List8[0].item8[0].Checkbox61[0]` | "/1" |
| **NO** | `SC-100[0].Page3[0].List8[0].item8[0].Checkbox61[1]` | "/2" |
| Claim Filed Date (if YES) | `SC-100[0].Page3[0].List8[0].item8[0].Date4[0]` | Format: YYYY-MM-DD |

## Page 4: Declarations and Signature

### Section 9 - Multiple Small Claims
**Question**: "Have you filed more than 12 other small claims within the last 12 months in California?"

| Choice | Field ID | Value |
|--------|----------|-------|
| **YES** | `SC-100[0].Page4[0].List9[0].Item9[0].Checkbox62[0]` | "/1" |
| **NO** | `SC-100[0].Page4[0].List9[0].Item9[0].Checkbox62[1]` | "/2" |

### Section 10 - Claim Over $2,500
**Question**: "Is your claim for more than $2,500?"

| Choice | Field ID | Value |
|--------|----------|-------|
| **YES** | `SC-100[0].Page4[0].List10[0].li10[0].Checkbox63[0]` | "/1" |
| **NO** | `SC-100[0].Page4[0].List10[0].li10[0].Checkbox63[1]` | "/2" |

### Signature Section
| Data | Field ID | Notes |
|------|----------|-------|
| Filing Date | `SC-100[0].Page4[0].Sign[0].Date1[0]` | Format: YYYY-MM-DD |
| Plaintiff Name | `SC-100[0].Page4[0].Sign[0].PlaintiffName1[0]` | Full name (printed) |
| Second Plaintiff Date (if applicable) | `SC-100[0].Page4[0].Sign[0].Date2[0]` | Format: YYYY-MM-DD |
| Second Plaintiff Name | `SC-100[0].Page4[0].Sign[0].PlaintiffName2[0]` | Full name (printed) |

**Note**: Actual signatures cannot be filled programmatically; leave signature lines blank for manual signing.

## Field Value Format Examples

```json
{
  "field_id": "SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName1[0]",
  "value": "Joyce He"
}
```

```json
{
  "field_id": "SC-100[0].Page2[0].List3[0].PlaintiffClaimAmount1[0]",
  "value": "1500"
}
```

```json
{
  "field_id": "SC-100[0].Page3[0].List3[0].Lib[0].Date1[0]",
  "value": "2025-09-30"
}
```

```json
{
  "field_id": "SC-100[0].Page3[0].List4[0].Item4[0].Checkbox50[0]",
  "value": "/1"
}
```

## Common Scenarios

### Single Plaintiff, Single Defendant
- Fill PlaintiffName1, PlaintiffPhone1, PlaintiffAddress1, etc. (all with index 1)
- Fill DefendantName1, DefendantPhone1, DefendantAddress1, etc. (all with index 1)
- Leave Checkbox1 unchecked (more than two plaintiffs)
- Leave Checkbox4 unchecked (more than one defendant)

### Multiple Plaintiffs
- Fill PlaintiffName1, PlaintiffPhone1, ... for first plaintiff
- Fill PlaintiffName2, PlaintiffPhone2, ... for second plaintiff
- Check Checkbox1 with "/1" to indicate more than two plaintiffs
- Attach SC-100A form for additional plaintiffs

### Mailing Address Different from Street Address
- Fill PlaintiffMailingAddress1, PlaintiffMailingCity1, etc.
- Same format as street address fields

## Validation Rules
- Phone numbers: 10 digits (e.g., 4125886066)
- Zip codes: 5 digits (e.g., 94086)
- Dates: YYYY-MM-DD format (e.g., 2026-01-19)
- Claim amount: Numeric value without currency symbol (e.g., 1500)
- State: 2-letter abbreviation (e.g., CA)
- Checkboxes: Use "/" prefix for values ("/1", "/2", etc.)
