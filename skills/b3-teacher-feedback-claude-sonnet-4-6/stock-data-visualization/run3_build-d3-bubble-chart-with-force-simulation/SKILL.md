---
name: build-d3-bubble-chart-with-force-simulation
description: Use when building a D3.js v6 bubble chart with force simulation, sector clustering, collision detection, tooltips, and interactive highlighting. Handles ETFs (no marketCap/sector) as a separate cluster.
---

# D3 v6 Bubble Chart with Force Simulation

## Key Requirements
- Bubbles sized by `marketCap` (ETFs get uniform size)
- Colored by sector; ETFs assigned sector `'ETF'` as fallback
- Force simulation with `forceX`/`forceY` pulling toward cluster centers
- `forceCollide` prevents overlap
- Pre-tick simulation with `.stop()` + `.tick(N)` for static initial render
- Tooltip on hover for non-ETF stocks only (detected by `!d.marketCap`)
- Click interaction highlights corresponding table row

## ETF Handling Pattern
```javascript
// In data loading — assign fallback sector BEFORE building clusterCenters
data.forEach(d => {
  if (!d.sector || d.sector.trim() === '') {
    d.sector = 'ETF';
  }
  // Parse marketCap as number if present
  d.marketCapNum = d.marketCap ? parseFloat(d.marketCap) : null;
});
```

## Cluster Centers Pattern
```javascript
const sectors = [...new Set(data.map(d => d.sector))];
const numSectors = sectors.length;
// Arrange cluster centers in a grid or circle
const clusterCenters = {};
sectors.forEach((sector, i) => {
  const angle = (i / numSectors) * 2 * Math.PI;
  clusterCenters[sector] = {
    x: innerW / 2 + (innerW * 0.35) * Math.cos(angle),
    y: innerH / 2 + (innerH * 0.35) * Math.sin(angle)
  };
});
```

## Force Simulation Pattern
```javascript
const simulation = d3.forceSimulation(data)
  .force('x', d3.forceX(d => clusterCenters[d.sector].x).strength(0.15))
  .force('y', d3.forceY(d => clusterCenters[d.sector].y).strength(0.15))
  .force('collide', d3.forceCollide(d => radiusScale(d.marketCapNum || minBubbleR) + 2))
  .stop();

// Pre-tick for static render
for (let i = 0; i < 300; i++) simulation.tick();

// Validate positions
data.forEach(d => {
  if (isNaN(d.x) || isNaN(d.y)) {
    d.x = innerW / 2;
    d.y = innerH / 2;
  }
});
```

## Tooltip Pattern (ETF-safe)
```javascript
node.on('mouseover', function(event, d) {
  if (!d.marketCap) return;  // Skip ETFs — no marketCap means ETF
  tooltip
    .style('opacity', 1)
    .html(`<strong>${d.ticker}</strong><br>${d.name}<br>${d.sector}`)
    .style('left', (event.pageX + 12) + 'px')
    .style('top', (event.pageY - 28) + 'px');
})
.on('mouseout', function(event, d) {
  if (!d.marketCap) return;
  tooltip.style('opacity', 0);
});
```

## Tooltip CSS
```css
.tooltip {
  position: absolute;
  background: rgba(0,0,0,0.75);
  color: #fff;
  padding: 8px 12px;
  border-radius: 4px;
  pointer-events: none;
  font-size: 13px;
  opacity: 0;  /* hidden by default via opacity, not display:none */
  transition: opacity 0.15s;
}
```

## SVG Container in HTML
```html
<!-- Must exist before JS runs -->
<div id="bubble-chart"></div>
```

## Color Scale Including ETF
```javascript
const colorScale = d3.scaleOrdinal(d3.schemeTableau10)
  .domain(sectors);  // sectors already includes 'ETF' from fallback assignment
```