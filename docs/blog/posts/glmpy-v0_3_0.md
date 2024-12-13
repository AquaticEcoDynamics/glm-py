---
draft: false 
date: 2024-12-13
authors:
  - gknight
categories:
  - Releases
---

# glm-py `0.3.0`

**Key changes from the latest release.**

glm-py `0.3.0` adds a `plots` module for visualising GLM's `lake.csv` and 
`output.nc` files with Matplotlib.

<!-- more -->

## What's changed

- Added a `plots` module for visualising GLM's output files with Matplotlib
  - `LakePlotter` class for plotting the `lake.csv` file
  - `NCProfile` class for plotting a timeseries profile of variables in the 
    `output.nc` file
  - `matplotlib` and `netcdf4` dependencies added
  - Added a how-to documentation page for the `plots` module
- Added a `example_sims.sparkling` sub-module for running the Sparkling Lake
simulation
  - `load_nml` function for returning a dictionary of the Sparkling NML
  - `load_bcs` function for returning a pandas dataframe of the boundary 
  condition data
  - `run_sim` function for running the Sparkling simulation
- Added `InvertedTruncatedPyramid` class to the `dimensions` module
  - Deprecation warning added to `InvertedTruncatedSquarePyramid`