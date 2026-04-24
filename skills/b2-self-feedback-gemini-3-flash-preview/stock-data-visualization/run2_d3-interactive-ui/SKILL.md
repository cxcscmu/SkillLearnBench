---
name: run2_d3-interactive-ui
description: Enhancing user experience with polished tooltips, table interactions, and smooth transitions.
---

# Polished D3 Interactive UI

This skill covers refining the visual feedback and interactivity of the web app.

## Better Tooltip Positioning

Use the mouse event to position tooltips accurately, ensuring they don't clip off the screen.

```javascript
.on("mousemove", (event) => {
    tooltip.style("left", (event.pageX + 15) + "px")
           .style("top", (event.pageY - 15) + "px");
})
```

## Bi-directional Linkage

Ensure that clicking either the bubble or the table row triggers the same state update.

```javascript
function selectStock(ticker) {
    // Update visual state of all elements
    d3.selectAll(".bubble").classed("selected", d => d.ticker === ticker);
    d3.selectAll("tr").classed("selected-row", d => d.ticker === ticker);
    
    // Scroll table
    const row = d3.select(`#row-${ticker}`).node();
    if (row) row.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
```

## Styling for Interactivity

Use CSS for hover effects and clear selection states.

```css
.bubble { transition: r 0.1s; cursor: pointer; }
.bubble:hover { stroke: #000; stroke-width: 2px; }
.selected-row { background-color: #e3f2fd !important; font-weight: bold; }
```
