---
name: d3-data-table
description: Build interactive HTML data tables with D3.js v6, including row highlighting and click-based selection synced with charts.
---

# D3.js v6 Data Table with Interactivity

## Creating a Table with D3
```js
const table = d3.select("#table-container").append("table");
const thead = table.append("thead").append("tr");
const columns = ["Ticker", "Name", "Sector", "Market Cap"];
thead.selectAll("th").data(columns).join("th").text(d => d);

const tbody = table.append("tbody");
const rows = tbody.selectAll("tr").data(data).join("tr")
  .attr("data-ticker", d => d.ticker);

rows.selectAll("td").data(d => [d.ticker, d.name, d.sector, d.marketCapFormatted])
  .join("td").text(d => d);
```

## Formatting Market Cap
```js
function formatMarketCap(val) {
  if (!val) return "N/A";
  if (val >= 1e12) return (val / 1e12).toFixed(2) + "T";
  if (val >= 1e9) return (val / 1e9).toFixed(2) + "B";
  if (val >= 1e6) return (val / 1e6).toFixed(2) + "M";
  return val.toLocaleString();
}
```

## Bidirectional Selection
- On bubble click: highlight corresponding row, scroll into view
- On row click: highlight corresponding bubble
- Use a shared `selectStock(ticker)` function
