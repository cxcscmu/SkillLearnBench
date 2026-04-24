---
name: find-earthquake-farthest-from-pacific-boundary
description: Find the earthquake within the Pacific plate (Code == "PA") that is farthest from the Pacific plate boundary lines in PB2002_boundaries.json. Uses an equal-area projection for accurate distance measurement. Filters boundaries where PlateA or PlateB equals "PA".
---

## Strategy

1. Load plate polygons, filter for Pacific plate using `Code == "PA"`.
2. Load boundaries, filter where `PlateA == "PA"` or `PlateB == "PA"`.
3. Filter earthquakes that fall **within** the Pacific plate polygon.
4. Project everything to an equal-area CRS.
5. Compute distance from each earthquake point to the unary_union of Pacific boundaries.
6. Find the maximum distance and output the result.

## Full Implementation

```python
import geopandas as gpd
import json
import pandas as pd
import numpy as np
from shapely.geometry import Point
import warnings
warnings.filterwarnings("ignore")

# ── 1. Load and inspect data ─────────────────────────────────────────────────
plates = gpd.read_file("/root/PB2002_plates.json")
print("Plates columns:", list(plates.columns))
print(plates.head(3).to_string())

boundaries = gpd.read_file("/root/PB2002_boundaries.json")
print("\nBoundaries columns:", list(boundaries.columns))
print(boundaries.head(3).to_string())

# ── 2. Find the Pacific plate polygon ────────────────────────────────────────
# Try common field names for plate code
plate_code_field = None
for candidate in ["Code", "code", "PlateName", "PLATENAME", "plate", "Plate"]:
    if candidate in plates.columns:
        plate_code_field = candidate
        break

if plate_code_field is None:
    print("Available plate columns:", plates.columns.tolist())
    raise ValueError("Cannot find plate code column")

print(f"\nUsing plate code field: '{plate_code_field}'")
print("Unique plate codes sample:", plates[plate_code_field].unique()[:20])

# Filter for Pacific plate (code "PA")
pacific_plate = plates[plates[plate_code_field] == "PA"].copy()
print(f"\nPacific plate rows: {len(pacific_plate)}")
print(pacific_plate[[plate_code_field, "geometry"]].to_string())

if len(pacific_plate) == 0:
    raise ValueError("No Pacific plate polygon found with Code == 'PA'")

pacific_polygon = pacific_plate.geometry.unary_union

# ── 3. Filter Pacific boundaries from PB2002_boundaries.json ─────────────────
print("\nBoundaries columns:", boundaries.columns.tolist())
print(boundaries.head(5).to_string())

# Find column names for PlateA / PlateB
plate_a_col = None
plate_b_col = None
for col in boundaries.columns:
    cl = col.lower()
    if "platea" in cl or cl == "plate_a":
        plate_a_col = col
    if "plateb" in cl or cl == "plate_b":
        plate_b_col = col

# Fallback: check for any column containing plate identifiers
if plate_a_col is None:
    print("Looking for plate identifier columns in boundaries...")
    for col in boundaries.columns:
        sample = boundaries[col].dropna().head(10).tolist()
        print(f"  {col}: {sample}")

print(f"PlateA col: {plate_a_col}, PlateB col: {plate_b_col}")

if plate_a_col and plate_b_col:
    pa_boundaries = boundaries[
        (boundaries[plate_a_col] == "PA") | (boundaries[plate_b_col] == "PA")
    ].copy()
else:
    # Try to find PA in any column
    mask = pd.Series([False] * len(boundaries))
    for col in boundaries.columns:
        if boundaries[col].dtype == object:
            mask = mask | boundaries[col].eq("PA")
    pa_boundaries = boundaries[mask].copy()

print(f"\nPacific boundaries count: {len(pa_boundaries)}")

if len(pa_boundaries) == 0:
    raise ValueError("No Pacific plate boundaries found")

# ── 4. Load earthquakes ────────────────────────────────────────────────────
with open("/root/earthquakes_2024.json") as f:
    eq_data = json.load(f)

rows = []
for feat in eq_data["features"]:
    props = feat["properties"]
    coords = feat["geometry"]["coordinates"]
    rows.append({
        "id": feat["id"],
        "place": props.get("place"),
        "time_ms": props.get("time"),
        "magnitude": props.get("mag"),
        "longitude": coords[0],
        "latitude": coords[1],
        "geometry": Point(coords[0], coords[1])
    })

eq_gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")
eq_gdf["time"] = pd.to_datetime(eq_gdf["time_ms"], unit="ms", utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
print(f"\nTotal earthquakes: {len(eq_gdf)}")

# ── 5. Filter earthquakes within Pacific plate polygon ────────────────────────
# The Pacific plate spans the antimeridian — use sjoin with the polygon
pacific_plate_4326 = pacific_plate.set_crs("EPSG:4326", allow_override=True) if pacific_plate.crs is None else pacific_plate.to_crs("EPSG:4326")

# Use spatial join (within) to find earthquakes inside Pacific plate
eq_in_pacific = gpd.sjoin(
    eq_gdf,
    pacific_plate_4326[["geometry"]],
    how="inner",
    predicate="within"
)
print(f"Earthquakes within Pacific plate (sjoin): {len(eq_in_pacific)}")

# Also try intersects as fallback if within gives 0
if len(eq_in_pacific) == 0:
    print("WARNING: 'within' returned 0 — trying manual contains check")
    mask = eq_gdf.geometry.apply(lambda pt: pacific_polygon.contains(pt))
    eq_in_pacific = eq_gdf[mask].copy()
    print(f"Earthquakes within Pacific plate (manual): {len(eq_in_pacific)}")

if len(eq_in_pacific) == 0:
    raise ValueError("No earthquakes found within Pacific plate polygon")

# Remove duplicate index columns if present
if "index_right" in eq_in_pacific.columns:
    eq_in_pacific = eq_in_pacific.drop(columns=["index_right"])

# ── 6. Project to equal-area CRS for accurate distance ────────────────────────
# World Azimuthal Equidistant centered near Pacific plate center
TARGET_CRS = "EPSG:3832"  # WGS 84 / PDC Mercator (Pacific-centered)
# Better option: use a Pacific-centered equal-area projection
# EPSG:3832 is Pacific-centered but Mercator
# Use custom Lambert Azimuthal Equal Area centered on Pacific
pacific_center_lon = 180.0
pacific_center_lat = 0.0
PROJ_STRING = f"+proj=laea +lat_0={pacific_center_lat} +lon_0={pacific_center_lon} +datum=WGS84 +units=m +no_defs"

eq_proj = eq_in_pacific.to_crs(PROJ_STRING)
pa_boundaries_proj = pa_boundaries.to_crs(PROJ_STRING)

boundary_union = pa_boundaries_proj.geometry.unary_union
print(f"Boundary union type: {boundary_union.geom_type}")

# ── 7. Compute distances ──────────────────────────────────────────────────────
distances = eq_proj.geometry.distance(boundary_union)
eq_proj = eq_proj.copy()
eq_proj["distance_m"] = distances
eq_proj["distance_km"] = distances / 1000.0

print(f"\nDistance stats:")
print(f"  Min: {eq_proj['distance_km'].min():.2f} km")
print(f"  Max: {eq_proj['distance_km'].max():.2f} km")
print(f"  Mean: {eq_proj['distance_km'].mean():.2f} km")

# ── 8. Find the farthest earthquake ──────────────────────────────────────────
idx_max = eq_proj["distance_km"].idxmax()
farthest = eq_proj.loc[idx_max]

print(f"\nFarthest earthquake from Pacific boundary:")
print(f"  ID: {farthest['id']}")
print(f"  Place: {farthest['place']}")
print(f"  Time: {farthest['time']}")
print(f"  Magnitude: {farthest['magnitude']}")
print(f"  Lat/Lon: {farthest['latitude']}, {farthest['longitude']}")
print(f"  Distance: {farthest['distance_km']:.2f} km")

# ── 9. Write output ─────────────────────────────────────────────────────────
result = {
    "id": farthest["id"],
    "place": farthest["place"],
    "time": farthest["time"],
    "magnitude": float(farthest["magnitude"]),
    "latitude": float(farthest["latitude"]),
    "longitude": float(farthest["longitude"]),
    "distance_km": round(float(farthest["distance_km"]), 2)
}

with open("/root/answer.json", "w") as f:
    json.dump(result, f, indent=2)

print("\nResult written to /root/answer.json")
print(json.dumps(result, indent=2))
```

## Key Implementation Notes

- **Always use `PB2002_boundaries.json`** filtered for PA, never the plate polygon's `.boundary`.
- **Plate code is `"PA"`** — filter `plates` with `Code == "PA"` (inspect actual column name first).
- **Boundary columns** are typically `PlateA`/`PlateB` — filter `(PlateA == "PA") | (PlateB == "PA")`.
- **Pacific-centered projection** (LAEA at lon_0=180) avoids antimeridian distortion.
- **Use `sjoin` with `predicate="within"`** for point-in-polygon; fall back to manual `.contains()` if needed.
- **Distance is in meters** from `.distance()` — divide by 1000 for km.