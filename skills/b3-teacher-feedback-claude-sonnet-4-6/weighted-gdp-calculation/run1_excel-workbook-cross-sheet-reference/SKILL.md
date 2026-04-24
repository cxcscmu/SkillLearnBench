---
name: excel-workbook-cross-sheet-reference
description: Use when writing formulas in one Excel sheet that reference data in another sheet. Covers syntax, absolute vs relative references, and best practices for multi-sheet lookup formulas.
---

## Cross-Sheet References in Excel

### Basic Syntax

To reference a cell or range in another sheet:
```excel
=SheetName!CellReference
```

Examples:
```excel
=Data!A1
=Data!$A$1
=Data!$A$21:$E$40
```

If the sheet name contains spaces or special characters, wrap in single quotes:
```excel
='Source Data'!A1
```

### Using Cross-Sheet References in Lookup Formulas

When using INDEX&MATCH to pull from the "Data" sheet into the "Task" sheet:

```excel
=INDEX(Data!$E$21:$I$40,
       MATCH($D12, Data!$D$21:$D$40, 0),
       MATCH(H$10,  Data!$E$20:$I$20, 0))
```

- All references to the Data sheet get the `Data!` prefix
- References within the Task sheet (like `$D12` and `H$10`) have no prefix
- Mix of locked (`$`) and unlocked references allows the formula to be copied across H12:L17

### Absolute vs. Relative References When Copying

| Reference Type | Syntax | Behavior when copied |
|---|---|---|
| Fully absolute | `$D$12` | Never moves |
| Row absolute | `D$12` | Column moves, row stays |
| Column absolute | `$D12` | Column stays, row moves |
| Fully relative | `D12` | Both move |

**For a 2D fill (e.g., H12:L17):**
- Row lookup key (series code, varies by row): `$D12` — lock column D, let row move
- Column lookup key (year, varies by column): `H$10` — lock row 10, let column move
- Data arrays on the other sheet: fully absolute `Data!$D$21:$D$40`

### Practical Checklist

1. Enter formula in the top-left cell of the target range (e.g., H12)
2. Verify the formula returns the correct value
3. Copy the cell, select the full target range (H12:L17), and paste
4. Spot-check corner cells (H12, L12, H17, L17) to confirm references shifted correctly
5. If results are `#N/A`, check that the lookup keys (series codes, years) exactly match the source data format (text vs number, leading/trailing spaces)

### Common Errors

- `#N/A` — lookup key not found; check data types (e.g., year stored as text "2020" vs number 2020)
- `#REF!` — reference range is wrong size or sheet name is misspelled
- Wrong values — mixed-up absolute/relative references; audit with F2 to inspect