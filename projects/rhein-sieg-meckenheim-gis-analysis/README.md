# GIS-Based Land Use, Forest Change, and Residential Development Suitability Analysis

**Study Area:** Rhein-Sieg-Kreis and Meckenheim, North Rhine-Westphalia, Germany  
**Project Area:** Urban Analytics with GIS  
**Author:** Emmanuel Frimpong Kissi

## Project Overview

This project applies Geographic Information Systems (GIS) to explore land use, forest-area change, and potential locations for future residential development in the Rhein-Sieg District of Germany.

The project combines spatial mapping, land-use analysis, historical change assessment, and multi-criteria suitability analysis. It aims to demonstrate how GIS can support land-use planning and evidence-based decision-making.

The analysis covers three main components:

- **Land-use mapping:** Visualisation of land-use and land-cover patterns across the Rhein-Sieg District.
- **Forest-area change:** Examination of changes in forest areas between 1845 and 2018.
- **Residential development suitability:** Identification of two potential locations for new residential development in Meckenheim using environmental constraints and accessibility criteria.

## Project Objectives

- Map and visualise land-use patterns across the Rhein-Sieg District.
- Examine long-term changes in forest areas.
- Identify potentially suitable locations for residential development in Meckenheim.
- Apply GIS-based spatial analysis to support land-use planning.
- Communicate spatial results through clear, map-based outputs.

## Map Outputs

The following maps present the main outputs of the project. The images are included so that visitors can explore the results directly from this repository.

### 1. Land-Use Plan of the Rhein-Sieg District

This map presents the spatial distribution of land-use and land-cover categories across the Rhein-Sieg District. It provides an overview of the landscape and the different land-cover types within the study area.

![Land-use plan of the Rhein-Sieg District](images/land-use-plan-rhein-sieg.png)

### 2. Forest-Area Change in the Rhein-Sieg District, 1845–2018

This map illustrates the historical change in forest areas across the Rhein-Sieg District between 1845 and 2018. The analysis provides a spatial perspective on long-term landscape transformation.

![Forest-area change in the Rhein-Sieg District, 1845–2018](images/forest-area-change-rhein-sieg.png)

### 3. Potential Residential Development Site 1 — Meckenheim

This map shows the first potential location identified through the residential development suitability analysis. The assessment considers spatial constraints and accessibility requirements to identify areas that may warrant further investigation.

![Potential residential development location 1 in Meckenheim](images/meckenheim-suitable-location-1.png)

### 4. Potential Residential Development Site 2 — Meckenheim

This map presents the second potential location identified by the suitability analysis. Together, the two candidate locations demonstrate how GIS-based criteria can help screen land for possible future residential development.

![Potential residential development location 2 in Meckenheim](images/meckenheim-suitable-location-2.png)

## Methodology

### Land-Use Mapping

Land-use and land-cover information was used to represent the spatial structure of the Rhein-Sieg District. The mapping provides a basis for understanding the distribution of different landscape categories.

### Forest-Area Change Analysis

Historical forest information was examined to assess changes in forest areas between 1845 and 2018. Comparing the historical datasets provides insight into the spatial development of forest cover over time.

### Residential Development Suitability Analysis

A GIS-based multi-criteria analysis (MCA) was used to identify two potential residential development locations in Meckenheim.

The suitability assessment considered the following types of criteria:

- **Environmental and land-use constraints:** Protected areas, forests, existing settlements, and traffic areas.
- **Industrial-area separation:** A 500-metre buffer around industrial areas.
- **Public transport accessibility:** Access to a railway station within a 40-minute e-bike travel time.
- **Kindergarten accessibility:** Access within a 15-minute walking time.
- **Supermarket accessibility:** Access within a 15-minute driving time.
- **Proximity to existing residential areas:** Candidate areas within 100 metres of existing residential zones.

The criteria were combined to screen for locations that met the specified requirements. Two potential locations were identified for further consideration.

*These thresholds represent the criteria used in the analysis; they should not be interpreted as universal planning standards.*

## Tools and Data

The project is based on GIS methods and spatial datasets documented in the accompanying coursework report.

Key data and analytical components include:

- **CORINE Land Cover (CLC5, 2018):** Land-cover mapping.
- **Historical forest datasets:** Forest-area comparison for 1845–2018.
- **OpenStreetMap data:** Transport networks and essential services for accessibility analysis.
- **GIS spatial analysis:** Land-use mapping, buffering, accessibility assessment, and multi-criteria suitability analysis.

The exact software versions and any additional datasets can be documented here if required.

## Key Outputs

- Land-use map of the Rhein-Sieg District.
- Historical forest-area change map for 1845–2018.
- Two potential residential development locations in Meckenheim.
- A GIS-based workflow combining environmental constraints and accessibility criteria.

## Limitations

- The results depend on the completeness, accuracy, and dates of the spatial datasets used.
- Accessibility estimates depend on the network data and travel-time assumptions.
- The identified locations are **potentially suitable areas under the criteria applied**, not confirmed or officially approved development sites.
- Further investigation would be needed to assess land ownership, detailed site conditions, planning regulations, infrastructure capacity, and other site-specific requirements.

## Repository Structure

A suggested structure for organising the project is:

```text
rhein-sieg-meckenheim-gis-analysis/
├── README.md
├── images/
│   ├── land-use-plan-rhein-sieg.png
│   ├── forest-area-change-rhein-sieg.png
│   ├── meckenheim-suitable-location-1.png
│   └── meckenheim-suitable-location-2.png
├── data/                  # Optional: shareable datasets only
├── scripts/               # Optional: GIS scripts or notebooks
└── report/                # Optional: project report
```

## Conclusion

This project demonstrates how GIS can be used to investigate land-use patterns, assess long-term forest-area change, and identify potential locations for residential development.

By combining spatial data, environmental constraints, and accessibility criteria, the analysis illustrates the value of GIS as a decision-support tool for urban and regional planning.

---

**Author:** Emmanuel Frimpong Kissi  
**Focus Areas:** Geographic Information Systems (GIS), Spatial Analysis, Land-Use Planning, Remote Sensing, and Accessibility Analysis

