---
name: sc100-form-filler
description: How to map and fill the California Small Claims Court form SC-100 (Plaintiff's Claim and ORDER to Go to Small Claims Court). Use this skill whenever the user mentions filling an SC-100 form or filing a small claims case in California.
---

# Filling the SC-100 Form

This skill maps standard case description elements to the PDF form fields of the California Small Claims Court SC-100 form.

## Field Mappings

### Page 2 - Plaintiff and Defendant Details

**Item 1: Plaintiff Information**
- `SC-100[0].Page2[0].PxCaption[0].Plaintiff[0]`: Plaintiff Name
- `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName1[0]`: Plaintiff Name
- `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffAddress1[0]`: Street Address
- `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffCity1[0]`: City
- `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffState1[0]`: State
- `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffZip1[0]`: Zip
- `SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffPhone1[0]`: Phone Number
- `SC-100[0].Page2[0].List1[0].Item1[0].EmailAdd1[0]`: Email Address (if available)

**Item 2: Defendant Information**
- `SC-100[0].Page2[0].List2[0].item2[0].DefendantName1[0]`: Defendant Name
- `SC-100[0].Page2[0].List2[0].item2[0].DefendantAddress1[0]`: Street Address
- `SC-100[0].Page2[0].List2[0].item2[0].DefendantCity1[0]`: City
- `SC-100[0].Page2[0].List2[0].item2[0].DefendantState1[0]`: State
- `SC-100[0].Page2[0].List2[0].item2[0].DefendantZip1[0]`: Zip
- `SC-100[0].Page2[0].List2[0].item2[0].DefendantPhone1[0]`: Phone Number

**Item 3: The Claim**
- `SC-100[0].Page2[0].List3[0].PlaintiffClaimAmount1[0]`: Amount owed ($)
- `SC-100[0].Page2[0].List3[0].Lia[0].FillField2[0]`: Why does the defendant owe the plaintiff money? (3a)

### Page 3 - Claim Details & Venue

**Header**
- `SC-100[0].Page3[0].PxCaption[0].Plaintiff[0]`: Plaintiff Name

**Item 3 (continued)**
- `SC-100[0].Page3[0].List3[0].Lib[0].Date2[0]`: Date Started (3b)
- `SC-100[0].Page3[0].List3[0].Lib[0].Date3[0]`: Through Date (3b)
- `SC-100[0].Page3[0].List3[0].Lic[0].FillField1[0]`: How did you calculate the money owed? (3c)

**Item 4: Asked for Payment**
- `SC-100[0].Page3[0].List4[0].Item4[0].Checkbox50[0]`: "Yes" (Check if plaintiff asked for payment) -> value `/1`
- `SC-100[0].Page3[0].List4[0].Item4[0].Checkbox50[1]`: "No" -> value `/2`

**Item 5: Venue**
- `SC-100[0].Page3[0].List5[0].Lia[0].Checkbox5cb[0]`: "a. Where the defendant lives or does business." -> value `/1`

**Item 6, 7, 8: Extra Info**
- `SC-100[0].Page3[0].List6[0].item6[0].ZipCode1[0]`: Zip code of the courthouse or where defendant lives.
- `SC-100[0].Page3[0].List7[0].item7[0].Checkbox60[1]`: "No" to attorney-client fee dispute -> value `/2`
- `SC-100[0].Page3[0].List8[0].item8[0].Checkbox61[1]`: "No" to suing a public entity -> value `/2`

### Page 4 - Declarations & Signature

**Header**
- `SC-100[0].Page4[0].PxCaption[0].Plaintiff[0]`: Plaintiff Name

**Item 9 & 10: Claim History**
- `SC-100[0].Page4[0].List9[0].Item9[0].Checkbox62[1]`: "No" to >12 claims -> value `/2`
- `SC-100[0].Page4[0].List10[0].li10[0].Checkbox63[1]`: "No" to claim >$2,500 -> value `/2`

**Signatures**
- `SC-100[0].Page4[0].Sign[0].Date1[0]`: Date of signature
- `SC-100[0].Page4[0].Sign[0].PlaintiffName1[0]`: Plaintiff's printed name

## Best Practices
- Dates should be formatted consistently, typically YYYY-MM-DD or as specified.
- Use `/1` for Yes and `/2` for No where standard Yes/No pairs exist in checkboxes.
- Leave optional and court-filled fields empty as required.
