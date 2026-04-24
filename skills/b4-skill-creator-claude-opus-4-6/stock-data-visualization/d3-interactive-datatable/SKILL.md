---
name: d3-interactive-datatable
description: >
  Build interactive data tables with D3.js that are linked to other D3 visualizations.
  Use this skill when building HTML tables with D3 that need click-to-highlight interaction,
  synchronized selection with charts, or formatted numeric columns. Triggers on: data table,
  interactive table, linked table and chart, click to highlight.
---

# D3 Interactive Data Table

## Overview

Create HTML `<table>` elements using D3's data join pattern, with click-based interaction
that synchronizes with other visualizations (e.g., a bubble chart).

## Building the Table

```js
const table = d3.select("#table-container")
  .append("table");

const thead = table.append("thead").append("tr");
thead.selectAll("th")
  .data(columns)
  .join("th")
  .text(d => d.label);

const tbody = table.append("tbody");
const rows = tbody.selectAll("tr")
  .data(data)
  .join("tr")
  .attr("data-ticker", d => d.ticker);

rows.selectAll("td")
  .data(d => columns.map(col => col.accessor(d)))
  .join("td")
  .text(d => d);
```

## Formatting Market Cap

Format large numbers into human-readable form (e.g., 1.64T, 345.98B):

```js
function formatMarketCap(value) {
  if (!value) return "N/A";
  if (value >= 1e12) return (value / 1e12).toFixed(2) + "T";
  if (value >= 1e9) return (value / 1e9).toFixed(2) + "B";
  if (value >= 1e6) return (value / 1e6).toFixed(2) + "M";
  return value.toLocaleString();
}
```

## Click-to-Highlight Synchronization

### Pattern: Shared Selection State

Maintain a shared selection state and update both the chart and the table when selection changes.

```js
function selectStock(ticker) {
  // Highlight the table row
  d3.selectAll("#table-container tr")
    .classed("highlighted", d => d && d.ticker === ticker);

  // Highlight the bubble
  d3.selectAll(".bubble")
    .classed("highlighted", d => d.ticker === ticker);

  // Scroll the table row into view
  const row = document.querySelector(`tr[data-ticker="${ticker}"]`);
  if (row) row.scrollIntoView({ behavior: "smooth", block: "center" });
}
```

### Binding Click Events

```js
// On bubble click
bubbles.on("click", (event, d) => selectStock(d.ticker));

// On table row click
rows.on("click", (event, d) => selectStock(d.ticker));
```

## Styling

- Use `position: sticky` on `<thead>` for scrollable tables
- Highlight rows with a distinct background color on `.highlighted` class
- Add hover effects on rows for discoverability
- Use alternating row colors for readability
