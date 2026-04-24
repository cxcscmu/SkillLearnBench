---
name: run2_d3-force-bubble
description: D3.js v6 force-directed bubble chart with sector clustering, collision avoidance, size mapping, and cross-component interaction.
---

# D3 Force Bubble Chart (Improved)

## Key Improvements over run1
1. Use `<g>` group nodes for bubbles so click events work on both circle and label
2. Stronger clustering forces (0.4+ strength) to keep sectors tight
3. Center-of-mass approach: place sector centers using a well-spaced grid relative to SVG center
4. Higher collide iterations (4) and padding (2px) for clean separation
5. Clamp nodes to SVG bounds in tick handler

## Force Simulation Best Practices
```js
const simulation = d3.forceSimulation(data)
  .force("x", d3.forceX(d => sectorCenters[d.sector].x).strength(0.4))
  .force("y", d3.forceY(d => sectorCenters[d.sector].y).strength(0.4))
  .force("collide", d3.forceCollide(d => d.radius + 2).strength(0.8).iterations(4))
  .force("charge", d3.forceManyBody().strength(-3))
  .alphaDecay(0.02);
```

## Sector Grid Layout (5 sectors)
With 5 sectors, use a layout like:
- Row 1: 3 sectors spread across width
- Row 2: 2 sectors centered

```js
const positions = [
  {x: w*0.2, y: h*0.33}, {x: w*0.5, y: h*0.33}, {x: w*0.8, y: h*0.33},
  {x: w*0.35, y: h*0.7}, {x: w*0.65, y: h*0.7}
];
```

## Click on `<g>` group (not just circle)
```js
node.on("click", function(event, d) {
  highlightStock(d.ticker);
});
```
This catches clicks on both the circle and the text label.

## Tooltip: attach to node group, check sector
```js
node.on("mouseover", function(event, d) {
  if (d.sector === "ETF") return;
  // show tooltip
}).on("mouseout", function() {
  // hide tooltip
});
```
