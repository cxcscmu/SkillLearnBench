---
name: run2_csv_robust_loading
description: Robust CSV loading and type coercion patterns for D3.js applications with multiple data sources
---

# Robust CSV Loading for D3.js

## Overview
Practical patterns for loading CSV data with proper type coercion, null handling, and batch operations for multi-file scenarios.

## Single CSV with Type Coercion

### Pattern: Inline Coercion
```javascript
d3.csv("data/stocks.csv").then(rawData => {
  const stocks = rawData.map(d => ({
    // String fields - trim whitespace
    ticker: d.ticker.trim(),
    name: d['full name'].trim(),
    sector: d.sector.trim(),
    country: d.country?.trim() || null,
    website: d.website?.trim() || null,

    // Numeric fields - parse and handle nulls
    marketCap: d.marketCap ? parseFloat(d.marketCap) : null,
    returnOnEquity: d.returnOnEquity ? parseFloat(d.returnOnEquity) : null,
    revenuePerShare: d.revenuePerShare ? parseFloat(d.revenuePerShare) : null,
    fullTimeEmployees: d.fullTimeEmployees ? parseInt(d.fullTimeEmployees) : null,

    // Date fields (if applicable)
    // dateCreated: d.dateCreated ? new Date(d.dateCreated) : null
  }));

  // Validate: Log rows with missing critical fields
  const incomplete = stocks.filter(s => !s.ticker || !s.sector);
  console.log(`Loaded ${stocks.length} stocks (${incomplete.length} incomplete)`);

  return stocks;
});
```

### Separate Coercion Function
For reusability and clarity:

```javascript
function coerceStockRow(d) {
  return {
    ticker: d.ticker.trim(),
    name: d['full name'].trim(),
    sector: d.sector.trim(),
    marketCap: d.marketCap ? parseFloat(d.marketCap) : null,
    country: d.country?.trim() || null,
    website: d.website?.trim() || null,
    returnOnEquity: d.returnOnEquity ? parseFloat(d.returnOnEquity) : null,
    revenuePerShare: d.revenuePerShare ? parseFloat(d.revenuePerShare) : null,
    beta: d.beta ? parseFloat(d.beta) : null
  };
}

d3.csv("data/stocks.csv")
  .then(data => data.map(coerceStockRow))
  .then(stocks => visualize(stocks));
```

## Multiple CSV Files (Batch Loading)

### Pattern: Promise.all for Multiple Files
```javascript
async function loadAllData() {
  const stocks = await d3.csv("data/stocks.csv")
    .then(data => data.map(coerceStockRow));

  const sectors = await d3.csv("data/sectors.csv")
    .then(data => data.map(d => ({
      name: d.sector,
      description: d.description
    })));

  return { stocks, sectors };
}

loadAllData().then(data => visualize(data));
```

### Pattern: Batch Loading Multiple Stock Files
For loading price history for each stock:

```javascript
async function loadStockPrices(tickers) {
  const promises = tickers.map(ticker =>
    d3.csv(`data/indiv-stock/${ticker}.csv`)
      .then(data => ({
        ticker,
        prices: data.map(d => ({
          date: new Date(d.Date),
          close: parseFloat(d.Close),
          volume: parseInt(d.Volume),
          high: parseFloat(d.High),
          low: parseFloat(d.Low)
        })).sort((a, b) => a.date - b.date)
      }))
      .catch(err => {
        console.warn(`Failed to load prices for ${ticker}:`, err);
        return { ticker, prices: [] };
      })
  );

  const allPrices = await Promise.all(promises);
  return Object.fromEntries(
    allPrices.map(p => [p.ticker, p.prices])
  );
}

// Usage
const stocks = await d3.csv("data/stocks.csv");
const prices = await loadStockPrices(stocks.map(s => s.ticker));
// prices now is: { 'AAPL': [...], 'MSFT': [...], ... }
```

## Handling Edge Cases

### Empty Strings and Whitespace
```javascript
function safeString(value, defaultValue = null) {
  if (!value || typeof value !== 'string') return defaultValue;
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : defaultValue;
}

// Usage
country: safeString(d.country),
website: safeString(d.website, "Unknown")
```

### Numeric Edge Cases
```javascript
function safeNumber(value, defaultValue = null) {
  if (value === null || value === undefined || value === '') {
    return defaultValue;
  }
  const num = parseFloat(value);
  return isNaN(num) ? defaultValue : num;
}

// Usage
marketCap: safeNumber(d.marketCap),
beta: safeNumber(d.beta, 1)  // Default beta to 1 if missing
```

### Field Name Mapping
CSV files may have inconsistent column names:

```javascript
// Define field mapping
const fieldMap = {
  'full name': 'name',
  'Market Cap': 'marketCap',
  'ROE': 'returnOnEquity'
};

function mapFields(row) {
  const mapped = {};
  for (let [csvKey, appKey] of Object.entries(fieldMap)) {
    mapped[appKey] = row[csvKey];
  }
  return mapped;
}
```

## Error Handling

### Try-Catch Pattern
```javascript
async function loadData() {
  try {
    const stocks = await d3.csv("data/stocks.csv");

    if (!stocks || stocks.length === 0) {
      throw new Error("CSV is empty");
    }

    return stocks.map(coerceStockRow);
  } catch (error) {
    console.error("Failed to load CSV:", error);
    return [];  // Return empty array as fallback
  }
}
```

### Progress Tracking for Large Loads
```javascript
async function loadWithProgress(files) {
  const total = files.length;
  let loaded = 0;

  const results = await Promise.all(
    files.map(file =>
      d3.csv(file)
        .then(data => {
          loaded++;
          console.log(`Loaded ${loaded}/${total}`);
          return data;
        })
    )
  );

  return results;
}
```

## Performance Tips

1. **Defer parsing**: Only parse fields you need
```javascript
// ✓ Good - parse only what's used
const stocks = data.map(d => ({
  ticker: d.ticker,
  marketCap: parseFloat(d.marketCap)
}));

// ✗ Avoid - parse everything
const stocks = data.map(d => coerceAllFields(d));
```

2. **Cache parsed data**: Store result of d3.csv()
```javascript
let cachedStocks = null;

function getStocks() {
  if (cachedStocks) return Promise.resolve(cachedStocks);

  return d3.csv("data/stocks.csv")
    .then(data => {
      cachedStocks = data.map(coerceStockRow);
      return cachedStocks;
    });
}
```

3. **Stream large files**: Load in chunks for 10k+ rows
```javascript
async function* readCSVChunks(url, chunkSize = 100) {
  const data = await d3.csv(url);
  for (let i = 0; i < data.length; i += chunkSize) {
    yield data.slice(i, i + chunkSize).map(coerceStockRow);
  }
}
```

## Testing Coercion Functions
```javascript
// Unit test example
const testRow = {
  ticker: "  AAPL  ",
  'full name': "Apple Inc.",
  marketCap: "2676055080960",
  country: ""
};

const coerced = coerceStockRow(testRow);
console.assert(coerced.ticker === "AAPL", "Trim failed");
console.assert(coerced.marketCap === 2676055080960, "Parse failed");
console.assert(coerced.country === null, "Empty string handling failed");
```
