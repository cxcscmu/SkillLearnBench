---
name: xlsx-tool-operations
description: Common operations and patterns for using the xlsx skill tool to manipulate Excel files programmatically.
---

# XLSX Tool Operations

## Overview
The xlsx skill tool allows programmatic interaction with Excel files, enabling reading, writing, and analyzing spreadsheet data without manually opening files.

## Common Operations

### Reading Spreadsheet Data
Use the xlsx skill to:
- Examine sheet structure and contents
- Understand data layout and ranges
- Identify cell references and formulas
- Analyze existing data before writing formulas

**Pattern:**
```
Skill: xlsx
Operation: read or get_data
File: path/to/file.xlsx
Sheet: "SheetName"
Range: optional specific range like A1:Z100
```

### Writing Formulas to Cells
Use the xlsx skill to:
- Add formulas to specific cells
- Write values to cells
- Batch update multiple cells
- Preserve existing formatting

**Pattern:**
```
Skill: xlsx
Operation: write_cell or batch_write
File: path/to/file.xlsx
Sheet: "SheetName"
Target: Single cell reference (A1) or range (A1:A10)
Value: Formula starting with = or literal value
Options: Preserve formatting, overwrite mode
```

### Working with Multiple Sheets
Reference sheets by name when:
- Reading from source data sheet and writing to results sheet
- Using cross-sheet formulas (SheetName!CellRef)
- Analyzing relationships between sheets

**Cross-sheet formula pattern:**
```
=Sheet1!A1  (reference cell in another sheet)
='Sheet Name'!A1  (if sheet name has spaces)
```

### Range Operations

**Single Row/Column:**
```
H12 (single cell)
H12:L12 (row range, 5 columns)
H12:H40 (column range, multiple rows)
```

**Multiple Ranges:**
```
H12:L17, H19:L24, H26:L31 (list separate ranges)
```

**2D Range with formulas:**
```
H12:L17 contains 6 rows × 5 columns = 30 cells
Fill with formula that references row/column criteria
```

## Specific Patterns for This Task

### Two-Condition Lookup Pattern
When filling ranges based on two criteria (Series Code in column, Year in row):

**Formula template:**
```
=INDEX(lookup_source_range, MATCH(row_series_code, lookup_column, 0), MATCH(header_year, lookup_row, 0))
```

**Implementation steps:**
1. Identify source data location (e.g., Data!A21:G40)
2. Identify lookup columns/rows (Series codes in Data column D, Years in Data row 10)
3. Create INDEX formula with nested MATCH functions
4. Use absolute references ($) for source ranges
5. Use mixed references for criteria (varies by row/column)

### Formula Writing Approach
When writing formulas to multiple cells in a range:

**Option 1: Write one formula with relative references**
- Write formula to first cell (e.g., H12)
- Use relative references for criteria that change by position
- Use absolute references for source data ($Data$A$21:$G$40)
- Copy formula across/down

**Option 2: Write individual formulas**
- Each cell gets specific MATCH values
- Useful if pattern varies
- More explicit but more complex

### Batch Operations
Write multiple cells efficiently by:
- Grouping cells by formula type
- Using ranges instead of individual cells
- Reusing formula patterns with position adjustments

## Excel Formula Reference Syntax

### Absolute vs Relative References
```
A1      - Relative (changes when copied)
$A$1    - Absolute (stays same when copied)
$A1     - Column absolute, row relative
A$1     - Column relative, row absolute
```

### Sheet References
```
Sheet1!A1        (no spaces in name)
'Sheet Name'!A1  (spaces require quotes)
Data!A21:G40     (range reference)
Data!$A$21:$G$40 (absolute range)
```

### Array Formula Considerations
Some functions like MATCH used in arrays may:
- Require Ctrl+Shift+Enter in traditional Excel
- Work normally in Excel 365
- Need special syntax handling in xlsx tool

## Validation Steps

1. **Preview data structure**: Read the sheet to understand layout
2. **Verify criteria**: Confirm all lookup values exist in source data
3. **Test formula**: Write to one cell first, verify result
4. **Batch write**: Copy tested formula to remaining cells
5. **Spot check**: Verify a few calculated values manually

## Common Issues and Solutions

### Formula not calculating
- Ensure equals sign (=) at start
- Check sheet name references
- Verify cell references exist in source data
- Check for typos in function names

### Incorrect data returned
- Verify MATCH is finding correct position
- Check INDEX range includes target data
- Ensure criteria values match exactly (case-sensitive in some functions)

### Range reference errors
- Include full sheet path if cross-sheet: Sheet!A1:Z100
- Use quotes if sheet name has spaces: 'Sheet Name'!A1
- Verify range bounds are correct for data size

## Performance Tips

1. Use efficient ranges (don't include entire columns if A1:A100 suffices)
2. Prefer XLOOKUP over INDEX/MATCH if available
3. Use MATCH with exact match (0) for performance
4. Test formulas before applying to large ranges
5. Group batch writes to minimize file operations
