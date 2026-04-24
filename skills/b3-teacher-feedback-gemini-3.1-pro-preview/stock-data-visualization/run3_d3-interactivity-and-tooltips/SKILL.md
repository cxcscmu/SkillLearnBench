---
name: d3-interactivity-and-tooltips
description: HTML/CSS/JS patterns for creating tooltips, conditional interactions based on data attributes, and cross-highlighting elements across different views (like a chart and a table).
---

### 1. Tooltip HTML/CSS/JS Pattern

To create a dynamic tooltip, use a hidden HTML `div` that is styled with CSS and positioned dynamically using JavaScript mouse events.

**HTML Pattern:**
```html
<!-- Place this somewhere in your HTML body, outside the SVG -->
<div id="tooltip" class="tooltip"></div>
```

**CSS Pattern:**
```css
.tooltip {
  position: absolute;
  opacity: 0; /* Hidden by default */
  pointer-events: none; /* Prevents the tooltip from interfering with mouse events */
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-family: sans-serif;
  font-size: 12px;
  /* Add transition for smooth appearance */
  transition: opacity 0.2s;
}
```

**JavaScript Pattern:**
Bind `mouseover`, `mousemove`, and `mouseout` events to your D3 selection. Position the tooltip using `event.pageX` and `event.pageY`.

```javascript
const tooltip = d3.select("#tooltip");

nodes.on("mouseover", function(event, d) {
    tooltip.style("opacity", 1); // Make visible
    tooltip.html(`<strong>${d.name}</strong><br>Value: ${d.value}`);
})
.on("mousemove", function(event, d) {
    // Offset by a few pixels so the cursor doesn't cover the tooltip
    tooltip.style("left", (event.pageX + 10) + "px")
           .style("top", (event.pageY + 10) + "px");
})
.on("mouseout", function(event, d) {
    tooltip.style("opacity", 0); // Hide
});
```

### 2. Conditional Interactions Pattern

Sometimes interactions (like tooltips) should only trigger for specific data points (e.g., skip entries missing certain fields). Wrap the logic inside your event listeners with a condition.

```javascript
nodes.on("mouseover", function(event, d) {
    // Conditional Interaction: Only show tooltip if the node is NOT an ETF
    if (d.type !== "ETF") {
        tooltip.style("opacity", 1);
        tooltip.html(`Ticker: ${d.ticker}<br>Market Cap: ${d.marketCap}`);
    }
})
.on("mousemove", function(event, d) {
    if (d.type !== "ETF") {
        tooltip.style("left", (event.pageX + 10) + "px")
               .style("top", (event.pageY + 10) + "px");
    }
})
.on("mouseout", function(event, d) {
    tooltip.style("opacity", 0);
});
```

### 3. Cross-Highlighting Pattern

To connect two different views (like a bubble chart and a table), assign common identifiers to both elements and toggle a specific CSS class (e.g., `.selected`) on click.

**CSS Pattern:**
```css
/* Styling for highlighted bubble */
.bubble.selected {
  stroke: #000;
  stroke-width: 3px;
}

/* Styling for highlighted table row */
.table-row.selected {
  background-color: #ffff99;
  font-weight: bold;
}
```

**JavaScript Pattern:**
Attach a click handler that removes the `.selected` class from all elements, then adds it back only to the elements matching the clicked data.

```javascript
// Give bubbles a class of 'bubble' and rows a class of 'table-row'
function handleSelection(event, d) {
    // 1. Remove the 'selected' class from ALL bubbles and rows
    d3.selectAll(".bubble").classed("selected", false);
    d3.selectAll(".table-row").classed("selected", false);
    
    // 2. Add the 'selected' class to the specific bubble and row matching the clicked data
    // Assuming both data objects share a unique 'ticker' property
    d3.selectAll(".bubble")
      .filter(nodeData => nodeData.ticker === d.ticker)
      .classed("selected", true);
      
    d3.selectAll(".table-row")
      .filter(rowData => rowData.ticker === d.ticker)
      .classed("selected", true);
}

// Bind the event listener to both the chart nodes and the table rows
d3.selectAll(".bubble").on("click", handleSelection);
d3.selectAll(".table-row").on("click", handleSelection);
```