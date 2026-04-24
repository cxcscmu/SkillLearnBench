Acting as a geospatial analyst with expertise in plate tectonics, your mission is to identify the specific 2024 seismic event that occurred at the absolute minimum distance to any global plate boundary. Using the seismic records in `/root/earthquakes_2024.json` and the tectonic framework defined in `/root/PB2002_boundaries.json`, you must determine which earthquake epicenter is geographically nearest to a recorded plate margin on a global scale.

The final result must be exported to `/root/answer.json` as a single JSON object containing the following fields: 
- `id`: The unique earthquake identifier.
- `place`: The descriptive string for the earthquake location.
- `time`: The timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
- `magnitude`: The numeric magnitude of the event.
- `latitude`: The epicenter latitude.
- `longitude`: The epicenter longitude.
- `distance_km`: The calculated largest distance to the Africa plate boundary in kilometers, rounded to exactly 2 decimal places.