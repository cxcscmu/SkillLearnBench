---
name: run2_d3_bubble_clusters
description: Production-ready D3.js bubble chart clustering with optimized force simulation and labeling
---

# D3.js Bubble Chart Clustering - Production Implementation

## Problem Statement
Creating a clustered bubble chart where bubbles group by sector with:
- Proportional sizing (market cap)
- Automatic sector positioning
- No bubble overlap
- Readable internal labels
- Responsive, centered layout

## Complete Implementation Pattern

### 1. Sector Grid Layout
Calculate even distribution of sector centers:

```javascript
// Get unique sectors and calculate grid dimensions
const sectors = Array.from(new Set(data.map(d => d.sector)));
const numSectors = sectors.length;
const cols = Math.ceil(Math.sqrt(numSectors));
const rows = Math.ceil(numSectors / cols);

// Available space
const width = 800;  // SVG width
const height = 600; // SVG height

// Calculate spacing
const spacingX = width / (cols + 1);
const spacingY = height / (rows + 1);

// Map sectors to positions
const sectorPositions = {};
sectors.forEach((sector, i) => {
  const col = i % cols;
  const row = Math.floor(i / cols);
  sectorPositions[sector] = {
    x: spacingX * (col + 1),
    y: spacingY * (row + 1)
  };
});
```

### 2. Optimal Force Configuration
```javascript
const simulation = d3.forceSimulation(nodes)
  // Clustering forces: Pull nodes toward sector centers
  .force("x", d3.forceX()
    .strength(0.08)           // Moderate pull strength
    .x(d => sectorPositions[d.sector].x))
  .force("y", d3.forceY()
    .strength(0.08)           // Balanced x and y
    .y(d => sectorPositions[d.sector].y))
  // Collision detection: Prevent overlap
  .force("collide", d3.forceCollide()
    .radius(d => d.radius + 3))  // Add padding
  // Charge: Light repulsion for natural spread
  .force("charge", d3.forceManyBody()
    .strength(-15))           // Negative = repulsion
  // Decay: Control convergence speed
  .alphaDecay(0.02);          // Slower convergence for stability
```

### 3. Bubble Sizing with Fallback
```javascript
// Filter data with market cap (exclude nulls)
const marketCapValues = data
  .filter(d => d.marketCap)
  .map(d => d.marketCap);

// Create scale from filtered data
const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(marketCapValues)])
  .range([10, 50]);

// Use uniform size for items without marketCap
const nodes = data.map(d => ({
  ...d,
  radius: d.marketCap ? radiusScale(d.marketCap) : 15
}));
```

### 4. Label Sizing and Positioning
Automatically size labels based on bubble size:

```javascript
const labels = svg.selectAll("text")
  .data(nodes)
  .enter()
  .append("text")
  .attr("x", d => d.x)
  .attr("y", d => d.y)
  .attr("dy", "0.3em")
  .attr("text-anchor", "middle")
  .attr("font-size", d => {
    // Scale font inversely: larger bubbles = larger text
    const size = d.radius;
    return Math.max(8, Math.min(14, size / 4));
  })
  .attr("fill", "white")
  .attr("font-weight", "bold")
  .attr("pointer-events", "none")  // Don't interfere with bubble clicks
  .text(d => d.ticker);
```

### 5. Update Loop
```javascript
simulation.on("tick", () => {
  // Update circles
  circles
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);

  // Update labels to stay centered in bubbles
  labels
    .attr("x", d => d.x)
    .attr("y", d => d.y);
});
```

## Key Tuning Parameters

| Parameter | Value | Effect |
|-----------|-------|--------|
| forceX/Y strength | 0.08 | Controls cluster tightness |
| forceCollide radius | radius + 3 | Padding between bubbles |
| forceManyBody strength | -15 | Repulsion between clusters |
| alphaDecay | 0.02 | Convergence speed (lower = slower/smoother) |

Adjust these based on:
- **Tighter clustering**: Increase force strength to 0.1-0.15
- **Looser clusters**: Decrease to 0.05
- **More repulsion**: Decrease strength to -20 or -30
- **Faster convergence**: Increase alphaDecay to 0.05

## Centering Clusters
Sector centers automatically distribute to fill the canvas. For perfect centering:

```javascript
// Center the overall layout
const minX = Math.min(...Object.values(sectorPositions).map(p => p.x));
const maxX = Math.max(...Object.values(sectorPositions).map(p => p.x));
const minY = Math.min(...Object.values(sectorPositions).map(p => p.y));
const maxY = Math.max(...Object.values(sectorPositions).map(p => p.y));

const offsetX = (width - (maxX - minX)) / 2 - minX;
const offsetY = (height - (maxY - minY)) / 2 - minY;

// Apply offset to all sector positions
Object.values(sectorPositions).forEach(pos => {
  pos.x += offsetX;
  pos.y += offsetY;
});
```

## Performance Optimization
- Set alphaDecay low (0.02) for smooth animations
- Limit nodes to ~200 for optimal interactivity
- Use requestAnimationFrame for label updates
- Cache sector positions and scales

## Common Issues & Fixes

**Issue: Bubbles clustering too tightly**
- Solution: Reduce force strength to 0.05, increase collision radius

**Issue: Clusters drifting apart**
- Solution: Increase force strength to 0.12, decrease alphaDecay to 0.015

**Issue: Labels overlapping bubbles**
- Solution: Increase font-size calculation multiplier or reduce min font-size

**Issue: Simulation running forever**
- Solution: Increase alphaDecay to 0.03 or set manual `.stop()` after timeout
