---
name: bundled-dataset-search-tool
description: invoke this skill when you need to perform database search for travel planning. This skill provides some useful pre-packaged tools to look up accommodations, attractions, cities, driving distance, flights, and restaurants from the bundled dataset.
---

# Overview

This skill provides six tools for searching the bundled dataset, always first use these tool scripts than writing code by yourself. 

# Installation

**before using the tools, please install:**

```bash
pip install pandas numpy requests
```

## Tool 1 :Search Accommodations

Find accommodations for a specific city. The bundled script is located at scripts/search_accommodations.py. An Example:

```python
from search_accommodations import Accommodations

acc = Accommodations()
result = acc.run("Seattle")
print(result)
```


## Tool 2: Search Attractions

Query attractions for a given city.  The bundled script is located at scripts/search_attractions.py. An Example:

```python
from search_attractions import Attractions

attractions = Attractions()
print(attractions.run("New York"))
```

## Tool 3: Search Cities

Map states to their cities from the background text file.  The bundled script is located at scripts/search_cities.py. An Example:

```python
from search_cities import Cities

cities = Cities()
print(cities.run("California"))
```
## Tool 4: Search Driving Distance

Look up distance/duration between an origin and destination. The bundled script is located at scripts/search_driving_distance.py. An Example:

```python
from search_driving_distance import GoogleDistanceMatrix

matrix = GoogleDistanceMatrix()
print(matrix.run("Seattle", "Portland", mode="driving"))
```

## Tool 5: Search Flights

Filter the cleaned flights CSV for specific routes and dates. The bundled script is located at scripts/search_flights.py. An Example:

```python
from search_flights import Flights

flights = Flights()
print(flights.run("New York", "Los Angeles", "2022-01-15"))
```

## Tool 6: Search Restaurants

Query restaurants for a given city. The bundled script is located at scripts/search_restaurants.py. An example:
```python
from search_restaurants import Restaurants

restaurants = Restaurants()
print(restaurants.run("San Francisco"))
```