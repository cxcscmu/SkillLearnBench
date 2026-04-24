---
name: visualization_logic_implementation
description: Implements the D3.js force simulation, tooltips, and data interaction logic in visualization.js.
---
Implement `visualization.js` with the following structure:
1. Wrap logic in `document.addEventListener('DOMContentLoaded', async () => { ... });`.
2. Load data: Use `d3.csv("./data/stock-descriptions.csv")`.
3. Bubble Chart: 
   - Define a `d3.forceSimulation`.
   - Use `d3.forceX` and `d3.forceY` grouped by sector name to create clusters.
   - Use `d3.forceCollide` based on bubble radius to prevent overlap.
   - Scale radius using `d3.scaleSqrt` for market cap (handle missing values for ETFs).
4. Tooltips: Append a hidden `div` to the body. On mouseover, update and show the tooltip for stocks (filter out ETFs using the sector or market cap null-check).
5. Interactivity:
   - Add click listeners to circles to add a CSS class (e.g., `.highlight`) and trigger `scrollIntoView` on the corresponding table row.
   - Add click listeners to table rows to find the corresponding bubble and highlight it.