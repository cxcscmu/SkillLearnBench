---
name: plate-tectonics-pb2002-parsing
description: Specific knowledge of the PB2002 (Bird, 2002) dataset structure for identifying the Pacific plate.
---

The "PB2002" dataset (by Peter Bird) is a standard dataset for tectonic plate boundaries. 
- `PB2002_plates.json`: Contains polygons. The Pacific plate is typically identified by the code **'PA'** in the `PlateName` or `Code` field.
- `PB2002_boundaries.json`: Contains LineStrings. To find the boundary of the Pacific plate, you can either filter boundaries that touch the Pacific plate polygon or simply extract the boundary of the 'PA' polygon itself using the `.boundary` attribute in GeoPandas.

When calculating the distance "to the Pacific plate boundary", it refers to the distance to the perimeter of the Pacific plate polygon.