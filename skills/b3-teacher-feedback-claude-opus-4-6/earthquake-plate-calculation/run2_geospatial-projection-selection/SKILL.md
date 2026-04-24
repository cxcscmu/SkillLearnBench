---
name: geospatial-projection-selection
description: Guidance on selecting appropriate CRS projections for geospatial distance calculations, especially EPSG:4087 for global analyses.
---

## EPSG:4087 — World Equidistant Cylindrical

- **Use case**: Global distance calculations where a single consistent projection is needed
- **Properties**: Equidistant along meridians; distances measured in meters
- **CRS string**: `EPSG:4087`

```python
gdf_projected = gdf.to_crs('EPSG:4087')
```

## When to use EPSG:4087 vs other projections

| Projection | Use case |
|---|---|
| EPSG:4326 | Spatial containment, lat/lon storage (unprojected) |
| EPSG:4087 | Global distance calculations in meters |
| Custom aeqd | Local distance calculations centered on a specific point |
| EPSG:3857 | Web mapping (NOT for distance/area calculations) |

## Important notes for Pacific plate analysis

- The Pacific plate crosses the antimeridian (±180° longitude)
- **Do NOT project the Pacific plate polygon** for containment checks — use EPSG:4326
- **Do project** points and boundaries to EPSG:4087 for distance calculations
- Use `make_valid()` from `shapely.validation` on plate polygons that may have topology issues