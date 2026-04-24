---
name: run2_d3-bubble-chart
description: Implementing force-directed bubble charts with category clustering and tooltips.
---
# Advanced Bubble Charts with Clustering

Use `d3.forceX` and `forceY` with scale mapping for sector clustering.

```javascript
const sectorX = d3.scalePoint().domain(sectors).range([width/4, 3*width/4]);

simulation.force("x", d3.forceX(d => sectorX(d.sector)).strength(0.1));
```
Tooltip handling:
```javascript
node.on("mouseover", (event, d) => {
    // Show tooltip div
});
```
