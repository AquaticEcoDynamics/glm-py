# Release Notes

## glm-py

### 0.4.0 <small>(17 January, 2025)</small> { id="0.4.0" }

- Added `restart_variables` to `InitProfilesBlock`, 
`NMLReader._default_converters`, and `NMLWriter._default_converters`
- Added `subm_elev` to `InflowBlock`, 
`NMLReader._default_converters`, and `NMLWriter._default_converters`
- Added `list_len` parameter to `NMLWriter.write_nml_list` which inserts line 
breaks to the comma-separated output after a specified number of items. 
`list_len` parameter also added to `NMLWriter` and `GLMNML`.
- Removed `NMLWriter.write_nml_array` and `NMLReader.read_nml_array`. Usage 
replaced in `glm_nml` and `nml` modules with 
`NMLWriter.write_nml_list`/`NMLReader.read_nml_list`

### 0.3.1 <small>(13 December, 2024)</small> { id="0.3.1" }

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

### 0.2.0 <small>(24 June, 2024)</small> { id="0.2.0" }

- The `nml` module has been split into `nml` and `glm_nml` sub-modules.
- The `glm_nml` sub-module provides high-level NML tools and implements all the 
existing classes from the `nml` module in `0.1.3`.
  - Classes from `0.1.3` are automatically imported using 
  `from glmpy import nml` to maintain backwards compatibility until `1.0.0`.
  - Class names from `0.1.3` will be deprecated by `1.0.0` in favour of a new 
  naming convention that ensures forwards compatibility with AED. Warnings are 
  raised to encourage you to migrate to the new class names.
- The new `nml` sub-module provides low-level tools for reading and writing any
NML file (GLM or AED).
  - `NMLWriter` converts a nested Python dictionary to an NML file. 
  - `NMLReader` converts an NML file to a nested Python dictionary. 
  - Both classes provide functionality to explicitly control how each parameter
  is read/written to file.
- `InvertedTruncatedCone` class added to the `dimensions` module to calculate
morphometry parameters for simple circular water bodies.

### 0.1.3 <small>(22 March, 2024)</small> { id="0.1.3" }

- glm-py released! 🚀
