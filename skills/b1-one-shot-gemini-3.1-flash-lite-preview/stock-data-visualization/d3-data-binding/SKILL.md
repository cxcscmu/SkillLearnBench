---
name: d3-data-binding
description: Efficiently binding data to DOM elements and handling user interactions like hover and click in D3.js.
---

# D3 Data Binding & Interactivity

Use the D3 enter/update/exit pattern to synchronize DOM with data.

## Implementation Pattern

```javascript
// Data binding
const bubbles = svg.selectAll(".bubble")
  .data(nodes)
  .join("circle")
  .attr("class", "bubble")
  .on("click", (event, d) => {
    highlightRow(d.ticker);
  });

// Tooltip
bubbles.on("mouseover", (event, d) => {
    d3.select("#tooltip")
      .style("display", "block")
      .html(`${d.ticker}: ${d.name}`);
})
.on("mouseout", () => {
    d3.select("#tooltip").style("display", "none");
});
```
