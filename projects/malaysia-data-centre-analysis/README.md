# Multisite Satellite Analysis of Data-Centre Developments in Malaysia

## Project Overview

This project investigates spatial patterns in land-surface temperature, vegetation, and built-up surfaces around multiple data-centre developments in Malaysia using satellite remote sensing and geospatial analysis.

The research examines how environmental indicators vary with distance from development sites and compares selected pre-development and post-development observations. Conventional urban and planned eco-city locations provide additional descriptive context.

## Research Objectives

- Examine land-surface temperature (LST) patterns around multiple data-centre sites.
- Assess vegetation patterns using the Normalized Difference Vegetation Index (NDVI).
- Examine built-up surface patterns using the Normalized Difference Built-up Index (NDBI).
- Compare environmental indicators across distance bands.
- Evaluate pre-development and post-development changes using satellite-derived indicators.
- Apply Before–After–Control–Impact (BACI) analysis to selected sites with matched controls.

## Data and Tools

- **Satellite data:** Landsat imagery and Sentinel imagery where suitable observations are available.
- **Processing:** Google Earth Engine.
- **Programming and statistical analysis:** Python and R.
- **Geospatial analysis:** GIS, distance-based buffers, seasonal composites, and matched-control comparisons.

## Methodology

1. Prepare satellite observations and apply cloud and quality masking.
2. Generate seasonal image composites for the relevant study periods.
3. Derive land-surface temperature and calculate NDVI and NDBI where the required imagery is available.
4. Summarise indicators across distance bands around the study sites.
5. Compare selected pre-development and post-development periods.
6. Conduct BACI analysis for eligible impact and matched-control units.
7. Interpret the results while considering data availability, environmental variability, and limitations of causal attribution.

## Results and Visualisations

### Annual Dry-Season Environmental Trajectories

The figure below presents annual dry-season trajectories for land-surface temperature (LST), the Normalized Difference Vegetation Index (NDVI), and the Normalized Difference Built-up Index (NDBI) across the study sites. Examining these indicators together helps characterise changes in surface thermal conditions, vegetation, and built-up surface patterns over the study period.

![Annual dry-season trajectories of LST, NDVI, and NDBI](figures/annual-dry-season-trajectories.png)

*Figure 1. Annual dry-season trajectories of LST, NDVI, and NDBI across the study sites in Malaysia. Interpretations should account for interannual climate variability, data availability, and differences in development timing.*

Additional figures will document pre–post changes across distance bands and comparisons between data-centre impact sites and matched controls.


Planned outputs include:

- Land-surface temperature comparisons.
- NDVI and NDBI change visualisations.
- Distance-band analysis.
- Pre-development and post-development comparisons.
- BACI estimates with confidence intervals.

## Limitations

Satellite observations can be limited by cloud cover, particularly in tropical environments. The number of eligible observations may therefore vary among sites and indicators. Changes observed after development should not automatically be attributed to data-centre development, because regional climate variability, rainfall, surrounding construction, and other land-use changes may also contribute.

## Research Contribution

The project demonstrates the application of satellite remote sensing, geospatial processing, spatial statistics, and matched-control methods to environmental monitoring around data-centre developments.

*This page describes the research workflow. Numerical findings and figures will be added once the selected outputs are verified and approved for sharing.*
