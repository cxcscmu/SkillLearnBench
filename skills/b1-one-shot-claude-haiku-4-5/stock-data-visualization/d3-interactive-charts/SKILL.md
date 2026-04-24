---
name: d3-interactive-charts
description: D3.js techniques for tooltips, hover effects, click handlers, and cross-filtering between visualizations
---

# D3.js Interactive Charts

## Overview
Making D3 charts interactive with tooltips, highlighting, and coordinated interactions between multiple charts.

## 1. Tooltips

### HTML Tooltip (Best for Hover)
```javascript
// Create tooltip div
const tooltip = d3.select("body")
  .append("div")
  .attr("class", "tooltip")
  .style("position", "absolute")
  .style("background", "rgba(0,0,0,0.8)")
  .style("color", "white")
  .style("padding", "8px 12px")
  .style("border-radius", "4px")
  .style("pointer-events", "none")
  .style("opacity", 0)
  .style("z-index", 1000);

// Add mouseover handlers
circles
  .on("mouseover", (event, d) => {
    tooltip
      .style("opacity", 1)
      .html(`<strong>${d.ticker}</strong><br/>${d.name}<br/>${d.sector}`)
      .style("left", event.pageX + 10 + "px")
      .style("top", event.pageY + 10 + "px");
  })
  .on("mousemove", (event) => {
    tooltip
      .style("left", event.pageX + 10 + "px")
      .style("top", event.pageY + 10 + "px");
  })
  .on("mouseout", () => {
    tooltip.style("opacity", 0);
  });
```

### CSS Styling for Tooltip
```css
.tooltip {
  position: absolute;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.85);
  color: white;
  border-radius: 4px;
  font-size: 12px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
  z-index: 1000;
  white-space: nowrap;
}
```

## 2. Hover Effects

### Highlight on Hover
```javascript
circles
  .on("mouseover", (event, d) => {
    // Highlight the hovered circle
    d3.select(event.currentTarget)
      .transition()
      .duration(200)
      .attr("opacity", 1)
      .attr("stroke", "black")
      .attr("stroke-width", 2);

    // Fade other circles
    circles.filter(nd => nd.id !== d.id)
      .transition()
      .duration(200)
      .attr("opacity", 0.3);
  })
  .on("mouseout", () => {
    // Restore all
    circles
      .transition()
      .duration(200)
      .attr("opacity", 1)
      .attr("stroke", "none");
  });
```

## 3. Click Handlers & Selection

### Click to Select
```javascript
let selectedId = null;

circles
  .on("click", (event, d) => {
    selectedId = (selectedId === d.id) ? null : d.id;

    circles
      .attr("opacity", nd => selectedId === null || nd.id === selectedId ? 1 : 0.3)
      .attr("stroke", nd => nd.id === selectedId ? "black" : "none")
      .attr("stroke-width", nd => nd.id === selectedId ? 2 : 0);

    // Trigger update in other visualizations
    updateTable(selectedId);
  });
```

## 4. Cross-Filtering Between Charts

### Pattern: Coordinating Multiple Visualizations

```javascript
// Define shared selection state
let selectedTicker = null;

// Update when bubble is clicked
function selectBubble(ticker) {
  selectedTicker = ticker;

  // Highlight bubble
  circles.attr("opacity", d => d.ticker === ticker ? 1 : 0.3);

  // Highlight table row
  tableRows.attr("class", d => d.ticker === ticker ? "selected" : "");
}

// Update when table row is clicked
function selectTableRow(ticker) {
  selectedTicker = ticker;

  // Highlight table row
  tableRows.attr("class", d => d.ticker === ticker ? "selected" : "");

  // Highlight bubble
  circles.attr("opacity", d => d.ticker === ticker ? 1 : 0.3);
}

// Setup handlers
circles.on("click", (event, d) => {
  selectBubble(d.ticker);
});

tableRows.on("click", (event, d) => {
  selectTableRow(d.ticker);
});
```

### CSS for Selection Highlighting
```css
.selected {
  background-color: #FFC700 !important;
  font-weight: bold;
}

tr.selected {
  background-color: #FFC700;
}
```

## 5. Dynamic Updates (Filtering/Sorting)

### Update visualization when data changes
```javascript
function updateChart(newData) {
  // Update scales
  colorScale.domain(Array.from(new Set(newData.map(d => d.sector))));

  // Rebind data
  circles = circles.data(newData, d => d.id);

  // Enter + Update + Exit pattern
  circles
    .join(
      enter => enter.append("circle")
        .attr("r", d => rScale(d.value))
        .attr("fill", d => colorScale(d.sector)),
      update => update,
      exit => exit.remove()
    )
    .transition()
    .duration(500)
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y));
}
```

## 6. Cursor & Visual Feedback

### Indicate Interactivity
```css
circle {
  cursor: pointer;
  transition: opacity 0.2s, stroke 0.2s;
}

circle:hover {
  cursor: pointer;
}

tr:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}
```

## 7. Event Delegation

### Handle events on parent, not children
```javascript
// Less efficient - attaches handler to many elements
circles.on("click", handler);

// More efficient - single handler on parent
g.on("click", (event, d) => {
  if (event.target.tagName === "circle") {
    handleCircleClick(d);
  }
});
```

## Best Practices
- Use `event.currentTarget` vs `this` for modern D3
- Debounce mousemove events for performance
- Clean up event handlers when removing visualizations
- Use CSS transitions alongside D3 transitions for smooth UX
- Provide visual feedback for all interactive elements
