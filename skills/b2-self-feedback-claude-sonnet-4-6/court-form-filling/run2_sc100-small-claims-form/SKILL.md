---
name: run2_sc100-small-claims-form
description: How to fill California SC-100 Small Claims Court PDF form using fillable field IDs; includes complete field mapping, checkbox behavior, and field fill strategy.
---

# Filling CA SC-100 Small Claims Court Form (Improved)

## Overview
The SC-100 is a 6-page California court form with fillable fields. Pages 2-4 contain plaintiff-fillable sections. Pages 1 (top header/court info) and 6 (bottom buttons) are court-managed.

## Workflow

1. Run `python3 scripts/check_fillable_fields.py <file.pdf>` → confirms fillable fields
2. Run `python3 scripts/extract_form_field_info.py <file.pdf> <field_info.json>` → extract field metadata
3. Run `python3 scripts/convert_pdf_to_images.py <file.pdf> <output_dir/>` → visualize for field identification
4. Create `field_values.json` using field mappings below
5. Run `python3 scripts/fill_fillable_fields.py <blank.pdf> <field_values.json> <filled.pdf>`

## Complete Field Mapping

### Page 1 — Court-filled only (do NOT fill)
- CourtInfo, CaseNumber, CaseName, TrialDate, TrialTime, TrialDepartment, ClerkSign fields are all filled by the court.

### Page 2 — Plaintiff & Defendant Info + Claim

**Header:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page2[0].PxCaption[0].Plaintiff[0]` | Plaintiff name(s) in header |

**Section 1 – Plaintiff:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName1[0]` | Plaintiff full name |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffPhone1[0]` | Plaintiff phone |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffAddress1[0]` | Plaintiff street |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffCity1[0]` | Plaintiff city |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffState1[0]` | Plaintiff state |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffZip1[0]` | Plaintiff zip |
| `SC-100[0].Page2[0].List1[0].Item1[0].EmailAdd1[0]` | Plaintiff email |
| `SC-100[0].Page2[0].List1[0].Item1[0].Checkbox1[0]` | More than 2 plaintiffs (checked_value="/1") |
| `SC-100[0].Page2[0].List1[0].Item1[0].Checkbox2[0]` | Plaintiff using fictitious name (checked_value="/1") |
| `SC-100[0].Page2[0].List1[0].Item1[0].Checkbox3[0]` | Plaintiff is licensee/payday lender (checked_value="/1") |

**Second plaintiff (if applicable):**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName2[0]` | Second plaintiff name |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffPhone2[0]` | Second plaintiff phone |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffAddress2[0]` | Second plaintiff street |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffCity2[0]` | Second plaintiff city |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffState2[0]` | Second plaintiff state |
| `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffZip2[0]` | Second plaintiff zip |
| `SC-100[0].Page2[0].List1[0].Item1[0].EmailAdd2[0]` | Second plaintiff email |

**Section 2 – Defendant:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantName1[0]` | Defendant full name |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantPhone1[0]` | Defendant phone |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantAddress1[0]` | Defendant street |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantCity1[0]` | Defendant city |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantState1[0]` | Defendant state |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantZip1[0]` | Defendant zip |
| `SC-100[0].Page2[0].List2[0].item2[0].Checkbox4[0]` | More than one defendant (checked_value="/1") |
| `SC-100[0].Page2[0].List2[0].item2[0].Checkbox5[0]` | Defendant on active military duty (checked_value="/1") |

**If defendant is a corporation/LLC (optional):**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantName2[0]` | Agent for service name |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantJob1[0]` | Job title of agent |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantAddress2[0]` | Agent street |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantCity2[0]` | Agent city |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantState2[0]` | Agent state |
| `SC-100[0].Page2[0].List2[0].item2[0].DefendantZip2[0]` | Agent zip |

**Section 3 – Claim:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page2[0].List3[0].PlaintiffClaimAmount1[0]` | Dollar amount (numeric only, e.g. "1500") |
| `SC-100[0].Page2[0].List3[0].Lia[0].FillField2[0]` | Why defendant owes (section 3a explanation) |

### Page 3 — When/How + Jurisdiction + Declarations

**Header:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page3[0].PxCaption[0].Plaintiff[0]` | Plaintiff name(s) in header |

**Section 3 (continued):**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page3[0].List3[0].Lib[0].Date1[0]` | 3b: When did this happen (single specific date) |
| `SC-100[0].Page3[0].List3[0].Lib[0].Date2[0]` | 3b: Time period start date ("Date started") |
| `SC-100[0].Page3[0].List3[0].Lib[0].Date3[0]` | 3b: Time period end date ("Through") |
| `SC-100[0].Page3[0].List3[0].Lic[0].FillField1[0]` | 3c: How amount was calculated |
| `SC-100[0].Page3[0].List3[0].Checkbox1[0]` | "Check here if you need more space" (checked_value="/1") |

**Section 4 – Asked Defendant to Pay:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page3[0].List4[0].Item4[0].Checkbox50[0]` | Q4 Yes (checked_value="/1") |
| `SC-100[0].Page3[0].List4[0].Item4[0].Checkbox50[1]` | Q4 No (checked_value="/2") |
| `SC-100[0].Page3[0].List4[0].Item4[0].FillField2[0]` | Q4 explanation if No |

**Section 5 – Why Filing at This Courthouse:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page3[0].List5[0].Lia[0].Checkbox5cb[0]` | 5a: defendant lives/works here OR contract made/broken here (checked_value="/1") |
| `SC-100[0].Page3[0].List5[0].Lib[0].Checkbox5cb[0]` | 5b: buyer/lessee contract (checked_value="/2") |
| `SC-100[0].Page3[0].List5[0].Lic[0].Checkbox5cb[0]` | 5c: retail installment contract (checked_value="/3") |
| `SC-100[0].Page3[0].List5[0].Lid[0].Checkbox5cb[0]` | 5d: vehicle finance sale (checked_value="/4") |
| `SC-100[0].Page3[0].List5[0].Lie[0].Checkbox5cb[0]` | 5e: Other (checked_value="/5") |
| `SC-100[0].Page3[0].List5[0].Lie[0].FillField55[0]` | 5e: Other explanation text |

**Sections 6-8:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page3[0].List6[0].item6[0].ZipCode1[0]` | Q6: Zip code of courthouse area |
| `SC-100[0].Page3[0].List7[0].item7[0].Checkbox60[0]` | Q7 Yes: attorney-client fee (checked_value="/1") |
| `SC-100[0].Page3[0].List7[0].item7[0].Checkbox60[1]` | Q7 No (checked_value="/2") |
| `SC-100[0].Page3[0].List7[0].item7[0].Checkbox11[0]` | Q7 arbitration done (checked_value="/1") |
| `SC-100[0].Page3[0].List8[0].item8[0].Checkbox61[0]` | Q8 Yes: suing public entity (checked_value="/1") |
| `SC-100[0].Page3[0].List8[0].item8[0].Checkbox61[1]` | Q8 No (checked_value="/2") |
| `SC-100[0].Page3[0].List8[0].item8[0].Checkbox14[0]` | Q8 claim already filed with entity (checked_value="/1") |
| `SC-100[0].Page3[0].List8[0].item8[0].Date4[0]` | Q8 date claim filed with public entity |

### Page 4 — Declarations & Signature

**Header:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page4[0].PxCaption[0].Plaintiff[0]` | Plaintiff name(s) in header |

**Sections 9-10:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page4[0].List9[0].Item9[0].Checkbox62[0]` | Q9 Yes: filed >12 claims last 12 months (checked_value="/1") |
| `SC-100[0].Page4[0].List9[0].Item9[0].Checkbox62[1]` | Q9 No (checked_value="/2") |
| `SC-100[0].Page4[0].List10[0].li10[0].Checkbox63[0]` | Q10 Yes: claim > $2,500 (checked_value="/1") |
| `SC-100[0].Page4[0].List10[0].li10[0].Checkbox63[1]` | Q10 No (checked_value="/2") |

**Signature section:**
| Field ID | Description |
|----------|-------------|
| `SC-100[0].Page4[0].Sign[0].Date1[0]` | Filing date for first plaintiff |
| `SC-100[0].Page4[0].Sign[0].PlaintiffName1[0]` | First plaintiff printed name |
| `SC-100[0].Page4[0].Sign[0].Date2[0]` | Filing date for second plaintiff |
| `SC-100[0].Page4[0].Sign[0].PlaintiffName2[0]` | Second plaintiff printed name |

## Important Notes

### Dates
- Format: `yyyy-mm-dd` (e.g., "2025-09-30", "2026-01-19")
- For a specific date: fill Date1, leave Date2/Date3 empty
- For a time period: leave Date1 empty, fill Date2 (started) and Date3 (through)

### Checkboxes
- Always use the `checked_value` from field_info.json (e.g., "/1", "/2")
- For section 4: Checkbox50[0] = Yes ("/1"), Checkbox50[1] = No ("/2")
- For sections 7/8/9/10: [0] = Yes, [1] = No
- Section 5 checkboxes use a shared field name `Checkbox5cb[0]` but different checked_values ("/1" through "/5")

### Do NOT fill (leave empty)
- Page 1: all court-stamp and order fields
- Mailing addresses (unless different from street address)
- Corporation/LLC agent fields (unless defendant is not an individual)
- Second plaintiff fields (unless there are multiple plaintiffs)
- Case Number fields (filled by court)

### Standard answers for individual vs. business
- Q7 (attorney-client dispute): No → `Checkbox60[1]` = "/2"
- Q8 (public entity): No → `Checkbox61[1]` = "/2"
- Q9 (>12 claims filed): if first time → No → `Checkbox62[1]` = "/2"
- Q10 (>$2,500): check amount against threshold → typically No for standard deposit cases

### Page headers (PxCaption)
Must fill `Plaintiff[0]` header on pages 2, 3, AND 4 — same value as PlaintiffName1.
