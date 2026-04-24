---
name: excel-lookup-functions
description: Master Excel lookup functions (VLOOKUP, HLOOKUP, INDEX/MATCH, XLOOKUP) for single and multiple criteria.
---

# Excel Lookup Functions

## Overview
Lookup functions allow you to find and retrieve data from tables based on criteria. Different functions suit different scenarios.

## Function Comparison

### VLOOKUP (Vertical Lookup)
Searches for a value in the first column of a range and returns a value in the same row from another column.

**Syntax:**
```
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

**Limitations:**
- Can only search in the first column
- Lookup column must be to the left of return column
- Cannot handle multiple criteria easily

**Example:**
```
=VLOOKUP("Series_A", Data!A:D, 3, FALSE)
```

### HLOOKUP (Horizontal Lookup)
Searches for a value in the first row of a range and returns a value in the same column from another row.

**Syntax:**
```
=HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])
```

**Use Case:**
When data is organized horizontally with lookup values in the top row.

**Example:**
```
=HLOOKUP(2020, Data!A1:F10, 3, FALSE)
```

### INDEX & MATCH (Flexible Lookup)
INDEX returns a value from a specific position in a range. MATCH finds the position of a value.

**Syntax:**
```
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
```

**Advantages:**
- Works with data in any position
- Can be modified for multiple criteria
- More flexible than VLOOKUP

**Example (Single Criterion):**
```
=INDEX(Data!$C$1:$C$100, MATCH("Series_A", Data!$A$1:$A$100, 0))
```

**Example (Multiple Criteria):**
```
=INDEX(Data!$E$1:$E$100, MATCH(1, (Data!$A$1:$A$100=criteria1)*(Data!$B$1:$B$100=criteria2), 0))
```
Note: This requires Ctrl+Shift+Enter (array formula) in traditional Excel.

### XLOOKUP (Modern Solution)
Available in Excel 365 and newer versions. Combines benefits of VLOOKUP and INDEX/MATCH.

**Syntax:**
```
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```

**Advantages:**
- Simpler syntax than INDEX/MATCH
- Can search left or right
- Built-in error handling
- Native support for multiple criteria

**Example (Single Criterion):**
```
=XLOOKUP("Series_A", Data!$A:$A, Data!$C:$C)
```

**Example (Multiple Criteria with FILTER):**
```
=XLOOKUP(1, (Data!$A:$A=criteria1)*(Data!$B:$B=criteria2), Data!$C:$C)
```

## Multiple Criteria Pattern

When you need to lookup based on TWO conditions (e.g., Series Code AND Year):

### Using INDEX & MATCH
```
=INDEX(return_range, MATCH(1, (condition1_range=condition1_value)*(condition2_range=condition2_value), 0))
```
Enter as array formula with Ctrl+Shift+Enter.

### Using XLOOKUP (Recommended for Excel 365)
```
=XLOOKUP(1, (lookup_range1=criteria1)*(lookup_range2=criteria2), return_range, "Not Found")
```

### Practical Example
Finding a value by Series Code (Column A) and Year (Row 10 headers):
```
=INDEX(Data!$C$21:$G$40, MATCH(Series_Code, Data!$A$21:$A$40, 0), MATCH(Year, Data!$C$10:$G$10, 0))
```

## Best Practices

1. **Use Absolute References**: Lock ranges with $ for reusability
   ```
   =INDEX(Data!$C$21:$G$40, ...)
   ```

2. **Handle Errors**: Use IFERROR to manage missing data
   ```
   =IFERROR(INDEX(...), "N/A")
   ```

3. **Test Criteria**: Verify both lookup values exist before using complex formulas

4. **Choose by Complexity**:
   - Single criterion → VLOOKUP/HLOOKUP
   - Multiple criteria → INDEX/MATCH or XLOOKUP
   - Modern Excel (365) → XLOOKUP preferred

5. **Performance**: For large datasets, INDEX/MATCH with array formulas may be slower than VLOOKUP on first column
