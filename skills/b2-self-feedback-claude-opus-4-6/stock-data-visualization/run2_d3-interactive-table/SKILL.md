---
name: run2_d3-interactive-table
description: D3.js data table with exact column headers, formatted market cap, and bidirectional highlight with bubble chart.
---

# D3 Interactive Data Table (Improved)

## Column Headers Must Match Spec Exactly
The task specifies: "Ticker symbol", "Full company name", "Sector", "Market cap"

```js
const columns = ["Ticker symbol", "Full company name", "Sector", "Market cap"];
```

## Market Cap Formatting
Format for human readability (e.g., "1.64T", "553.43B"):
```js
function formatMarketCap(val) {
  if (!val || isNaN(val)) return "N/A";
  val = +val;
  if (val >= 1e12) return (val / 1e12).toFixed(2) + "T";
  if (val >= 1e9) return (val / 1e9).toFixed(2) + "B";
  if (val >= 1e6) return (val / 1e6).toFixed(2) + "M";
  return val.toFixed(0);
}
```

## Bidirectional Highlighting
- Click bubble -> highlight row + scroll into view
- Click row -> highlight bubble
- Use a shared `highlightStock(ticker)` function
- Reset previous highlights before applying new ones
