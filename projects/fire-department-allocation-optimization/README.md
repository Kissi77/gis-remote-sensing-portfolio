# Fire Department Allocation Optimization

**GIS · Spatial Optimisation · Integer Linear Programming · Java · Gurobi**

## Overview

This completed academic project investigated the spatial optimisation of fire department resources in Bonn, Germany. The objective was to determine which existing fire stations should remain active and how demand locations should be assigned to the selected stations, with the aim of minimising travel or response distance.

The project integrated spatial data and integer linear programming to examine station-selection and demand-allocation decisions under different operational constraints.

## Objectives

- Determine which existing fire stations should remain active.
- Allocate demand locations to selected stations.
- Minimise travel or response distance subject to model constraints.
- Assess how station capacity and maximum allowable distance influence the optimisation solution.
- Examine changes in station selection, demand coverage, allocation patterns, and solution feasibility under alternative scenarios.
- Visualise the resulting station selections and demand assignments.

## Methodology

The project followed a GIS and mathematical optimisation workflow.

1. **Spatial data preparation:** Prepared project-provided spatial data for the allocation analysis.
2. **Optimisation formulation:** Represented station selection and demand allocation as an integer linear programming problem.
3. **Constraint definition:** Incorporated station-capacity limits and maximum allowable distances.
4. **Optimisation:** Used Java and Gurobi Optimizer to solve the allocation problem.
5. **Sensitivity analysis:** Varied station capacity and maximum allowable distance to examine how changes in these parameters affected the solutions.
6. **Spatial visualisation:** Produced maps showing selected fire stations and their assigned demand locations.

## Sensitivity Analysis

Sensitivity tests investigated how changes to two operational constraints influenced the optimisation results:

- **Station capacity:** Examined how changes in capacity affected the number of stations selected, the number or proportion of demand locations served, demand-to-station assignments, and solution feasibility.
- **Maximum allowable distance:** Examined how changing the permitted distance affected station selection, demand coverage, allocation patterns, and the feasibility of finding a solution.

This analysis provided a way to evaluate the model's response to different planning assumptions rather than relying on a single parameter configuration.

*The tested parameter values and quantitative comparisons between scenarios will be documented after verification against the original project materials.*

## Tools and Technologies

- **GIS:** Spatial data preparation and mapping
- **Optimisation:** Integer linear programming
- **Programming:** Java
- **Solver:** Gurobi Optimizer

## Outputs

The project produced maps and visualisations showing selected fire stations and their assigned demand locations.

The sensitivity analysis also examined changes in station selection, demand coverage, assignment patterns, and the feasibility of solutions under different capacity and distance settings.

Selected visual outputs may be added to this repository after review and clearance for public sharing.

## Potential Applications

Spatial optimisation can support emergency service planning by helping decision-makers evaluate existing facility configurations, allocate demand to available resources, and understand the implications of different capacity and distance requirements.

Sensitivity analysis is particularly useful for identifying how planning assumptions affect proposed allocations and whether a solution remains feasible under alternative constraints.

The practical interpretation of the results depends on the quality of the input data, the model assumptions, and how well the optimisation constraints represent real operational conditions.

## Limitations

The results depend on the spatial data, mathematical formulation, and constraints used in the academic model. The model's distance measure should not automatically be interpreted as actual emergency response time unless travel-time data and relevant operational factors were explicitly incorporated.

Quantitative performance measures and scenario comparisons have not been included here because the original results have not yet been verified.

## Project Status

**Completed academic project**

This page provides a high-level overview of the project. Further technical details and selected visual outputs will be added after verification and clearance for public sharing.
