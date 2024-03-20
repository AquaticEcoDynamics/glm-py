# glm-py ![Image title](https://raw.githubusercontent.com/AquaticEcoDynamics/GLM/master/glm.png){ align=right width="150"}


Python tools for running General Lake Model (GLM) simulations.

## GLM

GLM is a 1-dimensional lake water balance and stratification model. It can also be coupled with a powerful ecological modelling library to support simulations of lake water quality and ecosystem processes.

GLM is suitable for a wide range of natural and engineered lakes, including shallow (well-mixed) and deep (stratified) systems. The model has been successfully applied to systems from the scale of individual ponds and wetlands to the scale of Great Lakes.

For more information about running GLM, please see the model website's <a href="https://aed.see.uwa.edu.au/research/models/glm/overview.html" target="_blank">scientific basis description</a> and the <a href="https://aquaticecodynamics.github.io/glm-workbook/" target="_blank">GLM workbook</a>. 

The <a href="https://github.com/AquaticEcoDynamics/glm-aed/tree/main/binaries" target="_blank">GLM model</a> is available as an executable for Linux (Ubuntu), MacOS, and Windows. It is actively developed by the 
[Aquatic EcoDynamics](https://github.com/AquaticEcoDynamics) research group at The University of Western Australia.

## Why GLM-py?

GLM-py provides a series of classes, functions, and data structures that support running GLM simulations, preparing model input data and configurations, and processing model outputs. 

Its goal is to make running and deploying GLM in a range of environments easy, e.g., building APIs for web applications or cloud services that use GLM, running batches of GLM simulations on HPCs, and running GLM simulations locally within Python environments such as JupyterLab or QGIS. 

### NML

Classes that store model parameters and methods that generate `.nml` configuration files for running GLM. 

### Dimensions

Turns simple user descriptions of lake geometries and dimensions into appropriate morphometry parameters.

### GLM_JSON

Tools to convert JSON data to `.nml` format data. Useful for handling client requests if GLM is deployed within a web API / REST API.

### Simulations

Classes to handle running GLM simulations and processing output data into CSV, JSON, NetCDF files, or generating a JSON stream to pass onto clients. 
