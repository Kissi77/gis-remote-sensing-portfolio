# Multisite Satellite Analysis of Data-Centre Developments in Malaysia

## Project Overview

This project uses Geographic Information Systems (GIS) and satellite remote sensing to examine land-surface temperature (LST), vegetation patterns, and built-up surface characteristics around data-centre developments in Malaysia.

The analysis combines satellite-derived environmental indicators with spatial distance-band analysis, pre-development and post-development comparisons, and a Before–After–Control–Impact (BACI) framework using matched control locations where sufficient observations are available.

Two complementary spatial approaches are investigated: an individual-site analysis of 21 data centres and a cluster-based analysis that groups nearby developments into four clusters while retaining nine standalone sites. These approaches help examine environmental patterns at individual locations and account for the proximity of neighbouring developments.

## Research Objectives

- Examine land-surface temperature (LST), vegetation conditions (NDVI), and built-up surface patterns (NDBI) around data-centre developments.
- Assess environmental indicator patterns across distance bands around 21 individual data-centre sites.
- Compare pre-development and post-development indicator values.
- Evaluate an alternative spatial approach that groups nearby data centres into four clusters and analyses nine standalone sites.
- Compare changes at eligible impact units with changes at matched control locations using BACI analysis.
- Discuss the findings, data limitations, and uncertainty in attributing observed changes to data-centre development.

## Study Area and Data

The study focuses on data-centre developments in Malaysia. Satellite-derived observations are used to characterise environmental conditions over the available study period, subject to imagery availability and quality.

### Environmental Indicators

- **Land Surface Temperature (LST):** Characterises the thermal conditions of the land surface.
- **Normalized Difference Vegetation Index (NDVI):** Indicates the presence and relative greenness of vegetation.
- **Normalized Difference Built-up Index (NDBI):** Helps characterise built-up surface patterns.

These indicators describe different aspects of the surrounding landscape. They are complementary measures and should not be interpreted as direct measurements of air temperature, human thermal exposure, or building density.

## Methodology

The workflow combines satellite-image processing, spatial analysis, and statistical comparisons.

1. Prepare satellite imagery for the relevant study periods.
2. Apply cloud and quality masking to reduce the influence of unsuitable observations.
3. Generate seasonal composites from available satellite observations.
4. Derive or compile LST, NDVI, and NDBI for suitable periods and locations.
5. Summarise the indicators across the specified distance bands.
6. Compare eligible pre-development and post-development observations.
7. Group nearby data centres into clusters for a complementary spatial analysis.
8. Conduct BACI comparisons between eligible impact units and matched controls.
9. Interpret estimates alongside sample sizes, uncertainty, and limitations in satellite data availability.

## Spatial Analysis Framework

### Approach 1: Individual Analysis of 21 Data-Centre Sites

The first approach treats the 21 data-centre sites individually. Environmental indicators are summarised within five distance rings around each site:

- 0–500 m
- 500 m–1 km
- 1–2 km
- 2–3 km
- 3–5 km

This approach examines spatial variation in environmental indicators with distance from individual data-centre locations. Annual dry-season trajectories provide a temporal overview, while pre–post comparisons assess changes across the five rings.

### Annual Dry-Season Trajectories

The annual trajectories show how LST, NDVI, and NDBI vary over the study period across the individual-site analysis.

![Annual dry-season trajectories of LST, NDVI, and NDBI across 21 individual data-centre sites](figures/annual-dry-season-trajectories.png)

*Figure 1. Annual dry-season trajectories of LST, NDVI, and NDBI across the individual data-centre sites. Temporal patterns may reflect development activity as well as climate variability, observation availability, and other landscape changes.*

### Pre–Post Changes Across Five Distance Rings

This analysis compares environmental indicator values before and after development across the five individual-site distance rings.

![Pre-post environmental changes across five distance rings around individual data-centre sites](figures/individual-site-pre-post-distance-bands.png)

*Figure 2. Pre–post changes across the five distance rings around individual data-centre sites.*

## Approach 2: Cluster-Based and Standalone-Site Analysis

The second approach accounts for the proximity of neighbouring data centres. Four groups of nearby data centres are treated as clusters, while nine additional data centres are analysed as standalone sites.

For each cluster, overlapping 500 m buffers were dissolved to represent the grouped developments, and a centroid was calculated from the dissolved geometry. Spatial validation showed that some data centres within a cluster fell outside a 500 m buffer around the cluster centroid. The innermost cluster-analysis buffer was therefore increased to 1 km to encompass all data centres belonging to each cluster.

The cluster-based analysis uses four distance bands:

- 0–1 km
- 1–2 km
- 2–3 km
- 3–4 km

These bands differ from the five rings used in the individual-site analysis. The two approaches also use different spatial reference units: individual data-centre locations in the first approach and cluster centroids or standalone-site locations in the second. Their results are therefore complementary rather than directly equivalent measurements at identical distances.

### Cluster-Based Annual Trajectories

*Figure to be added.*

This figure will present annual dry-season trajectories for LST, NDVI, and NDBI across the four clusters and nine standalone sites.

### Pre–Post Changes Across Four Cluster-Based Distance Bands

*Figure to be added.*

This figure will present pre–post environmental changes across the cluster-based bands of 0–1 km, 1–2 km, 2–3 km, and 3–4 km.

## Before–After–Control–Impact (BACI) Analysis

BACI analysis compares changes over time at impact units with changes over the same period at matched control locations. This helps account for temporal changes that may also occur outside the impact areas.

The analysis is conducted for eligible clusters and standalone sites, subject to the availability of sufficiently valid satellite observations. The resulting estimates should be interpreted alongside their confidence intervals, sample sizes, and statistical uncertainty.

### Impact and Matched-Control Trajectories

*Figure to be added.*

This figure will compare LST trajectories for impact units and matched controls. Additional indicators will be presented where supported by the available data.

## Limitations and Interpretation

- **Satellite observation availability:** Persistent cloud cover in Malaysia can limit valid observations and reduce the number of sites available for individual indicator analyses.
- **Unequal data availability:** Sample sizes may differ between LST, NDVI, and NDBI because their valid observation periods and quality requirements can differ.
- **Climate variability:** Interannual changes in rainfall, regional temperature, and other climatic conditions may contribute to observed environmental patterns.
- **Development attribution:** Pre–post changes alone do not establish causality. BACI analysis provides a comparative framework, but its strength depends on control suitability, temporal comparability, and data availability.
- **Spatial-unit differences:** The individual-site and cluster-based analyses use different spatial units and distance-band boundaries and should not be treated as directly interchangeable.
- **Indicator interpretation:** LST, NDVI, and NDBI represent surface thermal conditions, vegetation greenness, and built-up surface patterns, respectively. They do not directly measure air temperature or human health outcomes.

## Tools and Technologies

- Google Earth Engine
- Python
- R
- GIS and remote-sensing workflows
- Satellite-image processing and quality masking
- Spatial buffering and distance-band analysis
- Statistical pre–post and BACI comparisons
- Data visualisation

## Reproducibility and Data Availability

This repository presents selected figures, methods, and documentation from the research project. Source data, processing scripts, and detailed results may be added where sharing permissions and data availability allow.

## Summary

This project provides a multisite assessment of environmental patterns around data-centre developments in Malaysia using satellite remote sensing and GIS. By combining individual-site analysis, cluster-based analysis, and matched-control comparisons, it examines observed changes in surface temperature, vegetation, and built-up surface patterns while recognising the limitations of observational satellite data.

and figures will be added once the selected outputs are verified and approved for sharing.*
