---
name: ca-small-claims-sc100
description: California SC-100 Small Claims Court form field mapping and filling guide.
---

# California SC-100 Form Field Mapping

## Form Structure (6 pages)
- Page 1: Court info header, trial dates (clerk fills)
- Page 2: Plaintiff info (Section 1), Defendant info (Section 2), Claim amount & reason (Section 3a)
- Page 3: Dates (Section 3b/3c), Asked defendant to pay? (Section 4), Filing location reason (Section 5), Zip (Section 6), Attorney dispute (Section 7), Public entity (Section 8)
- Page 4: Filed 12+ claims? (Section 9), Claim > $2500? (Section 10), Declaration/signature (Section 11)
- Pages 5-6: Information pages (not fillable by plaintiff)

## Key Field Paths

### Page 2 - Plaintiff (Section 1)
- `PlaintiffName1[0]` - Name
- `PlaintiffPhone1[0]` - Phone
- `PlaintiffAddress1[0]` - Street
- `PlaintiffCity1[0]`, `PlaintiffState1[0]`, `PlaintiffZip1[0]`
- `EmailAdd1[0]` - Email
- `Plaintiff[0]` (PxCaption) - Name at top of pages 2-4

### Page 2 - Defendant (Section 2)
- `DefendantName1[0]`, `DefendantPhone1[0]`
- `DefendantAddress1[0]`, `DefendantCity1[0]`, `DefendantState1[0]`, `DefendantZip1[0]`

### Page 2 - Claim (Section 3)
- `PlaintiffClaimAmount1[0]` - Dollar amount
- `FillField2[0]` (List3.Lia) - Why defendant owes money

### Page 3 - Dates (Section 3b)
- `Date1[0]` - Specific date (or leave blank)
- `Date2[0]` - Date started
- `Date3[0]` - Through date

### Page 3 - Calculation (Section 3c)
- `FillField1[0]` (List3.Lic) - How calculated

### Page 3 - Asked to Pay (Section 4)
- `Checkbox50[0]` = Yes (`/1`), `Checkbox50[1]` = No (`/2`)
- `FillField2[0]` (List4) - If no, explain

### Page 3 - Filing Location (Section 5)
- `Checkbox5cb[0]` in Lia = option a (`/1`)
- Others: Lib (`/2`), Lic (`/3`), Lid (`/4`), Lie (`/5`)

### Page 3 - Other Fields
- `ZipCode1[0]` - Section 6 zip
- `Checkbox60[0]`/`[1]` - Section 7 Yes/No
- `Checkbox61[0]`/`[1]` - Section 8 Yes/No

### Page 4
- `Checkbox62[0]`/`[1]` - Section 9 Yes/No
- `Checkbox63[0]`/`[1]` - Section 10 Yes/No
- `Date1[0]` (Sign) - Signature date
- `PlaintiffName1[0]` (Sign) - Printed name
