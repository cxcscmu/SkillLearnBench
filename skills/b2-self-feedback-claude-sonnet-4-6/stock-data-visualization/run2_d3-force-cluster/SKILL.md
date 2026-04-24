---
name: run2_d3-force-cluster
description: D3.js v6 force simulation for clustered bubbles by category using forceX/forceY anchors, forceCollide for no overlap, with truly deterministic initial positions.
---

# D3.js v6 Force Cluster Simulation (Improved)

## Key Principles
1. **Never use Math.random()** — use deterministic golden-angle spiral per sector
2. **Run fixed ticks**, then stop — don't animate
3. **Clamp final positions** within SVG bounds after simulation
4. Use **forceX + forceY strength 0.10–0.15** for cohesive clusters

## Sector Center Layout
With 5 sectors, use a ring with one sector on top and four around it:
```javascript
const sectors = Object.keys(SECTOR_COLORS);  // sorted, predictable
const W = 800, H = 600;
const cx = W / 2, cy = H / 2;

const sectorCenters = {};
sectors.forEach((sector, i) => {
    // Elliptical placement; adjust rx/ry for chart proportions
    const angle = (i / sectors.length) * 2 * Math.PI - Math.PI / 2;
    sectorCenters[sector] = {
        x: cx + (W * 0.28) * Math.cos(angle),
        y: cy + (H * 0.28) * Math.sin(angle)
    };
});
```

## Deterministic Initial Positions (Critical!)
D3's simulation starts from node x/y. Seed them deliberately:
```javascript
const sectorCounters = {};
// Sort nodes deterministically before seeding
const nodes = [...data].sort((a, b) => a.ticker.localeCompare(b.ticker));
nodes.forEach(d => {
    const center = sectorCenters[d.sector];
    const i = sectorCounters[d.sector] = (sectorCounters[d.sector] || 0);
    sectorCounters[d.sector]++;
    // Golden-angle spiral — fully deterministic, no Math.random()
    const angle = i * 2.39996;   // golden angle ≈ 137.5°
    const r = 6 * Math.sqrt(i + 1);
    d.x = center.x + r * Math.cos(angle);
    d.y = center.y + r * Math.sin(angle);
});
```

## Force Simulation Setup
```javascript
const simulation = d3.forceSimulation(nodes)
    .force('x', d3.forceX(d => sectorCenters[d.sector].x).strength(0.12))
    .force('y', d3.forceY(d => sectorCenters[d.sector].y).strength(0.12))
    .force('collide', d3.forceCollide(d => d.radius + 2).strength(1.0))
    .force('charge', d3.forceManyBody().strength(-10))
    .alphaDecay(0.02)
    .stop();  // Don't auto-run

// Run exactly 400 ticks for determinism
for (let i = 0; i < 400; i++) simulation.tick();

// Clamp to SVG bounds
nodes.forEach(d => {
    d.x = Math.max(d.radius + 4, Math.min(W - d.radius - 4, d.x));
    d.y = Math.max(d.radius + 4, Math.min(H - d.radius - 4, d.y));
});
```

## Placing SVG Elements After Simulation
Since we stop before rendering, just set attributes directly (no ticking):
```javascript
circles.attr('cx', d => d.x).attr('cy', d => d.y);
labels.attr('x', d => d.x).attr('y', d => d.y);
```

## Responsive SVG
Use viewBox on the SVG and measure container at draw time:
```javascript
const W = container.clientWidth || 700;
const H = container.clientHeight || 560;
svg.attr('viewBox', `0 0 ${W} ${H}`)
   .attr('preserveAspectRatio', 'xMidYMid meet');
```

## Tuning Guidance
- More nodes in a sector → increase `W * 0.28` slightly so clusters have more room
- Large radius variance → reduce `forceX/Y strength` to 0.08 so big bubbles don't push out
- Overlap still present → increase collide strength or reduce MAX_RADIUS
