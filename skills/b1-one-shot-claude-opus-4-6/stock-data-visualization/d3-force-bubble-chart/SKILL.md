---
name: d3-force-bubble-chart
description: Create force-simulation bubble charts with D3.js v6, including sector clustering, collision avoidance, tooltips, and legends.
---

# D3.js v6 Force-Simulation Bubble Chart

## Key Concepts
- Use `d3.forceSimulation()` with `forceX`, `forceY`, `forceCollide`, and `forceManyBody` to position bubbles.
- Cluster by category using `forceX(sectorX).strength(...)` and `forceY(sectorY).strength(...)`.
- Size bubbles via a `d3.scaleSqrt()` mapped from data (e.g., market cap) to radius.
- Color bubbles via `d3.scaleOrdinal(d3.schemeTableau10)` keyed on sector.

## Force Simulation Pattern

```js
const simulation = d3.forceSimulation(data)
  .force("x", d3.forceX(d => sectorX(d.sector)).strength(0.3))
  .force("y", d3.forceY(d => sectorY(d.sector)).strength(0.3))
  .force("collide", d3.forceCollide(d => radiusScale(d.marketCap) + 1.5))
  .force("charge", d3.forceManyBody().strength(-2))
  .on("tick", ticked);
```

## Sector Clustering
Assign each sector a target (x, y) position to group bubbles:
```js
const sectors = [...new Set(data.map(d => d.sector))];
const sectorPositions = {};
sectors.forEach((s, i) => {
  const angle = (2 * Math.PI * i) / sectors.length;
  sectorPositions[s] = {
    x: centerX + clusterRadius * Math.cos(angle),
    y: centerY + clusterRadius * Math.sin(angle)
  };
});
```

## Tooltips
Use a `div.tooltip` with `position: absolute` and `pointer-events: none`. Show on mouseover, hide on mouseout.

## Legend
Render colored rectangles + text labels for each sector using SVG `<g>` elements.
