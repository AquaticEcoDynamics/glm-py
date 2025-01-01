---
draft: false 
date: 2024-06-24 
authors:
  - gknight
categories:
  - Tutorials
readtime: 20
---

# Modelling Sparkling Lake with glm-py

**This tutorial guides users through the process of setting up a model of 
Sparkling Lake using glm-py.**

<a target="_blank" href="https://colab.research.google.com/github/AquaticEcoDynamics/glm-py/blob/main/notebooks/sparkling-lake-tutorial.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Sparkling Lake is an oligotrophic, northern temperate lake (89.7 ºN, 46.3 ºW) in Winconsin, USA. The lake is approximately 20m deep and covers a surface area of 0.638km<sup>2</sup>. This tutorial serves an introduction to the two core modules of glm-py - `nml` and `simulation`. You will use glm-py to model Sparkling Lake for 2 years (1980-04-15 to 1982-04-15).

<!-- more -->

First, install glm-py using `pip`:

```
pip install glm-py
```

## Creating a GLM NML file

Next, import the `glm_nml` sub-module from the `nml` module of `glmpy`:

```python
from glmpy.nml import glm_nml
```

The `glm_nml` module provides a set of classes to construct GLM's NML file (`.nml`).  A NML file is divided into multiple "blocks" that configure specific aspects of the model, e.g., the `morphometry` block defines morphometry of the water body. The structure of a NML file is shown below for the four minimum required blocks (`...` indicates that the block contains more parameters than shown):

```
&glm_setup
  sim_name = 'GLMSimulation'
  ...
/
&morphometry
  lake_name = 'my_lake'
  ...
/
&time
  timefmt = 3
  ...
/
&init_profiles
  lake_depth = 10
  ...
/
```

### Model setup

GLM simulates the dynamics of a water body by dividing it into a vertically stacked series of layers. The compulsory `glm_setup` block defines the structure of these layers, e.g., the maximum number of layers, the minimum layer volume, and the minimum and maximum layer thicknesses. To configure the `glm_setup` parameters for Sparkling Lake, you would typically write a NML file that contains the following:

```
&glm_setup 
   sim_name = 'Sparkling Lake'
   max_layers = 500
   min_layer_vol = 0.5
   min_layer_thick = 0.15
   max_layer_thick = 0.5
   density_model = 1
   non_avg = .true.
/
```

Using glm-py, you instead configure the `glm_setup` block by using the `SetupBlock` class from the `glm_nml` module. Each model parameter of the `glm_setup` block has a corresponding attribute in the `SetupBlock` class:

```python
glm_setup = glm_nml.SetupBlock(
    sim_name='Sparkling Lake',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
    non_avg=True
)
```

This approach offers a number of advantages over editing a raw NML file:

- Explicit type hinting for parameter types
- Native Python syntax
- Error checking

Once the attributes are set, you can return a dictionary of the consolidated model parameters by calling the `get_params` method:

```python
glm_setup_params = glm_setup.get_params()
print(glm_setup_params)
```

```
{'sim_name': 'Sparkling Lake', 'max_layers': 500, 'min_layer_vol': 0.5, 'min_layer_thick': 0.15, 'max_layer_thick': 0.5, 'density_model': 1, 'non_avg': True}
```

### Mixing and morphometry

Next, let's set the parameters that control the mixing processes within Sparkling Lake. Just as `SetupBlock` defines the `glm_setup` block, we can configure the `mixing` block using the `MixingBlock` class:

```python
mixing = glm_nml.MixingBlock(
    surface_mixing=1,
    coef_mix_conv=0.2,
    coef_wind_stir=0.402,
    coef_mix_shear=0.2,
    coef_mix_turb=0.51,
    coef_mix_KH=0.3,
    deep_mixing=2,
    coef_mix_hyp=0.5,
    diff=0.0
)
```

Let's repeat the same for the `morphometry` block - use the `MorphometryBlock` class:

```python
morphometry = glm_nml.MorphometryBlock(
    lake_name='Sparkling',
    latitude=46.00881,
    longitude=-89.69953,
    bsn_len=901.0385,
    bsn_wid=901.0385,
    crest_elev=320.0,
    bsn_vals=15,
    H=[301.712, 303.018285714286, 304.324571428571,
        305.630857142857, 306.937142857143, 308.243428571429,
        309.549714285714, 310.856, 312.162285714286,
        313.468571428571, 314.774857142857, 316.081142857143,
        317.387428571429, 318.693714285714, 320, 321],
    A=[0, 45545.8263571429, 91091.6527142857,
        136637.479071429, 182183.305428571, 227729.131785714,
        273274.958142857, 318820.7845, 364366.610857143,
        409912.437214286, 455458.263571429, 501004.089928571,
        546549.916285714, 592095.742642857, 637641.569, 687641.569]
)
```

### Setting the remaining blocks

There are up to 14 configurable blocks in the GLM NML file - setting each will take some time! Let's speed up the process by reading the remaining blocks from an existing NML file. Download the NML file to your working directory using `curl`:

```
!curl https://raw.githubusercontent.com/AquaticEcoDynamics/glm-py/main/notebooks/glmpy-demo/glm3.nml --output sparkling_lake.nml
```

To read `sparkling_lake.nml`, we'll use the `NMLReader` class from the `nml.nml` sub-module. After importing the sub-module, initalise the `NMLReader` class and provide the NML file path:

```python 
from glmpy.nml import nml

my_nml_file = nml.NMLReader("sparkling_lake.nml")
```
Next, let's extract the parameters for the `meteorology` block using the `get_block` method:

```python
meteorology_params = my_nml_file.get_block("meteorology")
```

Take a look at what `meteorology_params` contains:

```python
print(meteorology_attrs)
```

```
{'met_sw': True, 'lw_type': 'LW_IN', 'rain_sw': False, 'atm_stab': 0, 'catchrain': False, 'rad_mode': 1, 'albedo_mode': 1, 'cloud_mode': 4, 'fetch_mode': 0, 'subdaily': False, 'meteo_fl': 'bcs/nldas_driver.csv', 'wind_factor': 1.0, 'sw_factor': 1.08, 'lw_factor': 1.0, 'at_factor': 1.0, 'rh_factor': 1.0, 'rain_factor': 1.0, 'ce': 0.00132, 'ch': 0.0014, 'cd': 0.0013, 'rain_threshold': 0.01, 'runoff_coef': 0.3}
```

This is a dictionary containing all `meteorology` parameters from `sparkling_lake.nml` in Python data types. Look closely at the `meteo_fl` parameter - what's `bcs/nldas_driver.csv`? This is a path to a CSV that contains boundary condition data for Sparkling Lake, e.g., daily rainfall, wind speed, and air temperature. You'll need this file to run the model. Let's download it with `curl` and place it in sub-directory called `bcs`:

```
!mkdir bcs
!curl https://raw.githubusercontent.com/AquaticEcoDynamics/glm-py/main/notebooks/glmpy-demo/bcs/nldas_driver.csv --output bcs/nldas_driver.csv
```

Now, let's get the parameters for the remaining blocks:  `output`, `init_profiles`, `time`, `bird_model`, `light`, `sediment`. We'll use the `get_block` method from our instance of `NMLReader`:

```python
output_params=my_nml_file.get_block("output")
init_profiles_params=my_nml_file.get_block("init_profiles")
time_params=my_nml_file.get_block("time")
light_params=my_nml_file.get_block("light")
bird_model_params=my_nml_file.get_block("bird_model")
sediment_params=my_nml_file.get_block("sediment")
```

### Writing the NML file

We now have a dictionary of model parameters for each block. Let's combine them to create the NML file. First, create an instance of the `GLMNML` class from the `glm_nml` sub-module. Then pass in the dictionaries of parameters:

```python
my_nml = glm_nml.GLMNML(
  glm_setup=glm_setup.get_params(),
  mixing=mixing.get_params(),
  morphometry=morphometry.get_params(),
  time=time_params,
  output=output_params,
  init_profiles=init_profiles_params,
  meteorology=meteorology_params,
  bird_model=bird_model_params,
  light=light_params,
  sediment=sediment_params
)
```

Finally, use the `write_nml()` method to save the `.nml` to your working directory:

```python
my_nml.write_nml(nml_file_path='glm3.nml')
```

## Running the model

Model configuration is now complete! To run our Sparkling Lake simulation, import the `simulation` module:

```python
from glmpy import simulation
```

We now need to specify the location of any files that we'll use in the simulation. For Sparkling Lake, that's just your newly created `glm3.nml` and the meterological boundary condition file `nldas_driver.csv`. These will be defined in a dictionary where the key is the filename and the value is the file path:

```python
files = {
    "glm3.nml": "glm3.nml",
    "nldas_driver.csv": "bcs/nldas_driver.csv"
}
```

Now pass this dictionary to a new instance of the `GLMSim` class. `GLMSim` is used prepare a new directory of model inputs that we'll point GLM at . Set `api` to `False` to run the simulation locally and set `inputs_dir` to the name of the inputs directory that will be created:

```python
glm_sim = simulation.GLMSim(
  input_files=files,
  api=False,
  inputs_dir="inputs"
)
```

Create the `inputs` directory by calling the `.prepare_inputs()` method:

```python
inputs_dir = glm_sim.prepare_inputs()
```

You should now have a new directory that looks like this:

```
├── bcs
│   └── nldas_driver.csv
├── glm3.nml
```

Finally, run the simulation by calling the `.glm_run()` method and pass in the `inputs_dir` object:

```python
glm_sim.glm_run(inputs_dir=inputs_dir)
```

Congratulations! You've now configured and run a GLM simulation entirely in Python. You should see a new sub-directory called `outputs` within the `inputs` directory that contains the model results.


