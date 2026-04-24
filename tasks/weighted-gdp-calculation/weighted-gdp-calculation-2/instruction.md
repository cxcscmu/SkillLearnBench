You need to calculate the weighted mean of the Trade Balance Coefficient for the GCC countries in the file `gdp.xlsx`. The workbook contains two sheets: "Task" (where you will enter formulas) and "Data" (source data). Please work only within these existing sheets.

Step 1: The data you need for this problem are located in sheet "Data", rows 21 to 33. Please use the VLOOKUP&MATCH, HLOOKUP&MATCH, XLOOKUP&MATCH, or INDEX&MATCH functions to fill in the data in the yellow cell ranges H12:M17 and H19:M24 by using two conditions: (i) series code (in column D)  and (ii) year (in row 10). Both conditions are highlighted in blue.

Step 2: Calculate Trade Balance Coefficients for all six GCC countries in yellow cells H28:M33. Then calculate the min, max, median, simple mean, 25th percentile, and 75th percentiles.

> $$\text{Trade Balance Coefficient} = \frac{\text{Exports} - \text{Imports}}{\text{Exports} + \text{Imports}}$$

Step 3: Please calculate the Trade Balance Coefficients as percent of total trade volume (exports + imports) weighted mean for the GCC by using the SUMPRODUCT formula.

You should not change the original format of the file, including the colors, fonts, etc. You also should not add any macros, VBA code, or other customizations to the excel.  Ensure all the percentage results in step 2 and 3 are rounded to one decimal place. (e.g., if the result is 12.3%, the cell should display 12.3 rather than 0.123). You may achieve this by multiplying the final calculation by 100 within your formula.