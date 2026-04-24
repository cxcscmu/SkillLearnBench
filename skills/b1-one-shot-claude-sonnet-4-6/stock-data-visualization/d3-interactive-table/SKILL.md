---
name: d3-interactive-table
description: Build a sortable, highlightable HTML data table linked to a D3 chart so clicking a chart element highlights the matching table row and vice versa.
---

# D3 v6 Interactive Table with Chart Cross-Linking

## Overview

A pure-HTML table built alongside a D3 chart where selections are synchronized: clicking a bubble highlights a table row, clicking a table row highlights the bubble.

## Table Construction Pattern

```javascript
function buildTable(data, containerId) {
    const container = d3.select(containerId);
    const table = container.append('table').attr('class', 'data-table');

    // Header
    const thead = table.append('thead');
    thead.append('tr').selectAll('th')
        .data(['Ticker', 'Full Name', 'Sector', 'Market Cap'])
        .join('th')
        .text(d => d);

    // Body
    const tbody = table.append('tbody');
    const rows = tbody.selectAll('tr')
        .data(data)
        .join('tr')
        .attr('data-ticker', d => d.ticker)  // stable identifier
        .on('click', function(event, d) {
            selectItem(d.ticker);
        });

    rows.selectAll('td')
        .data(d => [d.ticker, d.name, d.sector, formatMarketCap(d.marketCap)])
        .join('td')
        .text(v => v);
}
```

## Cross-Linking Pattern

Use a shared `selectItem(ticker)` function that updates both the chart and table:

```javascript
let selectedTicker = null;

function selectItem(ticker) {
    selectedTicker = ticker;

    // Update table rows
    d3.selectAll('tr[data-ticker]')
        .classed('selected', d => d.ticker === ticker);

    // Update chart circles
    d3.selectAll('circle.bubble')
        .classed('selected', d => d.ticker === ticker);

    // Scroll to highlighted row
    const row = document.querySelector(`tr[data-ticker="${ticker}"]`);
    if (row) row.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}
```

## CSS for Highlighted State

```css
/* Table row highlight */
tr[data-ticker]:hover {
    background: #f0f4ff;
    cursor: pointer;
}
tr[data-ticker].selected {
    background: #dce8ff;
    font-weight: 600;
}

/* Bubble highlight */
circle.bubble.selected {
    stroke: #1a1a2e;
    stroke-width: 3px;
    filter: drop-shadow(0 0 4px rgba(0,0,0,0.5));
}
```

## Market Cap Formatting

```javascript
function formatMarketCap(val) {
    if (!val || isNaN(+val)) return '—';
    const v = +val;
    if (v >= 1e12) return (v / 1e12).toFixed(2) + 'T';
    if (v >= 1e9)  return (v / 1e9).toFixed(2) + 'B';
    if (v >= 1e6)  return (v / 1e6).toFixed(2) + 'M';
    return v.toFixed(0);
}
```

## Scrollable Table Container

For large datasets, constrain table height and enable overflow scrolling:

```css
.table-container {
    max-height: 600px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 6px;
}

/* Sticky header */
thead th {
    position: sticky;
    top: 0;
    background: #f8f9fa;
    z-index: 10;
}
```

## Click Toggle (Deselect on Second Click)

```javascript
.on('click', function(event, d) {
    if (selectedTicker === d.ticker) {
        clearSelection();
    } else {
        selectItem(d.ticker);
    }
})

function clearSelection() {
    selectedTicker = null;
    d3.selectAll('.selected').classed('selected', false);
}
```
