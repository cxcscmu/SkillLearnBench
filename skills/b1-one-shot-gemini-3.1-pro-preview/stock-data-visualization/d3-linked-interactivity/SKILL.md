---
name: d3-linked-interactivity
description: Guide for linking D3.js SVG visualizations with DOM elements like HTML tables for bidirectional interactivity (hover, click, highlight).
---

# D3 Linked Interactivity

Bidirectional interactivity allows a user to interact with one chart (e.g., a bubble) and see updates in another component (e.g., a table row).

## Implementation

1. **Assign unique IDs or Classes**: Ensure both the SVG elements and Table rows share a common data key, like an ID or Ticker.
```javascript
// Table rows
const rows = tbody.selectAll("tr")
  .data(data)
  .enter()
  .append("tr")
  .attr("id", d => `row-${d.id}`);

// SVG Nodes
const nodes = svg.selectAll("circle")
  .data(data)
  .enter()
  .append("circle")
  .attr("id", d => `node-${d.id}`);
```

2. **Event Listeners**:
Add `click` or `mouseover` events that select the linked element and toggle a highlighted state.

```javascript
nodes.on("click", function(event, d) {
  // Reset all
  d3.selectAll(".highlight").classed("highlight", false);
  
  // Highlight self and linked row
  d3.select(this).classed("highlight", true);
  d3.select(`#row-${d.id}`).classed("highlight", true);
  
  // Scroll row into view
  document.getElementById(`row-${d.id}`).scrollIntoView({ behavior: 'smooth', block: 'center' });
});

rows.on("click", function(event, d) {
  d3.selectAll(".highlight").classed("highlight", false);
  d3.select(this).classed("highlight", true);
  d3.select(`#node-${d.id}`).classed("highlight", true);
});
```
