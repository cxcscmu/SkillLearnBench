---
name: Identify ETF Entries for Conditional Rendering
description: Create a utility function to reliably detect ETF entries by checking for null/undefined marketCap values, enabling conditional tooltip display and styling
---

```javascript
/**
 * Determines if a stock entry is an ETF (Exchange-Traded Fund)
 * ETFs lack marketCap, country, and website data in the dataset
 * @param {Object} d - The stock data object
 * @returns {Boolean} true if the entry is an ETF, false otherwise
 */
function isETF(d) {
  return d.marketCap === null || d.marketCap === undefined || d.marketCap === '';
}

// Usage in D3 selections:
// - Only show tooltips for non-ETF entries
// - Apply uniform sizing to ETF bubbles
// - Filter conditional event handlers based on ETF status

// Example in bubble creation:
circles
  .on('mouseover', function(event, d) {
    if (!isETF(d)) {
      // Show tooltip only for non-ETF stocks
      tooltip.style('display', 'block');
    }
  })
  .on('mouseout', function(event, d) {
    if (!isETF(d)) {
      tooltip.style('display', 'none');
    }
  });
```

Key checks:
- Validate that `d.marketCap` is truly null/undefined before assuming ETF status
- Use this function consistently across all tooltip and event handler logic
- Test with sample data to confirm ETF entries have no marketCap value