---
name: d3-force-clustering
description: Creating bubble clusters in D3.js using force simulations.
---

# D3 Force Clustering

Use `d3.forceSimulation` to organize data into clusters.

## Implementation Pattern

```javascript
const simulation = d3.forceSimulation(nodes)
  .force("charge", d3.forceManyBody().strength(1))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("collide", d3.forceCollide().radius(d => d.r + 1))
  .force("x", d3.forceX().x(d => clusterX(d.sector)))
  .force("y", d3.forceY().y(d => clusterY(d.sector)));
```
