As a geospatial analyst with expertise in plate tectonics and earthquake analysis, your objective is to identify the specific 2024 seismic event located within the **Africa plate** that occurred at the maximum distance from its own tectonic boundaries. You must process the earthquake data provided in `/root/earthquakes_2024.json` against the tectonic framework defined in `/root/PB2002_plates.json` and `/root/PB2002_boundaries.json`.

The final result must be exported to `/root/answer.json` as a single JSON object containing the following fields: 
- `id`: The unique earthquake identifier.
- `place`: The descriptive string for the earthquake location.
- `time`: The timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
- `magnitude`: The numeric magnitude of the event.
- `latitude`: The epicenter latitude.
- `longitude`: The epicenter longitude.
- `distance_km`: The calculated largest distance to the Africa plate boundary in kilometers, rounded to exactly 2 decimal places.