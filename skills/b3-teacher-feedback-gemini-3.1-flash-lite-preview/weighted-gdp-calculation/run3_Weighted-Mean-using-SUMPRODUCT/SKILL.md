---
name: Weighted Mean using SUMPRODUCT
description: Calculate the weighted mean by multiplying Net Exports % by the corresponding GDP values and dividing by the total GDP.
---
1. Define the weighted mean formula: `=ROUND(SUMPRODUCT(NetExportsRange, GDPRange) / SUM(GDPRange), 1)`.
2. Ensure `NetExportsRange` and `GDPRange` have the exact same dimensions and orientation corresponding to the GCC countries for the given year.
3. Verify that the calculation multiplies by 100 if the source data is in decimal format (e.g., `0.123`) to ensure the final output reflects the `12.3` requirement.
4. If the source data is already in percentage format (e.g., `12.3`), simply use the formula above without multiplying by 100, ensuring the final `ROUND(..., 1)` satisfies the precision requirement.