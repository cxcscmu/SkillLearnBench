---
name: stock-data-processing
description: Load, parse, and transform stock market data from CSV files for D3 visualization. Use this skill when working with financial CSV data, handling missing values (ETFs often lack market cap/country data), formatting market capitalization as human-readable strings (1.64T), and preparing data for both visualization and table display. Essential for stock dashboards, portfolio analytics, and financial data pipelines.
---

# Stock Data Processing for D3 Visualization

This skill covers loading CSV data and preparing it for stock market visualizations.

## CSV Data Structure

Typical stock-descriptions CSV has columns:
```
Ticker,Name,Sector,Market Cap (Billions),Country,Website
AAPL,Apple Inc.,Technology,2800,USA,apple.com
ETF,ETF Name,ETF Sector,,,
```

**Important:** ETF rows have empty marketCap, Country, Website fields.

## Loading CSV with d3-dsv

D3 v6 includes CSV parsing via `d3.csv()`:

```javascript
d3.csv("data/stock-descriptions.csv").then(rawData => {
  const data = rawData.map(d => ({
    ticker: d.Ticker,
    name: d.Name,
    sector: d.Sector || "Unknown",
    marketCapBillions: d["Market Cap (Billions)"] ? +d["Market Cap (Billions)"] : null,
    country: d.Country || null,
    website: d.Website || null,
    isETF: !d["Market Cap (Billions)"] // Detect ETFs by missing market cap
  }));

  // Continue with data
});
```

## Formatting Market Cap

Convert billions to human-readable format (1.64T, 350B, etc.):

```javascript
function formatMarketCap(billionValue) {
  if (!billionValue) return "N/A";

  const value = billionValue;
  if (value >= 1000) {
    return (value / 1000).toFixed(2) + "T";
  } else if (value >= 1) {
    return value.toFixed(2) + "B";
  } else {
    return (value * 1000).toFixed(0) + "M";
  }
}
```

Example: `formatMarketCap(2800)` → `"2.80T"`

## Handling Individual Stock Data

If loading price history from separate files in `indiv-stock/`:

```javascript
async function loadStockPrices(ticker) {
  try {
    const prices = await d3.csv(`data/indiv-stock/${ticker}.csv`);
    return prices.map(d => ({
      date: new Date(d.Date),
      close: +d.Close,
      volume: +d.Volume
    }));
  } catch {
    return null; // File doesn't exist
  }
}
```

## Data Validation

```javascript
function validateStockData(data) {
  const issues = [];

  // Check required fields
  if (!data.ticker || !data.name || !data.sector) {
    issues.push("Missing required fields");
  }

  // Check numeric validity
  if (data.marketCapBillions && data.marketCapBillions <= 0) {
    issues.push("Invalid market cap (negative or zero)");
  }

  // Check for duplicates
  // (Implement if using data from multiple sources)

  return issues.length === 0;
}
```

## Grouping by Sector

```javascript
const sectorGroups = d3.group(data, d => d.sector);
const sectors = Array.from(sectorGroups.keys()).sort();
```

Or for iteration:
```javascript
const sectorCounts = d3.rollup(
  data,
  v => v.length,
  d => d.sector
);
```

## Handling Edge Cases

1. **Missing Market Cap (ETFs):**
   - Don't exclude from visualization
   - Use default/uniform sizing
   - Skip tooltips or mark as "N/A"
   - Don't show in sorted market cap rankings

2. **Duplicate Tickers:**
   - Keep first occurrence
   - Log warning for duplicates

3. **Special Characters:**
   - Tickers safe for CSS class names via: `ticker.toLowerCase().replace(/[^a-z0-9]/g, '')`
   - Names safe for HTML via: `d3.html` or escaped strings

4. **Missing Sector:**
   - Default to "Other"
   - Ensure sector exists in color scale domain

## Data Pipeline Example

```javascript
async function loadStockData() {
  const raw = await d3.csv("data/stock-descriptions.csv");

  const data = raw
    .map(d => ({
      ticker: d.Ticker.trim(),
      name: d.Name.trim(),
      sector: d.Sector.trim() || "Other",
      marketCapBillions: d["Market Cap (Billions)"] ? +d["Market Cap (Billions)"] : null,
      country: d.Country.trim() || null,
      website: d.Website.trim() || null,
      isETF: !d["Market Cap (Billions)"]
    }))
    .filter(d => validateStockData(d));

  return data;
}
```

## Testing Checklist

- [ ] CSV loads without errors
- [ ] All required fields present and non-null
- [ ] Market cap formatting produces correct units (T/B/M)
- [ ] ETFs correctly identified (no market cap = ETF)
- [ ] Sector grouping works correctly
- [ ] No duplicate tickers
- [ ] Numeric conversions work (no NaN values)
