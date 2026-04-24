---
name: d3-force-bubble-chart
description: How to create a force-directed bubble chart in D3.js (v6+). Use this skill whenever the user asks to build a bubble chart, cluster bubbles by category, or use d3.forceSimulation to position SVG circles without overlap.
---

# d3-force-bubble-chart

This skill explains how to build a bubble chart using D3.js force simulations (`d3.forceSimulation`), size bubbles by data, color them by category, group them into clusters, and prevent overlap.

## Setting Up the Simulation

To arrange bubbles by a categorical group (like "sector" or "industry") while avoiding overlap, use a composite of forces:
1. `d3.forceX(d => ...)`: Pulls nodes toward a specific horizontal position.
2. `d3.forceY(d => ...)`: Pulls nodes toward a specific vertical position.
3. `d3.forceCollide(d => ...)`: Prevents nodes from overlapping based on their radius.

### Example

```javascript
// 1. Create scales
const sizeScale = d3.scaleSqrt()
  .domain([d3.min(data, d => d.value), d3.max(data, d => d.value)])
  .range([minRadius, maxRadius]); // e.g., [5, 40]

const colorScale = d3.scaleOrdinal(d3.schemeCategory10)
  .domain(categories);

// 2. Define cluster centers
// e.g., mapping category -> {x, y} coordinate
const categoryCenters = {
  "Category A": { x: 200, y: 300 },
  "Category B": { x: 400, y: 300 },
  "Category C": { x: 600, y: 300 }
};

// 3. Initialize nodes
// If using existing data, add radius property to help collision
const nodes = data.map(d => ({
  ...d,
  radius: sizeScale(d.value) || defaultRadius // Fallback for null values
}));

// 4. Create the SVG circles
const bubbles = svg.append("g")
  .selectAll("circle")
  .data(nodes)
  .join("circle")
  .attr("r", d => d.radius)
  .attr("fill", d => colorScale(d.category));

// 5. Create labels (optional)
const labels = svg.append("g")
  .selectAll("text")
  .data(nodes)
  .join("text")
  .text(d => d.name)
  .attr("text-anchor", "middle")
  .attr("dominant-baseline", "central");

// 6. Set up and run simulation
const simulation = d3.forceSimulation(nodes)
  // Cluster nodes horizontally/vertically based on category
  .force("x", d3.forceX(d => categoryCenters[d.category].x).strength(0.1))
  .force("y", d3.forceY(d => categoryCenters[d.category].y).strength(0.1))
  // Prevent overlap, adding padding
  .force("collide", d3.forceCollide(d => d.radius + 1).iterations(2))
  // Add a slight charge to push things apart, optional
  .force("charge", d3.forceManyBody().strength(-2));

// Update positions on each tick
simulation.on("tick", () => {
  bubbles
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);
    
  labels
    .attr("x", d => d.x)
    .attr("y", d => d.y);
});
```

## Tips for Force Bubble Charts

- **Determinism:** If you need deterministic (reproducible) positions instead of animation, call `simulation.tick(300)` synchronously in a loop and stop the simulation, rather than relying on the animated `"tick"` event.
- **Null values:** Handle missing numerical data carefully. If a value is missing, give it a default radius (e.g., ETFs without market cap should have a constant size).
- **Tooltips:** Refer to the D3.js visualization skill for adding tooltips on hover.
