---
name: d3-cross-highlighting
description: How to implement cross-highlighting between D3.js visualizations and HTML Data Tables. Use this skill whenever the user wants to connect a chart (like a bubble chart or scatter plot) with an HTML table, so clicking or hovering one updates the other.
---

# d3-cross-highlighting

This skill explains how to synchronize state between a D3.js chart and an HTML `<table/>` to enable cross-highlighting (e.g., clicking a bubble highlights the table row, clicking a table row highlights the bubble).

## Architecture

1.  **Unique Identifiers:** Ensure every data row has a unique identifier (like an ID or a ticker symbol).
2.  **State Management:** Keep track of the currently selected identifier.
3.  **Render/Update Logic:** Write a function that updates the visual state of both the SVG chart and the HTML table based on the selected identifier.
4.  **Event Listeners:** Attach click/hover listeners to both SVG shapes and HTML table rows that trigger the update logic.

## Example Implementation

### Setup Data and Table

```javascript
// Data must have a unique ID, e.g., 'ticker'
const data = [
  { ticker: "AAPL", name: "Apple", value: 100 },
  { ticker: "MSFT", name: "Microsoft", value: 95 }
];

let selectedTicker = null; // Global state for selection

// Render HTML table rows
const tableBody = d3.select("#data-table tbody");
const rows = tableBody.selectAll("tr")
  .data(data, d => d.ticker)
  .join("tr")
  .attr("id", d => `row-${d.ticker}`) // Optional, useful for scrolling
  .on("click", (event, d) => {
    // Toggle selection
    selectedTicker = selectedTicker === d.ticker ? null : d.ticker;
    updateSelection();
  });

rows.selectAll("td")
  .data(d => [d.ticker, d.name, d.value])
  .join("td")
  .text(d => d);
```

### Setup SVG Chart

```javascript
// Render bubbles
const bubbles = svg.selectAll("circle")
  .data(data, d => d.ticker)
  .join("circle")
  .attr("class", "chart-bubble")
  // ... other attributes like r, cx, cy ...
  .on("click", (event, d) => {
    // Toggle selection
    selectedTicker = selectedTicker === d.ticker ? null : d.ticker;
    updateSelection();
  });
```

### Update Function

This function applies visual changes to both the table and the chart based on the `selectedTicker`.

```javascript
function updateSelection() {
  // Update Table Rows
  rows.classed("highlighted-row", d => d.ticker === selectedTicker);
  
  // Optionally, scroll the table to show the highlighted row
  if (selectedTicker) {
    const rowElement = document.getElementById(`row-${selectedTicker}`);
    if (rowElement) {
      rowElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  // Update SVG Bubbles
  bubbles
    .classed("highlighted-bubble", d => d.ticker === selectedTicker)
    .attr("stroke", d => d.ticker === selectedTicker ? "black" : "none")
    .attr("stroke-width", d => d.ticker === selectedTicker ? 3 : 0)
    .style("opacity", d => (selectedTicker === null || selectedTicker === d.ticker) ? 1 : 0.3);
}
```

## CSS Styling

Define classes to visually emphasize the selected state.

```css
/* Table highlighting */
.highlighted-row {
  background-color: #ffffcc;
  font-weight: bold;
}

/* Bubble highlighting */
.highlighted-bubble {
  /* Typically handled via SVG attributes or stroke, but can also use CSS */
}

/* Base styles for transition */
.chart-bubble {
  transition: opacity 0.2s, stroke 0.2s;
  cursor: pointer;
}
tr {
  cursor: pointer;
}
```

## Considerations

-   **Hover vs. Click:** If implementing hover logic, track a `hoveredTicker` variable and apply CSS classes similarly in an `updateHoverSelection()` function, attaching it to `"mouseenter"` and `"mouseleave"` events.
-   **Performance:** For very large datasets, using `.classed()` on D3 selections is efficient, as it batches DOM updates.
