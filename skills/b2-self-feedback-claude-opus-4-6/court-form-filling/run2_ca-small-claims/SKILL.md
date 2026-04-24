---
name: run2_ca-small-claims
description: Comprehensive field mapping for California SC-100 Small Claims Court form with field IDs and filling guidance.
---

# California SC-100 Small Claims Court Form — Field Reference

## Form Overview
The SC-100 has 6 pages, but only pages 1-4 contain fillable fields relevant to the plaintiff. Pages 5-6 are informational.

## Field ID to Form Mapping

### Page 1 — Court Header (mostly court-filled)
| Field ID | Purpose | Notes |
|---|---|---|
| `CourtInfo[0]` | County name after "Superior Court of California, County of" | Plaintiff fills this |
| `CaseNumber[0]` | Case number | Court-filled |
| `CaseName[0]` | Case name | Court-filled |
| `TrialDate1-3`, `TrialTime1-3`, etc. | Trial scheduling | Court-filled |

### Page 2 — Plaintiff, Defendant, Claim Amount
| Field ID Pattern | Purpose |
|---|---|
| `PlaintiffName1[0]` | First plaintiff full name |
| `PlaintiffPhone1[0]` | First plaintiff phone |
| `PlaintiffAddress1[0]` | First plaintiff street |
| `PlaintiffCity1[0]` | First plaintiff city |
| `PlaintiffState1[0]` | First plaintiff state |
| `PlaintiffZip1[0]` | First plaintiff zip |
| `PlaintiffMailingAddress1[0]` | Mailing address (if different) |
| `EmailAdd1[0]` | First plaintiff email |
| `PlaintiffName2[0]` through `EmailAdd2[0]` | Second plaintiff (if any) |
| `Checkbox1[0]` | More than 2 plaintiffs |
| `Checkbox2[0]` | Fictitious business name |
| `Checkbox3[0]` | Payday lender |
| `DefendantName1[0]` | Defendant full name |
| `DefendantPhone1[0]` | Defendant phone |
| `DefendantAddress1[0]` | Defendant street |
| `DefendantCity1[0]` | Defendant city |
| `DefendantState1[0]` | Defendant state |
| `DefendantZip1[0]` | Defendant zip |
| `DefendantMailingAddress1[0]` through `DefendantMailingZip1[0]` | Defendant mailing (if different) |
| `DefendantName2[0]`, `DefendantJob1[0]` | Agent for service (corporations) |
| `Checkbox4[0]` | More than 1 defendant |
| `Checkbox5[0]` | Defendant on active military duty |
| `PlaintiffClaimAmount1[0]` | Dollar amount claimed |
| `FillField2[0]` (under List3.Lia) | Section 3a: Why defendant owes money |
| `PxCaption.Plaintiff[0]` | Page header: plaintiff name (fill on pages 2, 3, 4) |

### Page 3 — Dates, Calculation, Demand, Filing Reason
| Field ID Pattern | Purpose |
|---|---|
| `Date1[0]` (Lib) | Section 3b: Specific date (if one date) |
| `Date2[0]` (Lib) | Section 3b: Date started (if range) |
| `Date3[0]` (Lib) | Section 3b: Through date (if range) |
| `FillField1[0]` (Lic) | Section 3c: How money was calculated |
| `Checkbox1[0]` (List3) | Need more space for section 3 |
| `Checkbox50[0]` | Section 4: Yes, asked defendant to pay |
| `Checkbox50[1]` | Section 4: No |
| `FillField2[0]` (Item4) | Section 4: Explain if no |
| `Checkbox5cb[0]` (Lia) | Section 5a: Defendant lives/does business here |
| `Checkbox5cb[0]` (Lib) | Section 5b: Buyer/lessee contract |
| `Checkbox5cb[0]` (Lic) | Section 5c: Retail installment |
| `Checkbox5cb[0]` (Lid) | Section 5d: Vehicle finance |
| `Checkbox5cb[0]` (Lie) | Section 5e: Other |
| `FillField55[0]` | Section 5e: Other explanation |
| `ZipCode1[0]` | Section 6: Zip of place in section 5 |
| `Checkbox60[0]` | Section 7: Yes, attorney fee dispute |
| `Checkbox60[1]` | Section 7: No |
| `Checkbox11[0]` | Section 7: Had arbitration |
| `Checkbox61[0]` | Section 8: Yes, suing public entity |
| `Checkbox61[1]` | Section 8: No |
| `Checkbox14[0]` | Section 8: Filed written claim |
| `Date4[0]` | Section 8: Claim filed date |

### Page 4 — Final Questions & Signature
| Field ID Pattern | Purpose |
|---|---|
| `Checkbox62[0]` | Section 9: Yes, filed 12+ claims |
| `Checkbox62[1]` | Section 9: No |
| `Checkbox63[0]` | Section 10: Yes, claim > $2,500 |
| `Checkbox63[1]` | Section 10: No |
| `Sign.Date1[0]` | First plaintiff signature date |
| `Sign.PlaintiffName1[0]` | First plaintiff printed name |
| `Sign.Date2[0]` | Second plaintiff signature date |
| `Sign.PlaintiffName2[0]` | Second plaintiff printed name |

## Key Decisions
- **County**: Determined by courthouse location. Sunnyvale → Santa Clara County.
- **Date format**: Follow instructions (e.g., xxxx-xx-xx).
- **Claim amount**: Use format like "1,500.00" (the "$" is pre-printed on the form).
- **Section 5**: Pick ONE option. For "filing where defendant lives" → check 5a.
- **Court-filled fields**: Leave blank: Case Number, Case Name, Trial dates/times, Clerk signatures.
- **Optional fields**: Leave blank if not applicable (mailing address if same, second plaintiff, agent for service, etc.).
