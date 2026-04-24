---
name: d3-csv-loading
description: Load and parse CSV data with D3.js v6 using d3.csv() and d3.autoType for local file serving.
---

# Loading CSV Data with D3.js v6

## d3.csv()
```js
const data = await d3.csv("data/stock-descriptions.csv", d3.autoType);
```
- `d3.autoType` auto-converts numeric strings to numbers.
- For local files, must be served via HTTP (use `python3 -m http.server`).

## Handling CSV with Quoted Fields
D3's CSV parser handles RFC 4180 (quoted fields with commas inside). The `stock-descriptions.csv` has columns:
- `,ticker,sector,full name,marketCap,fullTimeEmployees,longBusinessSummary,country,website,...`
- First column is an unnamed index column.

## Key Pattern: Inline Data
When local file serving is not guaranteed, embed data as a JS variable:
```js
const DATA = [...];  // pre-processed JSON array
```
This avoids CORS/fetch issues when opening HTML files directly with `file://`.
