---
name: Synchronize Bubble and Table Row Selection
description: Implement click handlers on both bubble chart and data table that maintain synchronized highlighting/selection state across both visualizations
---

```javascript
// Click handler for bubbles
circles.on('click', function(event, d) {
  if (isETF(d)) return; // Only allow interaction for non-ETF stocks
  
  // Remove previous selection from all circles and table rows
  circles.classed('selected', false);
  tableRows.classed('highlighted', false);
  
  // Add selection to clicked bubble
  d3.select(this).classed('selected', true);
  
  // Find and highlight matching row in table
  tableRows.each(function(rowData) {
    if (rowData.ticker === d.ticker) {
      d3.select(this).classed('highlighted', true);
    }
  });
});

// Click handler for table rows
tableRows.on('click', function(d) {
  // Remove previous selection from all rows and circles
  tableRows.classed('highlighted', false);
  circles.classed('selected', false);
  
  // Add highlight to clicked row
  d3.select(this).classed('highlighted', true);
  
  // Find and select matching bubble
  circles.each(function(bubbleData) {
    if (bubbleData.ticker === d.ticker) {
      d3.select(this).classed('selected', true);
    }
  });
});
```

Critical implementation details:
- Always remove previous `.highlighted` and `.selected` classes before applying new ones
- Use strict equality (`===`) when comparing ticker strings
- Ensure both `d.ticker` and `rowData.ticker` / `bubbleData.ticker` reference the same field
- Verify data types match (both should be strings)
- Add corresponding CSS classes in style.css with visible styling (e.g., stroke, background-color)
- Test in browser console to confirm event handlers fire and data matches correctly