---
name: itinerary-content-requirements
description: Guidelines for selecting database-compliant restaurants, accommodations, and attractions based on specific user constraints like budget, pets, and cuisine.
---

1. **Data Sourcing**: Only use real-world data from the provided database files (e.g., `restaurants/clean_restaurant_2022.csv`, `accommodations/clean_accommodations_2022.csv`). Do not use internal knowledge or hallucinations.
2. **Pet-Friendly Accommodations**: Filter the accommodations database specifically for entries labeled as pet-friendly. The selected lodging must explicitly support pets for every night of the trip.
3. **Cuisine Alignment**: Match the `breakfast`, `lunch`, and `dinner` fields with the user's preferred cuisines: American, Mediterranean, Chinese, and Italian. If a specific cuisine is unavailable in a city, default to a high-rated American option from the database.
4. **Attraction Format**: List attractions as a string, separated by semicolons, and ensure the string ends with a semicolon (e.g., "Attraction A;Attraction B;"). 
5. **Daily Engagement**: Ensure a minimum of one attraction is listed for every single day (Day 1 through Day 7). Use city-specific data to ensure the attraction is relevant to the `current_city` or route.