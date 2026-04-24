---
name: california-small-claims
description: How to fill out the California Small Claims Court SC-100 form, including field mapping and required vs. optional fields.
---

# California Small Claims Court SC-100 Form

## Overview
The SC-100 form ("Plaintiff's Claim and Order to Go to Small Claims Court") is a 6-page fillable PDF. Pages 1, 5, and 6 are informational; data entry is on pages 2–4.

## Field Sections by Page

### Page 2 – Plaintiff & Defendant Info + Claim Amount

#### Plaintiff (Section 1)
| Field ID suffix | Description |
|---|---|
| `PxCaption[0].Plaintiff[0]` | Plaintiff name(s) header |
| `PlaintiffName1[0]` | Plaintiff full name |
| `PlaintiffPhone1[0]` | Plaintiff phone |
| `PlaintiffAddress1[0]` | Plaintiff street address |
| `PlaintiffCity1[0]` | Plaintiff city |
| `PlaintiffState1[0]` | Plaintiff state |
| `PlaintiffZip1[0]` | Plaintiff ZIP |
| `PlaintiffMailingAddress1[0]` | Mailing address (if different) |
| `EmailAdd1[0]` | Plaintiff email |
| `Checkbox1[0]` | More than two plaintiffs (check /1 if yes) |
| `Checkbox2[0]` | Fictitious name (check /1 if yes) |
| `Checkbox3[0]` | Licensee/payday lender (check /1 if yes) |

#### Defendant (Section 2)
| Field ID suffix | Description |
|---|---|
| `DefendantName1[0]` | Defendant full name |
| `DefendantPhone1[0]` | Defendant phone |
| `DefendantAddress1[0]` | Defendant street address |
| `DefendantCity1[0]` | Defendant city |
| `DefendantState1[0]` | Defendant state |
| `DefendantZip1[0]` | Defendant ZIP |
| `DefendantMailingAddress1[0]` | Defendant mailing (if different) |
| `Checkbox4[0]` | More than one defendant |
| `Checkbox5[0]` | Defendant on active military duty |

#### Claim (Section 3)
| Field ID suffix | Description |
|---|---|
| `PlaintiffClaimAmount1[0]` | Dollar amount claimed |
| `Lia[0].FillField2[0]` | 3a: Why does defendant owe money |

### Page 3 – When/How + Venue + Misc

| Field ID suffix | Description |
|---|---|
| `Lib[0].Date2[0]` | 3b: Date started (if time period) |
| `Lib[0].Date3[0]` | 3b: Through date (if time period) |
| `Lib[0].Date1[0]` | 3b: Single date (if specific date) |
| `Lic[0].FillField1[0]` | 3c: How amount was calculated |
| `Checkbox1[0]` | Need more space (attach MC-031) |
| `Item4[0].Checkbox50[0]` | Sec 4: Yes – asked defendant to pay |
| `Item4[0].Checkbox50[1]` | Sec 4: No – did not ask |
| `Item4[0].FillField2[0]` | Sec 4: Explanation if No |
| `Lia[0].Checkbox5cb[0]` | Sec 5a: Defendant lives/does business here |
| `Lib[0].Checkbox5cb[0]` | Sec 5b: Buyer/lessee signed contract here |
| `Lic[0].Checkbox5cb[0]` | Sec 5c: Retail installment contract |
| `Lid[0].Checkbox5cb[0]` | Sec 5d: Vehicle finance sale |
| `Lie[0].Checkbox5cb[0]` | Sec 5e: Other |
| `Lie[0].FillField55[0]` | Sec 5e: Other (specify) |
| `item6[0].ZipCode1[0]` | Sec 6: ZIP of venue |
| `item7[0].Checkbox60[0]` | Sec 7: Yes – attorney-client fee dispute |
| `item7[0].Checkbox60[1]` | Sec 7: No |
| `item8[0].Checkbox61[0]` | Sec 8: Yes – suing public entity |
| `item8[0].Checkbox61[1]` | Sec 8: No |
| `item8[0].Date4[0]` | Sec 8: Date claim filed with public entity |

### Page 4 – Questions 9-11 + Signature

| Field ID suffix | Description |
|---|---|
| `Item9[0].Checkbox62[0]` | Sec 9: Yes – filed 12+ claims in 12 months |
| `Item9[0].Checkbox62[1]` | Sec 9: No |
| `li10[0].Checkbox63[0]` | Sec 10: Yes – claim over $2,500 |
| `li10[0].Checkbox63[1]` | Sec 10: No |
| `Sign[0].Date1[0]` | Signing date |
| `Sign[0].PlaintiffName1[0]` | Plaintiff printed name |

## Court-Filled Fields (DO NOT FILL)
- `CourtInfo`, `CaseNumber`, `CaseName` – filled by court clerk
- `TrialDate*`, `TrialTime*`, `TrialDepartment*` – set by court
- `TrialDateClerkSign*` – court clerk signature

## Date Format
Use `xxxx-xx-xx` (e.g., `2026-01-19`)

## Checkbox Values
- Checked: `/1` (or `/2` for second option in a pair)
- Unchecked: `/Off`
