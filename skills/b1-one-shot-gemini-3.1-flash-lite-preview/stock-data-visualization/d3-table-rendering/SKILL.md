---
name: d3-table-rendering
description: Creating data-driven HTML tables using D3.js.
---

# D3 Data Table Rendering

Use d3-selection to create rows and cells from JSON data.

## Implementation Pattern

```javascript
const table = d3.select("#table-container").append("table");
const thead = table.append("thead");
const tbody = table.append("tbody");

// Append columns
thead.append("tr").selectAll("th")
  .data(columns).enter().append("th").text(d => d);

// Create rows
const rows = tbody.selectAll("tr")
  .data(data).enter().append("tr")
  .on("click", (event, d) => highlightBubble(d.ticker));

// Populate cells
rows.selectAll("td")
  .data(d => columns.map(col => d[col]))
  .enter().append("td").text(d => d);
```
