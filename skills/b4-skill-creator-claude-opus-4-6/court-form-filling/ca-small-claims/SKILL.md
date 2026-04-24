---
name: ca-small-claims
description: California Small Claims Court SC-100 form field mapping and filling guide. Use this skill when filling out California SC-100 Plaintiff's Claim forms, understanding small claims court procedures, or mapping case details to SC-100 form fields.
---

# California SC-100 Small Claims Form Guide

## Form Structure (6 pages)

### Page 1 - Header & Court Order (court-filled)
- `CourtInfo[0]` - Court name and address (e.g., "Superior Court of California, County of Santa Clara")
- `CaseNumber[0]`, `CaseName[0]` - Court-assigned
- Trial date fields - Court-filled

### Page 2 - Parties & Claim Amount
**Section 1 - Plaintiff:**
- `PlaintiffName1[0]`, `PlaintiffPhone1[0]`
- `PlaintiffAddress1[0]` (street), `PlaintiffCity1[0]`, `PlaintiffState1[0]`, `PlaintiffZip1[0]`
- `EmailAdd1[0]`
- `Plaintiff[0]` - Header caption (plaintiff name)

**Section 2 - Defendant:**
- `DefendantName1[0]`, `DefendantPhone1[0]`
- `DefendantAddress1[0]` (street), `DefendantCity1[0]`, `DefendantState1[0]`, `DefendantZip1[0]`

**Section 3 - Claim:**
- `PlaintiffClaimAmount1[0]` - Dollar amount
- `FillField2[0]` (page 2) - Why defendant owes money (3a)

### Page 3 - Claim Details & Filing Reason
- `Plaintiff[0]`, `CaseNumber[0]` - Headers
- `Date1[0]` - Specific date (3b)
- `Date2[0]` - Date started, `Date3[0]` - Through date
- `FillField1[0]` - How money was calculated (3c)
- `Checkbox50[0]`=Yes / `Checkbox50[1]`=No - Asked defendant to pay (item 4)
- `FillField2[0]` (page 3) - Explanation if no

**Section 5 - Why this courthouse:**
- `Checkbox5cb[0]` states: `/1`=a, `/2`=b, `/3`=c, `/4`=d, `/5`=e
  - a.(1) Where defendant lives/does business

**Section 6-8:**
- `ZipCode1[0]` - Zip of place in item 5
- `Checkbox60[0]`=Yes/`[1]`=No - Attorney fee dispute (item 7)
- `Checkbox61[0]`=Yes/`[1]`=No - Suing public entity (item 8)

### Page 4 - Final Questions & Signature
- `Checkbox62[0]`=Yes/`[1]`=No - Filed 12+ claims (item 9)
- `Checkbox63[0]`=Yes/`[1]`=No - Claim > $2,500 (item 10)
- `Date1[0]` - Signature date
- `PlaintiffName1[0]` - Printed name

## Filing Location Rules
- File where defendant lives: choose 5a.(1)
- Sunnyvale, CA is in Santa Clara County
