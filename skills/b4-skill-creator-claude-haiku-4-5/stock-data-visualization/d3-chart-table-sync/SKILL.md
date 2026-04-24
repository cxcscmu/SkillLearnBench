---
name: d3-chart-table-sync
description: Synchronize interactions between D3 visualizations and HTML tables, enabling click-to-highlight and hover effects across both elements. Use this skill when you need chart and table elements to stay in sync - clicking a bubble highlights its table row, clicking a row highlights the bubble, and/or hovering shows related data across both. Essential for exploratory dashboards where users need to see data from multiple perspectives simultaneously.
---

# D3 Chart-Table Synchronization

This skill covers linking D3 visualizations with HTML data tables for synchronized interactions.

## Architecture

The key is using a **shared data key** (usually unique identifier like ticker symbol) to link chart elements and table rows:

```javascript
// In both chart and table, use consistent key
const KEY = d => d.ticker;
```

## Basic Selection Linking

```javascript
// When user clicks a bubble
circles.on("click", function(event, d) {
  const key = d.ticker;

  // Highlight bubble
  circles.classed("selected", e => KEY(e) === key);

  // Highlight table row
  tableRows.classed("selected", row => KEY(row) === key);
});

// When user clicks table row
tableRows.on("click", function(event, rowData) {
  const key = rowData.ticker;

  // Highlight table row
  tableRows.classed("selected", row => KEY(row) === key);

  // Highlight bubble
  circles.classed("selected", d => KEY(d) === key);
});
```

**CSS for highlighting:**
```css
circle.selected,
tr.selected {
  stroke: #000;
  stroke-width: 2;
}

tr.selected {
  background-color: #fff3cd;
}
```

## Click-to-Scroll: Table Follows Selection

When user clicks a bubble, scroll the table to show that row:

```javascript
circles.on("click", function(event, d) {
  const key = d.ticker;

  // ... highlighting code above ...

  // Find and scroll to table row
  const selectedRow = document.querySelector(`tr[data-ticker="${key}"]`);
  if (selectedRow) {
    selectedRow.scrollIntoView({behavior: "smooth", block: "center"});
  }
});
```

**In HTML table, add data attribute:**
```html
<tr data-ticker="AAPL">
  <td>AAPL</td>
  <td>Apple Inc.</td>
  ...
</tr>
```

## Hover Coordination

Lighter interaction - highlight without full selection:

```javascript
circles.on("mouseover", function(event, d) {
  const key = KEY(d);
  circles.classed("hovered", e => KEY(e) === key);
  tableRows.classed("hovered", row => KEY(row) === key);
})
.on("mouseout", function() {
  circles.classed("hovered", false);
  tableRows.classed("hovered", false);
});

tableRows.on("mouseover", function(event, rowData) {
  const key = KEY(rowData);
  tableRows.classed("hovered", row => KEY(row) === key);
  circles.classed("hovered", d => KEY(d) === key);
})
.on("mouseout", function() {
  tableRows.classed("hovered", false);
  circles.classed("hovered", false);
});
```

**CSS for hover:**
```css
circle.hovered {
  stroke: #333;
  stroke-width: 1;
  opacity: 0.8;
}

tr.hovered {
  background-color: #f0f0f0;
}
```

## D3 Data Binding Pattern

Ensure table rows and bubbles reference same data array:

```javascript
// Load data once
d3.csv("data/stocks.csv").then(rawData => {
  const data = processData(rawData);

  // Chart uses this data
  drawChart(data);

  // Table uses this data
  drawTable(data);
});

function drawChart(data) {
  const circles = svg.selectAll("circle")
    .data(data, d => d.ticker) // Key function
    .enter()
    .append("circle");
  // ... rest of chart code
}

function drawTable(data) {
  const rows = tbody.selectAll("tr")
    .data(data, d => d.ticker) // Same key function!
    .enter()
    .append("tr");
  // ... rest of table code
}
```

**Critical:** Use identical key functions in both `data()` calls.

## Pattern: Bilateral Selection State

Maintain a shared state object to prevent infinite loops:

```javascript
let selectedTicker = null;

function selectByTicker(ticker) {
  selectedTicker = ticker;

  // Update both chart and table
  circles.classed("selected", d => d.ticker === ticker);
  tableRows.classed("selected", row => row.ticker === ticker);
}

circles.on("click", function(event, d) {
  selectByTicker(d.ticker);
});

tableRows.on("click", function(event, rowData) {
  selectByTicker(rowData.ticker);
});
```

## Handling Dynamic Updates

If data changes:

```javascript
function updateData(newData) {
  // Update chart circles
  circles = svg.selectAll("circle").data(newData, d => d.ticker);
  circles.exit().remove();
  // ... handle update and enter selections

  // Update table rows
  rows = tbody.selectAll("tr").data(newData, d => d.ticker);
  rows.exit().remove();
  // ... handle update and enter selections

  // Reattach event handlers
  attachClickHandlers();
}
```

## Testing Checklist

- [ ] Click bubble → row highlights and table scrolls
- [ ] Click row → bubble highlights
- [ ] Click different bubble → previous highlights clear
- [ ] Hover bubble → row highlights
- [ ] Hover row → bubble highlights
- [ ] Scroll table → interactions still work
- [ ] Multiple rapid clicks don't break state
- [ ] Data keys are consistent (no duplicates)
- [ ] CSS classes applied/removed correctly
