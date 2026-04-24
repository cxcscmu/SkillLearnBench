---
name: d3-stock-viz
description: Use this skill for D3.js (v6) force-directed bubble charts and linked data tables. Always use this when tasked with financial data visualization using D3.js.
---

# D3.js Financial Visualization Skill

## Force-Directed Bubble Chart Guidelines
- **Simulation**: Use `d3.forceSimulation()` with `forceX`, `forceY` (center by sector), and `forceCollide` (radius + padding).
- **Sizing**: Size bubbles by `marketCap`. Use `d3.scaleSqrt()` for mapping `marketCap` to `radius`.
- **Coloring**: Map `sector` to a categorical color scale like `d3.scaleOrdinal(d3.schemeCategory10)`.
- **Interaction**: Add `mouseover`/`mouseout` events for tooltips. Add `click` events to sync with the data table.

## Linked Data Table Guidelines
- **Columns**: "Ticker symbol", "Full company name", "Sector", "Market cap" (formatted as "1.64T").
- **Linking**: Use a common data join or ID mapping to link table rows with bubble chart circles. Highlight both on `click` or `hover`.

## Data Handling
- **Loading**: Use `d3.csv()` with `d3.autoType`.
- **Filtering/Cleaning**: Filter out ETF entries (missing `marketCap`). Ensure numbers are properly parsed.
