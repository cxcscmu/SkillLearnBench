---
name: d3-data-table
description: >
  How to build an interactive HTML data table driven by D3.js v6 with sortable
  columns, row highlighting, cross-component selection, and formatted values.
  Use this skill when building tabular displays alongside D3 charts, especially
  when the table needs to stay in sync with chart interactions.
---

# D3 v6 Interactive Data Table

## Basic Table Rendering with D3

```js
const tbody = d3.select("#table-container table tbody");
const rows = tbody.selectAll("tr")
  .data(data, d => d.ticker)
  .join("tr")
  .attr("data-ticker", d => d.ticker);

rows.selectAll("td")
  .data(d => [d.ticker, d.name, d.sector, formatMarketCap(d.marketCap)])
  .join("td")
  .text(d => d);
```

## Formatting Market Cap

```js
function formatMarketCap(value) {
  if (!value || isNaN(+value)) return "—";
  const v = +value;
  if (v >= 1e12) return (v / 1e12).toFixed(2) + "T";
  if (v >= 1e9)  return (v / 1e9).toFixed(2) + "B";
  if (v >= 1e6)  return (v / 1e6).toFixed(2) + "M";
  return v.toLocaleString();
}
```

## Row Highlighting

Use a CSS class for selected state, toggled via D3:

```css
tr.highlighted { background-color: #fffbe6; outline: 2px solid #f0b429; }
```

```js
function highlightRow(ticker) {
  d3.selectAll("tr").classed("highlighted", false);
  const row = d3.select(`tr[data-ticker="${ticker}"]`);
  row.classed("highlighted", true);
  // Scroll into view
  const el = row.node();
  if (el) el.scrollIntoView({ behavior: "smooth", block: "nearest" });
}
```

## Cross-Component Sync

Listen for events dispatched by the bubble chart:

```js
document.addEventListener("stockSelected", e => highlightRow(e.detail));
```

Emit events when a row is clicked:

```js
rows.on("click", (event, d) => {
  document.dispatchEvent(new CustomEvent("stockSelected", { detail: d.ticker }));
});
```

## Scrollable Container

```css
.table-container {
  max-height: 600px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
}
table {
  border-collapse: collapse;
  width: 100%;
}
thead th {
  position: sticky;
  top: 0;
  background: #f8f9fa;
  z-index: 1;
}
```

## Key Tips

- Use `data-ticker` attributes on `<tr>` for easy DOM selection.
- For large datasets, virtual scrolling helps, but for ≤100 rows a simple `max-height` + `overflow-y: auto` is sufficient.
- Sticky `thead` keeps column headers visible during scroll.
- Always emit AND listen to the same custom event so chart ↔ table sync is bidirectional.
