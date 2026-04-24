---
name: d3-force-bubble-chart
description: Create sector-clustered bubble charts with D3.js force simulation. Use this skill when building bubble charts that need to cluster elements by category (sectors, regions, types), avoid overlap, size bubbles by numeric values, and organize clusters spatially. Common patterns include market analysis dashboards, portfolio visualizations, and categorical bubble charts with dynamic clustering.
---

# D3.js Force Simulation Bubble Chart

This skill covers how to build interactive, clustered bubble charts using D3 v6 force simulation.

## Key Components

### 1. Force Simulation Setup

Create a force simulation that organizes bubbles into sector clusters:

```javascript
const simulation = d3.forceSimulation(data)
  .force("x", d3.forceX()
    .strength(0.05)
    .x(d => xPositionBySector(d.sector)))
  .force("y", d3.forceY()
    .strength(0.05)
    .y(d => yPositionBySector(d.sector)))
  .force("collide", d3.forceCollide()
    .radius(d => d.radius + 2))
  .force("charge", d3.forceManyBody().strength(-30))
  .on("tick", updatePositions);
```

**Why these forces:**
- **forceX/forceY**: Pull bubbles toward sector-specific positions, creating clusters
- **forceCollide**: Prevents bubble overlap by pushing circles apart when they collide
- **forceManyBody**: Adds repulsion to prevent tight clustering (negative strength = repulsion)

### 2. Sector Clustering Strategy

Define center positions for each sector. Common approaches:

**Grid layout (simple, predictable):**
```javascript
function getSectorPosition(sector, sectors) {
  const index = sectors.indexOf(sector);
  const cols = Math.ceil(Math.sqrt(sectors.length));
  const x = (index % cols) * (width / cols) + width / (cols * 2);
  const y = Math.floor(index / cols) * (height / 2) + height / 4;
  return {x, y};
}
```

**Circle layout (more compact):**
```javascript
function getSectorPosition(sector, sectors) {
  const index = sectors.indexOf(sector);
  const angle = (index / sectors.length) * 2 * Math.PI;
  const radius = 150;
  return {
    x: width / 2 + radius * Math.cos(angle),
    y: height / 2 + radius * Math.sin(angle)
  };
}
```

### 3. Bubble Sizing

Size bubbles proportionally to numeric values (market cap):

```javascript
const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.marketCap || 0)])
  .range([3, 40]);

data.forEach(d => {
  d.radius = d.marketCap ? radiusScale(d.marketCap) : 20; // Default for ETFs
});
```

**Why `scaleSqrt`:** Area scales linearly with value (perceived area = value)

### 4. Color by Sector

```javascript
const colorScale = d3.scaleOrdinal()
  .domain(sectors)
  .range(d3.schemeSet2); // or d3.schemeCategory10, etc.
```

### 5. Labels Inside Bubbles

Ensure text remains readable inside bubbles:

```javascript
svg.selectAll("text")
  .attr("x", d => d.x)
  .attr("y", d => d.y)
  .attr("text-anchor", "middle")
  .attr("dy", "0.3em")
  .attr("font-size", d => Math.max(10, d.radius * 0.4) + "px")
  .attr("pointer-events", "none")
  .text(d => d.ticker);
```

### 6. Handling Missing Data

For ETFs (no market cap):
- Set to default radius: `d.radius = 20`
- Still cluster by sector
- Don't exclude from visualization
- Optionally use different styling (stroke, opacity) to indicate missing data

### 7. Hover Tooltips

```javascript
circles.on("mouseover", function(event, d) {
  if (!d.marketCap) return; // Skip ETFs

  const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .html(`<strong>${d.ticker}</strong><br/>${d.name}<br/>${d.sector}`);

  tooltip
    .style("left", (event.pageX + 10) + "px")
    .style("top", (event.pageY - 28) + "px");
})
.on("mouseout", function() {
  d3.selectAll(".tooltip").remove();
});
```

## Performance Tips

- Use `simulation.alpha(0)` after manual positioning to skip initial layout
- Limit to 100-200 nodes for smooth animations; beyond that, optimize with quadtrees
- Cache radius calculations instead of computing in loops

## Testing Checklist

- [ ] Bubbles cluster by sector visually
- [ ] No overlapping bubbles (forceCollide working)
- [ ] Bubbles sized proportionally to market cap
- [ ] Text labels fit inside bubbles
- [ ] ETFs sized uniformly, no tooltips shown
- [ ] Sector colors distinct and consistent with legend
