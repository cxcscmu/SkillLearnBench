---
name: california-sc100-form-fields
description: Use this skill when you need to fill out the California Small Claims Court form SC-100. It maps the form's PDF field names to their meanings and expected values.
---

# California SC-100 Small Claims Court Form - Field Mapping

## Overview
The SC-100 is the official "Plaintiff's Claim and ORDER to Go to Small Claims Court" form used in California. It is a fillable PDF with specific named form fields.

## Common PDF Field Names and Their Meanings

The SC-100 form typically has these sections and fields (field names may vary slightly by PDF version but generally follow this pattern):

### Header / Court Info
- **Court name fields**: Usually at top — the Superior Court name, branch, address. Often left for the court to fill or filled based on filing location.
- Fields like `SCCourt`, `court_name`, or `Text1`-style names for court identification.

### Plaintiff Information (Item 1)
- **Plaintiff name**: The person filing the claim (e.g., `Plaintiff1Name`, `Name of Plaintiff 1`)
- **Plaintiff address / Street**: Street address of plaintiff
- **Plaintiff City, State, ZIP**: City/State/Zip
- **Plaintiff phone**: Telephone number
- **Plaintiff email**: Email address (if field exists)
- Multiple plaintiff support (Plaintiff 2, etc.)

### Defendant Information (Item 2)
- **Defendant name**: The person being sued
- **Defendant address / Street**: Street address
- **Defendant City, State, ZIP**
- **Defendant phone**: Phone number

### Claim Details (Items 3–8)
- **Item 3 - Why filing in this court**: Checkboxes for venue reason (where defendant lives, where damage occurred, where contract was signed, etc.)
  - Common checkbox: "Defendant lives in this court's jurisdiction" or similar
- **Item 4 - Amount of claim**: Dollar amount claimed (e.g., `$1,500.00`)
- **Item 5 - Basis of claim / What happened**: Text field explaining the dispute
  - Often includes date fields for when the events occurred
- **Item 6 - Have you asked the defendant to pay**: Yes/No checkbox, with explanation
- **Item 7 - Number of small claims filed in past 12 months**: Count field
- **Item 8 - Understanding of rules**: Checkbox acknowledging court procedures

### Filing / Signature Section
- **Date filed**: Date of filing
- **Plaintiff signature**: Signature field
- **Filed on behalf of**: Whether plaintiff is individual, business, etc.

## Checkbox Fields
Checkboxes in PDF forms are typically toggled with values like:
- `Yes`, `On`, `1`, `True` for checked
- `Off`, `No`, `0`, `False` for unchecked

The actual value depends on how the PDF was authored. Use a PDF inspection tool to determine exact values.

## Date Format
Per the task instructions, dates should be formatted as `xxxx-xx-xx` (e.g., `2026-01-19`).

## Important Notes
- **Court-filled fields** (like case number, hearing date/time) should be left empty.
- **Optional fields** not mentioned in the case description should be left empty.
- Inspect the actual PDF field names using a tool like `pdftk dump_data_fields` or Python's `PyPDF2`/`pikepdf`/`pdfrw` to get exact field names before filling.