---
name: d3-force-simulation
description: D3.js force simulation for creating interactive bubble charts with clustering, collision detection, and physics-based positioning
---

# D3.js Force Simulation

## Overview
Force simulation in D3 uses physics-based algorithms to position nodes (bubbles) based on forces. Perfect for creating bubble charts with natural-looking clusters.

## Core Concepts

### 1. Creating a Simulation
```javascript
const simulation = d3.forceSimulation(nodes)
  .force("name", forceFunction)
  .on("tick", updatePositions);

// Start simulation (runs in background)
simulation.alpha(1);  // reset energy
```

### 2. Common Forces

#### forceX / forceY
Position bubbles toward target x/y coordinates (creates clustering):

```javascript
// Group by sector - each sector gets target x position
const sectors = Array.from(new Set(data.map(d => d.sector)));
const sectorX = d3.scalePoint()
  .domain(sectors)
  .range([0, width]);

const simulation = d3.forceSimulation(nodes)
  .force("x", d3.forceX()
    .x(d => sectorX(d.sector))  // each sector pulled to its x position
    .strength(0.05)              // weak force (allows spreading)
  )
  .force("y", d3.forceY()
    .y(height / 2)               // all centered vertically
    .strength(0.03)
  );
```

#### forceCollide
Prevents bubbles from overlapping:

```javascript
.force("collide", d3.forceCollide()
  .radius(d => radiusScale(d.marketCap) + 2)  // add padding
  .strength(0.5)  // collision strength (0-1)
)
```

#### forceManyBody
Repulsive or attractive force between all nodes:

```javascript
.force("charge", d3.forceManyBody()
  .strength(-50)  // negative = repulsion, positive = attraction
)
```

### 3. Tick Events
Update positions on each simulation frame:

```javascript
simulation.on("tick", () => {
  // Update circles
  circles
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);

  // Update text
  labels
    .attr("x", d => d.x)
    .attr("y", d => d.y);
});
```

### 4. Preventing Bubbles from Moving Off-Screen

Fix nodes to boundaries:

```javascript
simulation.on("tick", () => {
  nodes.forEach(d => {
    // Clamp positions within bounds
    d.x = Math.max(d.radius, Math.min(width - d.radius, d.x));
    d.y = Math.max(d.radius, Math.min(height - d.radius, d.y));
  });

  // Update positions
  circles.attr("cx", d => d.x).attr("cy", d => d.y);
});
```

### 5. Interactive Dragging
Allow users to drag nodes:

```javascript
function drag(simulation) {
  return d3.drag()
    .on("start", (event, d) => {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    })
    .on("drag", (event, d) => {
      d.fx = event.x;
      d.fy = event.y;
    })
    .on("end", (event, d) => {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    });
}

circles.call(drag(simulation));
```

## Complete Example: Bubble Cluster Chart

```javascript
// Setup
const nodes = data.map(d => ({
  id: d.ticker,
  sector: d.sector,
  value: d.marketCap,
  radius: Math.sqrt(d.marketCap / Math.PI)
}));

const width = 800, height = 600;

// Scales
const sectorX = d3.scalePoint()
  .domain(Array.from(new Set(data.map(d => d.sector))))
  .range([100, width - 100]);

const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(nodes, d => d.value)])
  .range([5, 50]);

const colorScale = d3.scaleOrdinal()
  .domain(Array.from(new Set(data.map(d => d.sector))))
  .range(d3.schemeCategory10);

// Simulation
const simulation = d3.forceSimulation(nodes)
  .force("x", d3.forceX().x(d => sectorX(d.sector)).strength(0.05))
  .force("y", d3.forceY().y(height / 2).strength(0.03))
  .force("collide", d3.forceCollide().radius(d => radiusScale(d.value) + 2))
  .force("charge", d3.forceManyBody().strength(-30))
  .on("tick", () => {
    circles
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
  });

// Render
const svg = d3.select("body").append("svg")
  .attr("width", width).attr("height", height);

const circles = svg.selectAll("circle")
  .data(nodes)
  .join("circle")
  .attr("r", d => radiusScale(d.value))
  .attr("fill", d => colorScale(d.sector));
```

## Performance Tips
- Use `simulation.alphaMin(0.001)` to stop simulation faster
- Reduce `strength` values for smoother settling
- Use `radius` in forceCollide matching actual visual radius
- Call `simulation.stop()` when not needed to save CPU
