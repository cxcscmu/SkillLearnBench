---
name: d3-force-bubble-chart
description: Build a force-simulation bubble chart in D3.js v6 where bubbles are sized by a numeric value, colored by category, and clustered by category using forceX/forceY. Covers deterministic layout, collision, and tick-based settling.
---

# D3 v6 Force Bubble Chart

## Overview

A force-simulated bubble chart positions nodes using D3's `forceSimulation`. Each bubble is a circle sized by a data value (e.g. market cap) and colored by a categorical variable (e.g. sector). Nodes in the same category are attracted to a common cluster center via `forceX`/`forceY`.

## Core Pattern

```javascript
// 1. Compute cluster centers per category
const categories = [...new Set(data.map(d => d.category))].sort();
const clusterCenters = {};
categories.forEach((cat, i) => {
    const angle = (2 * Math.PI * i) / categories.length;
    clusterCenters[cat] = {
        x: width / 2 + clusterRadius * Math.cos(angle),
        y: height / 2 + clusterRadius * Math.sin(angle)
    };
});

// 2. Size scale (sqrt for area perception)
const rScale = d3.scaleSqrt()
    .domain([0, d3.max(data, d => d.value)])
    .range([MIN_R, MAX_R]);

// 3. Assign initial positions deterministically (sort by category then name)
const sorted = [...data].sort((a, b) =>
    a.category.localeCompare(b.category) || a.name.localeCompare(b.name)
);
sorted.forEach((d, i) => {
    const center = clusterCenters[d.category];
    d.x = center.x + (i % 5 - 2) * 20;  // grid offset
    d.y = center.y + (Math.floor(i / 5) - 2) * 20;
});

// 4. Force simulation
const simulation = d3.forceSimulation(sorted)
    .force('x', d3.forceX(d => clusterCenters[d.category].x).strength(0.15))
    .force('y', d3.forceY(d => clusterCenters[d.category].y).strength(0.15))
    .force('collide', d3.forceCollide(d => rScale(d.value) + PADDING).strength(0.8))
    .force('charge', d3.forceManyBody().strength(-5))
    .stop();  // Stop auto-ticking

// 5. Run ticks deterministically
simulation.tick(300);

// 6. Draw circles at settled positions
const node = svg.selectAll('circle')
    .data(sorted)
    .join('circle')
    .attr('cx', d => d.x)
    .attr('cy', d => d.y)
    .attr('r', d => rScale(d.value))
    .attr('fill', d => colorScale(d.category));
```

## ETF / Missing-Value Handling

ETFs have no market cap. Use a uniform fallback radius:

```javascript
const r = d.marketCap ? rScale(d.marketCap) : ETF_RADIUS;
```

## Cluster Centering Strategy

For 5 sectors use a pentagon layout:

```javascript
const N = categories.length;
categories.forEach((cat, i) => {
    const angle = (2 * Math.PI * i / N) - Math.PI / 2; // start at top
    clusterCenters[cat] = {
        x: cx + clusterRadius * Math.cos(angle),
        y: cy + clusterRadius * Math.sin(angle)
    };
});
```

Adjust `clusterRadius` (e.g. 160–200px) and `forceX/forceY strength` (0.1–0.2) to keep clusters tightly grouped.

## Labels Inside Bubbles

```javascript
svg.selectAll('text.label')
    .data(sorted)
    .join('text')
    .attr('class', 'label')
    .attr('x', d => d.x)
    .attr('y', d => d.y)
    .attr('dy', '0.35em')
    .attr('text-anchor', 'middle')
    .style('font-size', d => Math.min(12, rScale(d.value) * 0.45) + 'px')
    .style('pointer-events', 'none')
    .text(d => d.ticker);
```

## Key Parameters

| Parameter | Typical Value | Effect |
|-----------|---------------|--------|
| `forceX/Y strength` | 0.1–0.2 | Higher = tighter clusters |
| `forceCollide strength` | 0.7–1.0 | Higher = less overlap |
| `forceManyBody strength` | -5 to -20 | Repulsion between nodes |
| `simulation.tick(N)` | 200–400 | More ticks = more settled |
| `clusterRadius` | 150–220px | Distance between cluster centers |
| `PADDING` | 1.5–3px | Gap between bubbles |

## Gotchas

- Always call `.stop()` before `.tick(N)` for deterministic layout.
- Use `d3.scaleSqrt` (not linear) for bubble radius so area is proportional.
- After ticking, positions are in `d.x`, `d.y` — bind them with `.attr('cx', d => d.x)`.
- Keep initial positions near the cluster center to aid convergence.
