---
name: csv-data-handling
description: Loading and parsing CSV files with D3.js, data transformation, and handling missing values
---

# CSV Data Handling with D3.js

## Overview
D3.js provides built-in CSV parsing. Understanding type coercion and data transformation is essential for visualization.

## 1. Loading CSV Files

### Basic CSV Load
```javascript
d3.csv("data.csv").then(data => {
  console.log(data);  // Array of objects
  // [{ key1: value1, key2: value2 }, ...]
});
```

### With Error Handling
```javascript
d3.csv("data.csv")
  .then(data => {
    console.log("Data loaded:", data.length, "rows");
    processData(data);
  })
  .catch(error => {
    console.error("Error loading CSV:", error);
  });
```

### With Type Accessor
D3 can automatically convert types:

```javascript
d3.csv("data.csv", row => {
  return {
    ticker: row.ticker,
    marketCap: +row.marketCap,  // convert to number
    sector: row.sector,
    value: parseFloat(row.value)
  };
}).then(processData);
```

## 2. Data Transformation

### Parsing Numeric Values
```javascript
data.forEach(d => {
  d.marketCap = +d.marketCap;  // unary + operator
  d.employees = parseInt(d.employees, 10);
  d.yield = parseFloat(d.yield);
});
```

### Handling Missing Values
```javascript
data = data.filter(d => {
  // Keep only rows with required data
  return d.marketCap && d.sector;
});

// Or replace missing with default
data.forEach(d => {
  d.marketCap = d.marketCap || 0;
  d.website = d.website || "N/A";
});
```

### Filtering and Sorting
```javascript
// Filter by sector
const tech = data.filter(d => d.sector === "Information Technology");

// Sort by market cap
data.sort((a, b) => b.marketCap - a.marketCap);

// Top 50 by market cap
const top50 = data.sort((a, b) => b.marketCap - a.marketCap).slice(0, 50);
```

## 3. Loading Multiple Files

### Sequential Loading
```javascript
Promise.all([
  d3.csv("companies.csv"),
  d3.csv("prices.csv")
]).then(([companies, prices]) => {
  // Both loaded
  const merged = mergeData(companies, prices);
  visualize(merged);
});
```

### Loading Individual Stock Data
```javascript
// Load main data
d3.csv("data/stock-descriptions.csv").then(stocks => {
  // For each stock, load price history
  const pricePromises = stocks.map(stock =>
    d3.csv(`data/indiv-stock/${stock.ticker}.csv`)
      .then(prices => ({
        ticker: stock.ticker,
        prices: prices
      }))
  );

  return Promise.all(pricePromises);
}).then(allData => {
  // Process combined data
  visualize(allData);
});
```

## 4. Aggregation & Grouping

### Group by Category
```javascript
const bySetor = d3.group(data, d => d.sector);
// Map { sector: [stocks...], ... }

// Or convert to array
const sectorGroups = Array.from(bySetor, ([sector, stocks]) => ({
  sector,
  count: stocks.length,
  totalCap: d3.sum(stocks, d => d.marketCap)
}));
```

### Nesting (Hierarchical Grouping)
```javascript
const nested = d3.nest()
  .key(d => d.sector)
  .entries(data);

// Returns: [{ key: "sector1", values: [stocks...] }, ...]
```

## 5. Formatting Numbers for Display

### Format for Visualization
```javascript
// Market cap formatter
const capFormatter = d3.format(".2s");  // "1.6T"
const capFormat = (value) => {
  const sizes = ['', 'K', 'M', 'B', 'T'];
  let sizeIndex = 0;
  let num = value;
  while (num >= 1000 && sizeIndex < sizes.length - 1) {
    num /= 1000;
    sizeIndex++;
  }
  return num.toFixed(2) + sizes[sizeIndex];
};

console.log(capFormat(1641026945024));  // "1.64T"
```

### Format Percentages
```javascript
const percentFormatter = d3.format(".2%");
console.log(percentFormatter(0.28806));  // "28.81%"
```

## 6. Data Validation

### Check for Required Fields
```javascript
function validateData(data) {
  return data.every(d => {
    return d.ticker &&
           d.sector &&
           d.marketCap !== undefined;
  });
}

if (!validateData(data)) {
  console.error("Invalid data structure");
}
```

## 7. Copying Data for Performance

### Deep Copy to Avoid Mutations
```javascript
// Shallow copy (references still point to original objects)
const copy1 = [...data];
const copy2 = data.slice();

// Deep copy (complete independence)
const copy3 = JSON.parse(JSON.stringify(data));

// Selective copy
const lightweightData = data.map(d => ({
  ticker: d.ticker,
  sector: d.sector,
  marketCap: d.marketCap
}));
```

## Common Patterns

### Parse and Enrich
```javascript
d3.csv("stocks.csv")
  .then(stocks => {
    // Type conversion
    stocks.forEach(d => {
      d.marketCap = +d.marketCap;
      d.employees = +d.employees;
    });

    // Filter out invalid
    stocks = stocks.filter(d => d.marketCap > 0);

    // Add computed fields
    stocks.forEach(d => {
      d.capFormatted = capFormatter(d.marketCap);
      d.category = categorizeByMarketCap(d.marketCap);
    });

    return stocks;
  })
  .then(processedData => visualize(processedData));
```

## Tips & Gotchas
- CSV string "1000000" stays a string until converted
- Empty cells become empty strings "", not null
- Use `d => d.value` to access object properties, not `d["value"]`
- D3's CSV parser handles quoted fields with commas automatically
- Use `Promise.all()` for loading multiple files in parallel
- Always validate data structure before visualizing
