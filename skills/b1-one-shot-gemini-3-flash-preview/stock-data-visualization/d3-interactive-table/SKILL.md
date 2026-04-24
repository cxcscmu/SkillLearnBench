---
name: d3-interactive-table
description: Building dynamic tables with D3 and implementing bidirectional interactions with SVG elements.
---

# Interactive D3 Data Tables

D3 is highly effective for binding data to HTML tables and synchronizing state between the table and other visualizations like SVG charts.

## Table Structure
Use `selectAll`, `data`, and `join` to create table rows and cells.

```javascript
const table = d3.select("#table-container").append("table");
const tbody = table.append("tbody");

const rows = tbody.selectAll("tr")
    .data(data)
    .join("tr")
    .attr("id", d => `row-${d.ticker}`)
    .on("click", (event, d) => highlightStock(d.ticker));

rows.selectAll("td")
    .data(d => [d.ticker, d.name, d.sector, d.marketCap])
    .join("td")
    .text(d => d);
```

## Bidirectional Linking
To connect a chart (SVG) and a table:
1.  **Unique Identifiers**: Use a common ID (like ticker symbol) for both the SVG circles and the table rows.
2.  **Selection State**: Define a function that updates CSS classes or attributes for both elements simultaneously.

```javascript
function highlightStock(ticker) {
    // Reset previous highlights
    d3.selectAll(".highlighted").classed("highlighted", false);

    // Highlight row
    d3.select(`#row-${ticker}`).classed("highlighted", true);
    
    // Highlight bubble
    d3.select(`#bubble-${ticker}`).classed("highlighted", true);
    
    // Scroll table to row
    document.getElementById(`row-${ticker}`).scrollIntoView({ behavior: 'smooth', block: 'center' });
}
```
