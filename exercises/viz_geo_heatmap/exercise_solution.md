# Exercise Card: Viz 4 - The Geographic Heatmap (The Global View)

## Title & Problem Statement
**The Global View: Mapping Sales Data Geographically with Folium**

Tables and bar charts can show *what* is selling, but maps show *where*. Geographic visualization is one of the most impactful ways to present sales, logistics, or demographic data because it immediately connects numbers to real-world locations. In this exercise, you will use **Folium** — a Python library that generates interactive Leaflet.js maps — to create a heatmap and marker visualization of global sales data. The output is a standalone HTML file with full pan, zoom, and click interactivity.

## Difficulty & Estimated Time
*   **Difficulty:** Intermediate-Advanced (Geospatial Visualization)
*   **Estimated Time:** 35-45 Minutes

## Required Libraries
*   `pandas`: Loading and aggregating the sales data by city.
*   `folium`: The core library that generates interactive Leaflet.js maps from Python.
*   `folium.plugins`: Specifically `HeatMap` for the heat layer and `MarkerCluster` for grouped markers.

## Didactic Step-by-Step

### 1. Data Preparation
**Concept:** Geographic visualization requires latitude/longitude coordinates.
*   **Action:** Load the sales CSV. The dataset includes city names with pre-assigned lat/lon coordinates. Aggregate revenue and order count per city.

### 2. Base Map Creation
**Concept:** Folium creates a base map tile (like Google Maps) that you add layers to.
*   **Action:** Initialize a `folium.Map()` centered on a reasonable location (e.g., lat=20, lon=0 for a world view) with a zoom level of 2. Choose a tile style (`CartoDB dark_matter` for a striking dark theme).

### 3. Heatmap Layer
**Concept:** A heatmap shows data density/intensity as a color gradient overlaid on the map.
*   **Action:** Create a list of `[lat, lon, weight]` tuples where weight = revenue. Add this to the map using `HeatMap()` from `folium.plugins`.

### 4. Marker Layer
**Concept:** Markers are clickable points on the map with popups showing details.
*   **Action:** For each city, add a `CircleMarker` with radius proportional to revenue. Attach a `Popup` with HTML content showing city name, total revenue, orders, and top product.

### 5. Layer Control & Finishing
**Concept:** Layer control lets the user toggle heatmap and markers on/off.
*   **Action:** Add `folium.LayerControl()` to the map. Save the entire map as an HTML file.

## Tips for Coding and Vibe-Coding

1.  **Tile Styles transform the mood:** Try `"CartoDB dark_matter"` for a dramatic dark look, `"Stamen Toner"` for a clean black-and-white, or `"OpenStreetMap"` for the classic look.
2.  **Normalize your heatmap weights:** If one city has 100x more revenue, the heatmap will only show that one city. Consider using `log()` or `min-max scaling` to balance the intensity.
3.  **HTML in popups:** Folium popups accept raw HTML strings. Use `<b>`, `<br>`, and even `<table>` tags to format beautiful popup cards.
4.  **Circle size scaling:** Don't use raw revenue as the radius — it'll be too large. Divide by a constant or use a square root scale: `radius = (revenue / max_revenue) * 30`.
5.  **Save and share:** The `.html` output includes all the JavaScript. You can email it, drop it in SharePoint, or embed it in a web page. No Python needed to view it.

## Copilot Master Prompt
*You can use this prompt to generate the solution code:*

> "I have a pandas DataFrame with columns: City, Country, Latitude, Longitude, Revenue, Order_Count, Top_Product.
> Using the Folium library, create an interactive map saved as HTML that includes:
> 1. A base map using CartoDB dark_matter tiles centered at lat=20, lon=0 with zoom=2.
> 2. A HeatMap layer using latitude, longitude, and revenue as weight.
> 3. Circle markers for each city sized proportionally to revenue, with popup HTML showing city details.
> 4. A LayerControl to toggle between heatmap and markers.
> Make it look professional and save as 'sales_heatmap.html'."
