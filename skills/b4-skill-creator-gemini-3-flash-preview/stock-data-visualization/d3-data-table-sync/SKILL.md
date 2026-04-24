name: d3-data-table-sync
description: How to create a data table synced with a D3.js visualization for bidirectional highlighting. Use this whenever a table and a chart need to interact.

## Implementation Guide

### 1. Table Creation
Generate the table rows using D3's data binding.
```javascript
const table = d3.select("#table-container").append("table");
const tbody = table.append("tbody");

const rows = tbody.selectAll("tr")
    .data(data)
    .enter()
    .append("tr")
    .attr("id", d => `row-${d.ticker}`);

rows.append("td").text(d => d.ticker);
// ... other cells
```

### 2. Bidirectional Highlighting
Implement a common highlighting function.

#### Chart to Table:
```javascript
node.on("click", (event, d) => {
    d3.selectAll("tr").classed("highlight", false);
    d3.select(`#row-${d.ticker}`).classed("highlight", true);
    document.getElementById(`row-${d.ticker}`).scrollIntoView({ behavior: 'smooth', block: 'center' });
});
```

#### Table to Chart:
```javascript
rows.on("click", (event, d) => {
    d3.selectAll("circle").classed("highlight", false);
    d3.selectAll("circle")
      .filter(circleData => circleData.ticker === d.ticker)
      .classed("highlight", true);
    
    d3.selectAll("tr").classed("highlight", false);
    d3.select(event.currentTarget).classed("highlight", true);
});
```

### 3. Formatting Numbers
Use `d3.format` for human-readable numbers.
```javascript
const formatMarketCap = d3.format(".2s"); // e.g., 1.6T
// Custom formatter for trillion/billion
function formatLargeNumber(n) {
    if (n >= 1e12) return (n / 1e12).toFixed(2) + "T";
    if (n >= 1e9) return (n / 1e9).toFixed(2) + "B";
    return n;
}
```
