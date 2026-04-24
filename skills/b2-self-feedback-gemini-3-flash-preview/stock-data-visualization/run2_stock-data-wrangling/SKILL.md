---
name: run2_stock-data-wrangling
description: Robust data cleaning and formatting for financial datasets in D3.js.
---

# Stock Data Wrangling

Ensuring data consistency between individual files and the summary CSV.

## Robust ETF Detection

ETFs often have missing `sector` and `marketCap`. Explicitly label them to apply specific logic (uniform sizing, no tooltip).

```javascript
const processed = rawData.map(d => {
    const marketCap = d.marketCap ? parseFloat(d.marketCap) : null;
    const isETF = isNaN(marketCap) || !marketCap || d.sector === "" || d.sector === "ETF";
    return {
        ...d,
        marketCap,
        isETF,
        sector: isETF ? "ETF" : d.sector
    };
});
```

## Precise Market Cap Formatting

Formatting numbers to "1.64T" or "150B" using fixed precision.

```javascript
function formatCurrency(val) {
    if (!val) return "N/A";
    const trillion = 1e12;
    const billion = 1e9;
    const million = 1e6;
    
    if (val >= trillion) return (val / trillion).toFixed(2) + "T";
    if (val >= billion) return (val / billion).toFixed(2) + "B";
    if (val >= million) return (val / million).toFixed(2) + "M";
    return val.toLocaleString();
}
```
