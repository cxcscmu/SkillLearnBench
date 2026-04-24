---
name: Load and Validate Stock Data for Ticker Field Presence
description: Load CSV data and verify all stock entries contain the required `ticker` field with non-empty string values before using in selection matching logic
---

```javascript
// Load stock descriptions CSV
d3.csv('/root/output/data/stock-descriptions.csv').then(function(data) {
  // Validate that all entries have ticker field
  data.forEach((d, index) => {
    if (!d.ticker || d.ticker.trim() === '') {
      console.warn(`Row ${index} is missing ticker field:`, d);
    }
    
    // Trim whitespace from ticker and other fields
    d.ticker = d.ticker.trim();
    d.name = d.name.trim();
    d.sector = d.sector.trim();
    
    // Convert marketCap to number or null
    if (d.marketCap === '' || d.marketCap === null) {
      d.marketCap = null; // Identify ETFs
    } else {
      d.marketCap = parseFloat(d.marketCap);
    }
  });
  
  console.log('Loaded stock data:', data);
  
  // Log ETF vs non-ETF count for debugging
  const etfCount = data.filter(d => isETF(d)).length;
  const nonETFCount = data.length - etfCount;
  console.log(`Total stocks: ${data.length}, ETFs: ${etfCount}, Non-ETF: ${nonETFCount}`);
  
  // Proceed with visualization using validated data
  initializeVisualization(data);
});
```

Validation checklist:
- Confirm all 50 stocks have non-empty ticker values
- Trim whitespace from ticker, name, and sector fields
- Properly parse marketCap as number or null
- Log data to browser console to verify structure
- Check that ticker field matches between bubbles and table rows during matching