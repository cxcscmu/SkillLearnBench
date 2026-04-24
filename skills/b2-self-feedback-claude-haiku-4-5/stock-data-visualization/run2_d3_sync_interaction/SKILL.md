---
name: run2_d3_sync_interaction
description: Two-way synchronized selection between D3 visualization and HTML table with tooltips and scroll management
---

# Synchronized D3 Visualization & Table Interaction

## Problem
Create bidirectional selection where:
1. Clicking a bubble highlights the corresponding table row
2. Clicking a table row highlights the corresponding bubble
3. Table scrolls to show selected row
4. Visual feedback is clear and consistent

## Solution Architecture

### 1. Unified Selection State
Use a single source of truth for selection:

```javascript
let selectedTicker = null;  // Currently selected ticker

function selectByTicker(ticker, source = 'unknown') {
  // Clear previous selection
  clearSelection();

  if (ticker) {
    selectedTicker = ticker;

    // Update bubble
    d3.selectAll('circle')
      .classed('selected', d => d.ticker === ticker);

    // Update table row
    d3.selectAll('table tbody tr')
      .classed('highlighted', d => {
        const rowTicker = d3.select(d).attr('data-ticker');
        return rowTicker === ticker;
      });

    // Scroll row into view if source is not table
    if (source !== 'table') {
      scrollTableToTicker(ticker);
    }
  }
}

function clearSelection() {
  selectedTicker = null;
  d3.selectAll('circle').classed('selected', false);
  d3.selectAll('table tbody tr').classed('highlighted', false);
}
```

### 2. Bubble Click Handler
```javascript
circles.on('click', function(event, d) {
  event.stopPropagation();

  // Toggle selection
  if (selectedTicker === d.ticker) {
    clearSelection();
  } else {
    selectByTicker(d.ticker, 'bubble');
  }
});
```

### 3. Table Row Click Handler
```javascript
d3.selectAll('table tbody tr').on('click', function() {
  const ticker = d3.select(this).attr('data-ticker');

  if (selectedTicker === ticker) {
    clearSelection();
  } else {
    selectByTicker(ticker, 'table');
  }
});
```

### 4. Smart Table Scrolling
Keep selected row visible:

```javascript
function scrollTableToTicker(ticker) {
  const container = d3.select('.table-section');
  const row = container.select(`tr[data-ticker="${ticker}"]`);

  if (row.empty()) return;

  const rowElement = row.node();
  const containerElement = container.node();

  // Get positions
  const rowTop = rowElement.offsetTop;
  const rowHeight = rowElement.offsetHeight;
  const containerScrollTop = containerElement.scrollTop;
  const containerHeight = containerElement.clientHeight;

  // Scroll if row is not visible
  if (rowTop < containerScrollTop) {
    // Scroll to top of row with margin
    containerElement.scrollTop = Math.max(0, rowTop - 50);
  } else if (rowTop + rowHeight > containerScrollTop + containerHeight) {
    // Scroll to bottom of row with margin
    containerElement.scrollTop = rowTop + rowHeight - containerHeight + 50;
  }
}
```

### 5. Hover Effects (Lighter Touch)
Distinguish between hover and selection:

```javascript
// Hover: light effect
circles
  .on('mouseover', function(event, d) {
    if (d.marketCap) {  // Only for complete data
      showTooltip(event, d);
    }
    // Don't change styling on hover - selection is more important
  })
  .on('mouseout', function() {
    hideTooltip();
  });

// Table hover
d3.selectAll('table tbody tr')
  .on('mouseover', function() {
    d3.select(this).style('background-color', '#f9f9f9');
  })
  .on('mouseout', function() {
    // Restore selection state
    const ticker = d3.select(this).attr('data-ticker');
    const bgColor = selectedTicker === ticker ? '#ffe6e6' : '';
    d3.select(this).style('background-color', bgColor);
  });
```

## Tooltip Implementation

### Tooltip HTML Structure
```html
<div id="tooltip" style="
  position: absolute;
  display: none;
  background: rgba(0,0,0,0.85);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  z-index: 1000;
  pointer-events: none;
"></div>
```

### Tooltip Display with Smart Positioning
```javascript
function showTooltip(event, d) {
  const tooltip = d3.select('#tooltip');

  // Build content
  const html = `
    <strong>${d.ticker}</strong><br/>
    ${d.name}<br/>
    <small>${d.sector}</small>
  `;

  tooltip.html(html);

  // Calculate position
  let x = event.pageX + 10;
  let y = event.pageY - 10;

  // Check bounds and adjust
  const tooltipNode = tooltip.node();
  const tooltipWidth = tooltipNode.offsetWidth;
  const tooltipHeight = tooltipNode.offsetHeight;

  if (x + tooltipWidth > window.innerWidth - 10) {
    x = event.pageX - tooltipWidth - 10;
  }
  if (y + tooltipHeight > window.innerHeight - 10) {
    y = event.pageY - tooltipHeight - 10;
  }

  tooltip
    .style('left', x + 'px')
    .style('top', y + 'px')
    .style('display', 'block');
}

function hideTooltip() {
  d3.select('#tooltip').style('display', 'none');
}
```

## Data Attributes for Linking

### HTML Setup
Ensure both circle and table row can be linked by ticker:

```html
<!-- Table row -->
<tr data-ticker="AAPL" data-id="AAPL">
  <td>AAPL</td>
  <td>Apple Inc.</td>
  <td>Information Technology</td>
  <td>2.68T</td>
</tr>

<!-- Circle in D3 -->
circles
  .attr('data-ticker', d => d.ticker)
  .attr('data-id', d => d.ticker);
```

## CSS for Visual States

```css
/* Bubble selection */
circle.selected {
  stroke: #ff4444;
  stroke-width: 3;
  filter: drop-shadow(0 0 6px rgba(255, 68, 68, 0.5));
}

circle:hover {
  opacity: 0.85;
}

/* Table row selection */
table tbody tr.highlighted {
  background-color: #ffe6e6;
  font-weight: 500;
}

table tbody tr:hover {
  background-color: #f9f9f9;
}

table tbody tr.highlighted:hover {
  background-color: #ffd4d4;
}

/* Transitions for smooth feedback */
circle,
table tbody tr {
  transition: stroke 150ms, background-color 150ms, opacity 150ms;
}
```

## Click Outside to Deselect
```javascript
d3.select(document).on('click', function() {
  // Only clear if clicking on SVG background (not element)
  const target = d3.event.target;
  if (target.tagName === 'svg' || target.id === 'chart') {
    clearSelection();
  }
});
```

## Advanced: Keyboard Navigation
```javascript
d3.select(window).on('keydown', function() {
  if (event.key === 'Escape') {
    clearSelection();
  }
  // Arrow keys to navigate selected items
  if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
    const current = document.querySelector('table tbody tr.highlighted');
    if (current) {
      const next = event.key === 'ArrowDown'
        ? current.nextElementSibling
        : current.previousElementSibling;
      if (next) {
        const ticker = next.getAttribute('data-ticker');
        selectByTicker(ticker, 'keyboard');
      }
    }
  }
});
```

## Testing Synchronization
Verify both directions work:

```javascript
// Test 1: Select by ticker
selectByTicker('AAPL', 'test');
console.assert(
  d3.selectAll('circle.selected').size() === 1,
  'Bubble not selected'
);
console.assert(
  d3.selectAll('table tr.highlighted').size() === 1,
  'Table row not selected'
);

// Test 2: Deselection
clearSelection();
console.assert(
  d3.selectAll('circle.selected').size() === 0,
  'Bubble not deselected'
);
console.assert(
  d3.selectAll('table tr.highlighted').size() === 0,
  'Table row not deselected'
);
```
