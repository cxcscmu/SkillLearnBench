---
name: run2_d3-data-load
description: Optimized loading and pre-processing of CSV data for D3.js.
---
# Advanced Data Loading in D3.js

For larger datasets or complex transformations:
```javascript
d3.csv(url, d => ({
    ...d,
    marketCap: +d.marketCap || 0,
    r: Math.sqrt(+d.marketCap || 1e11) / 1e5 // Pre-calculate radii
})).then(data => { ... });
```
