---
name: Implement Tooltip Display with Correct Positioning
description: Create and manage a D3 tooltip element that displays on hover for non-ETF stocks with dynamic positioning based on mouse movement
---

```javascript
// Create tooltip div in the DOM (do this once during initialization)
const tooltip = d3.select('body')
  .append('div')
  .attr('class', 'tooltip')
  .style('display', 'none')
  .style('position', 'absolute')
  .style('background-color', 'rgba(0, 0, 0, 0.8)')
  .style('color', 'white')
  .style('padding', '8px 12px')
  .style('border-radius', '4px')
  .style('font-size', '12px')
  .style('pointer-events', 'none')
  .style('z-index', '1000');

// Add event handlers to circle elements
circles
  .on('mouseover', function(event, d) {
    if (!isETF(d)) {
      tooltip.style('display', 'block')
        .html(`
          <strong>${d.ticker}</strong><br/>
          ${d.name}<br/>
          <em>${d.sector}</em>
        `);
    }
  })
  .on('mousemove', function(event, d) {
    if (!isETF(d)) {
      tooltip
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 28) + 'px');
    }
  })
  .on('mouseout', function(event, d) {
    if (!isETF(d)) {
      tooltip.style('display', 'none');
    }
  });
```

Important details:
- Use `event.pageX` and `event.pageY` to get mouse position relative to viewport
- Add offset (e.g., +10 and -28) to position tooltip near cursor without blocking it
- Verify HTML content includes all three fields: ticker, name, sector
- Test that tooltip only appears for non-ETF entries (where marketCap is not null)
- Add CSS styling in style.css for `.tooltip` class