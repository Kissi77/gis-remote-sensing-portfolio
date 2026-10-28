# GIS-Based Multi-Criteria Analysis for Residential Site Selection in Bonn, Germany

**QGIS · GIS Analysis · Multi-Criteria Analysis · Spatial Decision Support · Accessibility Analysis**

## Project Overview

This academic project applied Geographic Information Systems (GIS) to identify potential areas for residential development in Bonn, Germany. Using QGIS, OpenStreetMap data, and OpenRouteService, the analysis combined spatial exclusion criteria, proximity analysis, and travel-time accessibility assessment to identify locations that met the specified residential development requirements.

The analysis considered environmental constraints, proximity to existing residential areas, access to railway stations, and accessibility to essential local infrastructure. The final output was a suitability map highlighting two potential areas for residential development.

## Project Objectives

- Identify potential residential development areas using GIS-based multi-criteria analysis.
- Exclude environmentally protected areas, forests, existing settlements, and traffic areas.
- Assess proximity to existing residential areas and industrial zones.
- Evaluate access to railway stations using cycling travel-time analysis.
- Assess accessibility to kindergartens and supermarkets.
- Produce a suitability map showing the selected potential development areas.

## Study Area

**Bonn, North Rhine-Westphalia, Germany**

The analysis used geographic datasets covering Bonn Municipality to examine potential locations for new residential development.

## Methodology

### 1. Spatial Data Preparation

Relevant spatial datasets were prepared in QGIS, including administrative boundaries, protected areas, forests, existing settlements, traffic areas, industrial areas, and open land. OpenStreetMap data were used to identify railway stations, kindergartens, and supermarkets.

### 2. Environmental and Land-Use Constraints

Spatial exclusion operations were used to remove areas that did not meet the development requirements. These included:

- Protected areas
- Forest areas
- Existing settlements
- Traffic areas
- Areas within 500 metres of industrial areas

### 3. Proximity to Existing Residential Areas

A 100-metre buffer was created around existing residential areas. Buffer and intersection operations were then used to identify potential development areas close to existing residential zones while satisfying the specified exclusion criteria.

### 4. Railway Accessibility

Railway stations were identified using OpenStreetMap data. OpenRouteService tools in QGIS were used to generate cycling accessibility areas representing locations reachable within 40 minutes by e-bike.

The resulting accessibility areas were used to identify candidate development locations meeting the railway-accessibility requirement.

### 5. Access to Essential Infrastructure

Accessibility to two types of local infrastructure was assessed:

- **Kindergartens:** locations reachable within 15 minutes on foot.
- **Supermarkets:** locations reachable within 15 minutes by car.

Travel-time isochrones and spatial intersection operations were used to identify candidate areas with access to these facilities.

### 6. Final Site Selection and Mapping

The spatial analysis outputs were combined through successive spatial operations to identify candidate areas satisfying the specified criteria. Two potential residential development areas were selected and presented on a final suitability map.

## Tools and Technologies

- **QGIS:** Spatial data management, geoprocessing, analysis, and cartographic visualisation.
- **OpenStreetMap:** Geographic data for transport and local amenities.
- **QuickOSM:** Extraction of relevant OpenStreetMap features.
- **OpenRouteService:** Travel-time isochrones and accessibility analysis.
- **Spatial analysis techniques:** Buffering, clipping, difference, intersection, spatial selection, and exclusion analysis.

## Key Output

The main deliverable was a residential site suitability map highlighting two potential development areas in Bonn that met the criteria considered in the analysis.

The project demonstrates how GIS can integrate environmental constraints, land-use information, proximity relationships, and travel-time accessibility to support spatial planning decisions.

## Limitations

The findings depend on the geographic datasets, criteria, and accessibility assumptions used in the original analysis. The identified locations represent potential sites based on the specified criteria; they should not be interpreted as definitive development recommendations without further field verification, planning review, and assessment of additional factors.

## Project Status

**Completed academic project**

This repository page provides a summary of the project workflow and methods. Original datasets, code, and map outputs will be considered for publication only after confirming that they are cleared for public sharing.
