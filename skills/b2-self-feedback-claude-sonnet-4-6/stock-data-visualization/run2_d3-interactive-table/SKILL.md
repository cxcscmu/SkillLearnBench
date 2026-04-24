---
name: run2_d3-interactive-table
description: Building a scrollable D3.js HTML table linked to a bubble chart with bidirectional click-highlight, correct scrollIntoView for overflow containers, and sector color badges.
---

# D3.js v6 Interactive Table (Improved)

## HTML Structure
```html
<div id="table-panel">
    <h2>All Stocks</h2>
    <div id="table-container">  <!-- scrollable wrapper -->
        <table id="stock-table">
            <thead><tr>
                <th>Ticker</th><th>Full Company Name</th>
                <th>Sector</th><th>Market Cap</th>
            </tr></thead>
            <tbody id="table-body"></tbody>
        </table>
    </div>
</div>
```

## CSS — Sticky Header + Scrollable Body
```css
#table-container {
    flex: 1;
    overflow-y: auto;   /* Scroll within panel */
}
#stock-table thead {
    position: sticky;
    top: 0;
    z-index: 2;
    background: #f0f2f5;
}
```

## Building Rows with D3
```javascript
const sorted = [...data].sort((a, b) => a.ticker.localeCompare(b.ticker));
const rows = d3.select('#table-body')
    .selectAll('tr')
    .data(sorted, d => d.ticker)
    .join('tr')
    .attr('data-ticker', d => d.ticker);

rows.each(function(d) {
    const tr = d3.select(this);
    tr.append('td').text(d.ticker);
    tr.append('td').text(d['full name']);
    // Sector badge with matching bubble color
    tr.append('td').append('span')
        .attr('class', 'sector-badge')
        .style('background-color', getSectorColor(d.sector))
        .text(d.sector);
    tr.append('td').text(formatMarketCap(d.marketCapNum));
});
```

## Bidirectional Selection
```javascript
let currentSelected = null;

function handleSelection(ticker) {
    if (currentSelected === ticker) {
        // Toggle off
        currentSelected = null;
        d3.selectAll('circle.bubble').classed('highlighted', false);
        d3.selectAll('#table-body tr').classed('highlighted', false);
    } else {
        currentSelected = ticker;
        d3.selectAll('circle.bubble').classed('highlighted', d => d.ticker === ticker);
        d3.selectAll('#table-body tr').classed('highlighted', d => d.ticker === ticker);
        scrollTableToTicker(ticker);
    }
}

// Wire up table rows and circles to the same handler
rows.on('click', (event, d) => handleSelection(d.ticker));
circles.on('click', (event, d) => handleSelection(d.ticker));
```

## Correct scrollIntoView for Nested Overflow Container
IMPORTANT: `scrollIntoView()` scrolls the nearest scrollable ancestor.
Since `#table-container` is the scrollable container, this just works:
```javascript
function scrollTableToTicker(ticker) {
    const row = document.querySelector(`#table-body tr[data-ticker="${ticker}"]`);
    if (row) {
        row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}
```

`block: 'nearest'` is key — it scrolls only if the element is out of view,
and scrolls within the nearest scrollable ancestor (`#table-container`).

## CSS for Highlight States
```css
#stock-table tbody tr.highlighted {
    background-color: #fff3cd;
    font-weight: 600;
}

circle.bubble.highlighted {
    stroke: #222;
    stroke-width: 3px;
    filter: drop-shadow(0 0 5px rgba(0,0,0,0.5));
}

.sector-badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 10px;
    font-size: 0.75rem;
    color: white;
}
```
