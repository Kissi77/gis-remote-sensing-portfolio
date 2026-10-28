# Bonn Interactive Alternative Route Finder

An interactive GIS and web-mapping application for exploring driving routes in Bonn, Germany.

## Project overview

This project allows users to select an origin and destination on an interactive map, calculate the shortest-distance driving route, and explore up to two alternative routes.

## Key features

- Interactive map-based origin and destination selection.
- Shortest-distance driving route calculation.
- Up to two alternative routes.
- Colour-coded route visualisation following the road network.
- Route-distance and detour comparisons.

## Tools and technologies

- Python
- OpenStreetMap
- OSMnx
- NetworkX
- Streamlit
- Folium

## Interactive demonstration

*Live demo link will be added after deployment.*

## Methodology

The application uses a driving-road network and road-network distance to calculate the shortest route. Alternative routes are filtered by their distance relative to the shortest route and the amount of road-network overlap.

## Limitations

The application does not currently account for live traffic, travel-time optimization, road closures, or accessibility requirements. The number of alternatives depends on the selected locations and filtering criteria.

## Data attribution

Road-network data is obtained from OpenStreetMap. See the [OpenStreetMap copyright and attribution page](https://www.openstreetmap.org/copyright).

