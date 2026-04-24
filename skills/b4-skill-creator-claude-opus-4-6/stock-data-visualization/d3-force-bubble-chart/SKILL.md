---
name: d3-force-bubble-chart
description: >
  Build D3.js v6 force-simulation bubble charts where bubbles are sized by a numeric metric,
  colored by category, and clustered by category using forceX/forceY. Use this skill whenever
  the user asks for bubble charts, force-layout visualizations, or clustered circle packing
  with D3.js. Triggers on: bubble chart, force simulation, cluster layout, circle packing.
---

# D3 Force Bubble Chart

## Overview

A force-simulation bubble chart uses `d3.forceSimulation` to position circles (bubbles) in a
layout where they are clustered by category, sized by a numeric value, and colored by category.

## Architecture

### Sizing Bubbles

Use `d3.scaleSqrt()` to map a numeric value (e.g., market cap) to bubble radius. Square-root
scaling ensures area is proportional to value, which is perceptually accurate.

```js
const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.value)])
  .range([minRadius, maxRadius]);
```

For items missing the sizing metric (e.g., ETFs with no market cap), assign a uniform default radius.

### Coloring by Category

Use `d3.scaleOrdinal()` with a color scheme like `d3.schemeTableau10`:

```js
const colorScale = d3.scaleOrdinal()
  .domain(categories)
  .range(d3.schemeTableau10);
```

### Clustering with Force Simulation

Use `forceX` and `forceY` to pull bubbles toward category-specific cluster centers.
Calculate cluster centers by dividing the chart space into a grid or ring layout based on
the number of categories.

```js
// Compute cluster center positions
const sectorCenters = {};
sectors.forEach((sector, i) => {
  const angle = (2 * Math.PI * i) / sectors.length;
  sectorCenters[sector] = {
    x: centerX + clusterRadius * Math.cos(angle),
    y: centerY + clusterRadius * Math.sin(angle)
  };
});

const simulation = d3.forceSimulation(data)
  .force("x", d3.forceX(d => sectorCenters[d.sector].x).strength(0.3))
  .force("y", d3.forceY(d => sectorCenters[d.sector].y).strength(0.3))
  .force("collide", d3.forceCollide(d => radiusScale(d.value) + padding))
  .force("charge", d3.forceManyBody().strength(-5))
  .on("tick", ticked);
```

Key tuning parameters:
- **forceX/forceY strength**: 0.2–0.4 keeps clusters tight without excessive overlap
- **forceCollide padding**: 1–3px between bubbles
- **forceManyBody strength**: Small negative value (-2 to -10) for gentle repulsion

### Labels Inside Bubbles

Add `<text>` elements centered on each bubble. Only show labels when the bubble is large
enough to contain the text (check radius vs. text length).

```js
node.append("text")
  .text(d => d.ticker)
  .attr("text-anchor", "middle")
  .attr("dy", "0.35em")
  .style("font-size", d => Math.min(radiusScale(d.value) * 0.6, 14) + "px");
```

### Tooltips

Use a `<div>` with `position: absolute` that follows the mouse on `mouseover`/`mousemove`
and hides on `mouseout`.

### Legends

Add a legend mapping colors to sector names. Position it in a corner or below the chart.
Use small colored circles/rectangles paired with text labels.

## Common Pitfalls

- Forgetting `forceCollide` causes overlapping bubbles
- Using `forceCenter` with `forceX`/`forceY` creates fighting forces — avoid `forceCenter`
  when using explicit cluster positioning
- Not calling `simulation.stop()` or limiting ticks can cause layout jitter
- Cluster centers too far apart leads to scattered layout — keep `clusterRadius` moderate
  relative to chart width
