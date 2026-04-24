---
name: d3-data-formatting
description: Loading CSV data, formatting currency/large numbers, and implementing tooltips in D3.
---

# Data Processing and Tooltips in D3

Efficient data visualization requires robust parsing and clear numerical presentation.

## Loading Multiple CSVs
Use `Promise.all` with `d3.csv` to load multiple datasets before initializing the visualization.

```javascript
Promise.all([
    d3.csv("data/stock-descriptions.csv"),
    d3.csv("data/indiv-stock/AAPL.csv")
]).then(([descriptions, aaplData]) => {
    // Process and merge data
});
```

## Number Formatting
For market capitalization, use `d3.format` or custom logic to convert large numbers into readable strings (e.g., Trillions 'T', Billions 'B').

```javascript
function formatMarketCap(d) {
    if (!d || d === "") return "N/A";
    const val = parseFloat(d);
    if (val >= 1e12) return (val / 1e12).toFixed(2) + "T";
    if (val >= 1e9) return (val / 1e9).toFixed(2) + "B";
    if (val >= 1e6) return (val / 1e6).toFixed(2) + "M";
    return val.toLocaleString();
}
```

## Tooltips
Create a hidden `div` and update its position and content on mouse events.

```javascript
const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

nodes.on("mouseover", (event, d) => {
    tooltip.transition().duration(200).style("opacity", .9);
    tooltip.html(`Ticker: ${d.ticker}<br/>Sector: ${d.sector}`)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 28) + "px");
})
.on("mouseout", () => {
    tooltip.transition().duration(500).style("opacity", 0);
});
```
