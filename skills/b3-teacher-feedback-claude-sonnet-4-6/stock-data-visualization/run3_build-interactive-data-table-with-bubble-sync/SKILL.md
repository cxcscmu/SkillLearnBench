---
name: build-interactive-data-table-with-bubble-sync
description: Use when building an HTML data table that syncs highlighting with a D3 bubble chart on click interactions in both directions.
---

# Interactive Data Table Synced with D3 Bubble Chart

## Table Structure
```html
<div id="stock-table">
  <table>
    <thead>
      <tr>
        <th>Ticker Symbol</th>
        <th>Full Company Name</th>
        <th>Sector</th>
        <th>Market Cap</th>
      </tr>
    </thead>
    <tbody id="table-body"></tbody>
  </table>
</div>
```

## Market Cap Formatting
```javascript
function formatMarketCap(val) {
  if (!val || isNaN(val)) return 'N/A';
  const num = parseFloat(val);
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
  if (num >= 1e9)  return (num / 1e9).toFixed(2) + 'B';
  if (num >= 1e6)  return (num / 1e6).toFixed(2) + 'M';
  return num.toString();
}
```

## Table Population
```javascript
const tbody = d3.select('#table-body');
data.forEach(d => {
  tbody.append('tr')
    .attr('data-ticker', d.ticker)
    .html(`
      <td>${d.ticker}</td>
      <td>${d.name}</td>
      <td>${d.sector}</td>
      <td>${formatMarketCap(d.marketCapNum)}</td>
    `)
    .on('click', function() {
      // Highlight this row
      d3.selectAll('#table-body tr').classed('highlighted', false);
      d3.select(this).classed('highlighted', true);
      // Highlight corresponding bubble
      d3.selectAll('.bubble').classed('highlighted', false);
      d3.select(`.bubble[data-ticker="${d.ticker}"]`).classed('highlighted', true);
    });
});
```

## Bubble Click → Table Sync
```javascript
// On bubble click
.on('click', function(event, d) {
  // Clear previous highlights
  d3.selectAll('.bubble').classed('highlighted', false);
  d3.selectAll('#table-body tr').classed('highlighted', false);
  // Highlight this bubble
  d3.select(this).classed('highlighted', true);
  // Highlight table row and scroll into view
  const row = document.querySelector(`#table-body tr[data-ticker="${d.ticker}"]`);
  if (row) {
    row.classList.add('highlighted');
    row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
});
```

## Highlight CSS
```css
#table-body tr.highlighted {
  background-color: #ffe082;
  font-weight: bold;
}
.bubble.highlighted circle {
  stroke: #ff6f00;
  stroke-width: 3px;
}
```