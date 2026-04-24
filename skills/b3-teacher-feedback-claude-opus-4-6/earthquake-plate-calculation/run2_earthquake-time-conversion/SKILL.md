---
name: earthquake-time-conversion
description: Converting earthquake timestamps from USGS GeoJSON format (epoch milliseconds) to ISO 8601 format for output.
---

## USGS Earthquake Time Format

USGS earthquake GeoJSON data stores time as **epoch milliseconds** (integer). To convert to ISO 8601:

```python
import pandas as pd

# If time is in milliseconds since epoch
time_ms = 1704067200000  # example
time_iso = pd.to_datetime(time_ms, unit='ms', utc=True).strftime('%Y-%m-%dT%H:%M:%SZ')
```

### Handling different possible formats

```python
def convert_time(time_val):
    """Convert USGS earthquake time to ISO 8601."""
    if isinstance(time_val, (int, float)):
        return pd.to_datetime(time_val, unit='ms', utc=True).strftime('%Y-%m-%dT%H:%M:%SZ')
    elif isinstance(time_val, str):
        return pd.to_datetime(time_val, utc=True).strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        return pd.to_datetime(time_val, utc=True).strftime('%Y-%m-%dT%H:%M:%SZ')
```

The output format must be: `YYYY-MM-DDTHH:MM:SSZ`