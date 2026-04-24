# excel-formatting-and-units

Handling percentages, rounding, and preserving workbook styles. Use this skill whenever a task requires specific output formats like decimal rounding or percentage conversions without changing existing workbook formatting.

## Displaying Percentages as Whole Numbers
If the user requests a result to be displayed as `12.3` for `12.3%`:
- **Formula:** `=(Raw_Calculation) * 100`
- Combined with rounding: `=ROUND((Raw_Calculation) * 100, 1)`

## Preserving Workbook Formatting
When updating cells with new formulas, it's critical to maintain the existing visual style:
- **Style Overwrite:** Avoid any operations that replace cell styles (colors, borders, fonts).
- **Data Insertion:** Only modify the cell value or formula property, not the entire cell object.
- **Excel Colors:** Use industry standards (Blue for inputs, Black for formulas) if the template is empty, but **always follow the existing pattern first**.

## Working with Specific Cell Ranges
When the user specifies a range (e.g., `H12:L17`), ensure every cell in that range is correctly populated with the intended logic.
- Verify the start and end of the range.
- Use consistent relative/absolute references for easier formula application.
