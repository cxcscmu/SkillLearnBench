---
name: run2_d3-force-clustering
description: Advanced clustering techniques in D3.js force simulations for compact and aesthetically pleasing layouts.
---

# Advanced D3 Force Clustering

This skill focuses on creating compact, sector-based clusters that are visually grouped but centrally located.

## Dynamic Cluster Centers

Instead of a rigid grid, use a radial layout or a packed grid for cluster centers to keep them "close together".

```javascript
const clusterCenters = sectors.map((s, i) => {
    const angle = (i / sectors.length) * 2 * Math.PI;
    const radius = 150; // Distance from center
    return {
        sector: s,
        x: width / 2 + radius * Math.cos(angle),
        y: height / 2 + radius * Math.sin(angle)
    };
});
```

## Collision with Padding

Ensure bubbles don't overlap by adding padding to the collision force.

```javascript
simulation.force("collide", d3.forceCollide().radius(d => getRadius(d) + 2).iterations(4));
```

## Grouping Forces

Apply forces that pull nodes towards their specific cluster center.

```javascript
simulation
    .force("x", d3.forceX(d => centers[d.sector].x).strength(0.2))
    .force("y", d3.forceY(d => centers[d.sector].y).strength(0.2))
    .force("center", d3.forceCenter(width / 2, height / 2));
```
