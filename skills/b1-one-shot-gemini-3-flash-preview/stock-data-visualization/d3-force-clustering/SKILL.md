---
name: d3-force-clustering
description: Techniques for creating clustered bubble charts using D3 force simulations (v6).
---

# D3.js Force Simulation for Clustered Bubble Charts

D3's force simulation is essential for creating bubble charts where elements are grouped by categories (clusters) and prevented from overlapping.

## Key Forces

1.  **forceSimulation**: The engine that updates positions.
2.  **forceX / forceY**: Attracts nodes to specific coordinates. Use this to create clusters by mapping categories to center points.
3.  **forceCollide**: Prevents nodes from overlapping by specifying a radius.
4.  **forceCenter**: Keeps the entire group of nodes centered in the SVG.

## Usage Pattern

```javascript
const simulation = d3.forceSimulation(data)
    .force("x", d3.forceX(d => clusterCenters[d.sector].x).strength(0.1))
    .force("y", d3.forceY(d => clusterCenters[d.sector].y).strength(0.1))
    .force("collide", d3.forceCollide(d => radiusScale(d.value) + 2))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .on("tick", ticked);

function ticked() {
    nodes
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    
    labels
        .attr("x", d => d.x)
        .attr("y", d => d.y);
}
```

## Clustering Strategy
To group nodes by a "Sector" attribute:
1. Define a set of center points for each sector (e.g., arranged in a grid or circle).
2. Apply `forceX` and `forceY` targeting those centers.
3. Use a moderate `strength` (e.g., 0.1) to allow collision force to resolve overlaps while maintaining the cluster shape.
