---
name: Data Retrieval using INDEX and MATCH
description: Use INDEX combined with MATCH to retrieve data from a source table based on two criteria (row and column headers).
---
To retrieve data from the 'Data' sheet into the 'Task' sheet:
1. Use the formula: `=INDEX(Data!$E$21:$Z$40, MATCH($D12, Data!$D$21:$D$40, 0), MATCH(H$10, Data!$E$20:$Z$20, 0))`.
2. Ensure the row index (column D) and column index (year header in row 10) are locked appropriately with `$` signs to allow dragging across the target ranges (H12:L17, H19:L24, and H26:L31).
3. Verify that the array range `Data!$E$21:$Z$40` exactly matches the source data bounds specified in the requirements.