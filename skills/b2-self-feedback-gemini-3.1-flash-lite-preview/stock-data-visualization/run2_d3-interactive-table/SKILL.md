---
name: run2_d3-interactive-table
description: Improving interaction between D3 charts and HTML tables with selection events.
---
# Advanced Interaction Linking

Synchronize table and chart selection using a centralized state or event listener:

```javascript
// Add event listener to rows
rows.on("mouseover", (event, d) => {
    d3.select("#" + d.ticker).classed("hovered", true);
    d3.selectAll("circle").filter(c => c.ticker === d.ticker).attr("stroke", "orange");
});
```
