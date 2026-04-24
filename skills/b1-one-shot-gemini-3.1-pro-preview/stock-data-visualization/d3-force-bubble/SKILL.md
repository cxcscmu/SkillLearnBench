---
name: d3-force-bubble
description: Guide for creating clustered bubble charts using D3.js force simulations (v6+), including collision and categorization.
---

# D3.js Force Bubble Chart

This skill covers setting up a D3 force simulation to create a clustered bubble chart.

## Setup
You need `d3.forceSimulation` combined with positioning forces (`forceX`, `forceY`) and collision forces (`forceCollide`).

```javascript
const simulation = d3.forceSimulation(data)
  .force("x", d3.forceX(d => clusterCenters[d.category].x).strength(0.1))
  .force("y", d3.forceY(d => clusterCenters[d.category].y).strength(0.1))
  .force("collide", d3.forceCollide().radius(d => d.radius + 1).iterations(2))
  .on("tick", ticked);

function ticked() {
  node
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);
}
```

## Considerations
- **Radius Scaling**: Use `d3.scaleSqrt()` for sizing bubbles by area (e.g., Market Cap).
- **Collision**: Ensure the radius in `forceCollide` matches the visible radius. Add a small buffer (e.g., `+ 1`) for visual separation.
- **Clustering**: Calculate centers for each category beforehand, or dynamically adjust `forceX`/`forceY` based on the category of the node.
